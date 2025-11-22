import json
from collections import Counter
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

from common.db import orders_table, order_events_table


def calculate_time_diff(start_time_str, end_time_str):
    """Calcula diferencia en minutos entre dos timestamps ISO"""
    try:
        start = datetime.fromisoformat(start_time_str)
        end = datetime.fromisoformat(end_time_str)
        diff_seconds = (end - start).total_seconds()
        return round(diff_seconds / 60, 2)  # Retornar en minutos
    except:
        return None


def get_order_timeline_metrics(order):
    """Calcula métricas de tiempo para una orden individual"""
    metrics = {
        "order_id": order.get("order_id"),
        "status": order.get("status"),
        "created_at": order.get("created_at"),
        "phases": {}
    }

    created_at = order.get("created_at")

    # Analizar cada fase del workflow
    phases = ["cooking", "packing", "delivering", "delivered"]
    for phase in phases:
        phase_start = order.get(f"{phase}_started_at")
        if phase_start:
            time_from_creation = calculate_time_diff(created_at, phase_start)
            metrics["phases"][phase] = {
                "started_at": phase_start,
                "time_from_creation_minutes": time_from_creation,
                "attended_by": order.get(f"{phase}_by", "N/A")
            }

    # Calcular tiempo total si la orden está completada
    if order.get("status") == "DELIVERED" and order.get("delivered_started_at"):
        total_time = calculate_time_diff(created_at, order.get("delivered_started_at"))
        metrics["total_time_minutes"] = total_time

    return metrics


def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")

    if not tenant_id:
        return {"statusCode": 400, "body": json.dumps({"message": "tenantId required"})}

    table = orders_table()
    resp = table.query(
        KeyConditionExpression=Key("tenant_id").eq(tenant_id)
    )
    items = resp.get("Items", [])

    # Contador de órdenes por estado
    counts = Counter(o.get("status", "UNKNOWN") for o in items)

    # Separar órdenes completadas vs en proceso
    completed_orders = [o for o in items if o.get("status") == "DELIVERED"]
    in_progress_orders = [o for o in items if o.get("status") != "DELIVERED"]

    # Calcular métricas de tiempo para órdenes completadas
    total_time_minutes = []
    phase_times = {
        "cooking": [],
        "packing": [],
        "delivering": []
    }

    for order in completed_orders:
        created_at = order.get("created_at")
        delivered_at = order.get("delivered_started_at")

        if created_at and delivered_at:
            total = calculate_time_diff(created_at, delivered_at)
            if total:
                total_time_minutes.append(total)

        # Calcular tiempo en cada fase
        cooking_start = order.get("cooking_started_at")
        packing_start = order.get("packing_started_at")
        delivering_start = order.get("delivering_started_at")
        delivered_at = order.get("delivered_started_at")

        if cooking_start and packing_start:
            cooking_time = calculate_time_diff(cooking_start, packing_start)
            if cooking_time:
                phase_times["cooking"].append(cooking_time)

        if packing_start and delivering_start:
            packing_time = calculate_time_diff(packing_start, delivering_start)
            if packing_time:
                phase_times["packing"].append(packing_time)

        if delivering_start and delivered_at:
            delivering_time = calculate_time_diff(delivering_start, delivered_at)
            if delivering_time:
                phase_times["delivering"].append(delivering_time)

    # Calcular promedios
    avg_total_time = round(sum(total_time_minutes) / len(total_time_minutes), 2) if total_time_minutes else 0

    avg_phase_times = {}
    for phase, times in phase_times.items():
        avg_phase_times[phase] = round(sum(times) / len(times), 2) if times else 0

    # Obtener órdenes recientes con sus métricas detalladas
    recent_orders = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
    recent_metrics = []
    for order in recent_orders:
        recent_metrics.append(get_order_timeline_metrics(order))

    summary = {
        "tenant_id": tenant_id,
        "total_orders": len(items),
        "by_status": dict(counts),
        "completed_orders": len(completed_orders),
        "in_progress_orders": len(in_progress_orders),
        "average_times": {
            "total_delivery_minutes": avg_total_time,
            "total_delivery_hours": round(avg_total_time / 60, 2) if avg_total_time else 0,
            "phases": {
                "cooking_minutes": avg_phase_times.get("cooking", 0),
                "packing_minutes": avg_phase_times.get("packing", 0),
                "delivering_minutes": avg_phase_times.get("delivering", 0)
            }
        },
        "recent_orders": recent_metrics
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(summary, default=str),
    }
