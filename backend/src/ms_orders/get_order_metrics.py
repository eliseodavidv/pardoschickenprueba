import json
from datetime import datetime
from boto3.dynamodb.conditions import Key

from common.db import orders_table, order_events_table


def calculate_time_diff(start_time_str, end_time_str):
    """Calcula diferencia en minutos entre dos timestamps ISO"""
    try:
        start = datetime.fromisoformat(start_time_str)
        end = datetime.fromisoformat(end_time_str)
        diff_seconds = (end - start).total_seconds()
        return {
            "seconds": round(diff_seconds, 2),
            "minutes": round(diff_seconds / 60, 2),
            "hours": round(diff_seconds / 3600, 2)
        }
    except:
        return None


def handler(event, context):
    """
    Endpoint para que el cliente vea métricas de tiempo de su orden.
    GET /tenants/{tenantId}/orders/{orderId}/metrics
    """
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")
    order_id = path_params.get("orderId")

    if not tenant_id or not order_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "tenantId and orderId required"})
        }

    # Obtener la orden
    resp = orders_table().get_item(
        Key={"tenant_id": tenant_id, "order_id": order_id}
    )

    if "Item" not in resp:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Order not found"})
        }

    order = resp["Item"]

    # Obtener todos los eventos de esta orden
    events_resp = order_events_table().query(
        KeyConditionExpression=Key("order_id").eq(order_id),
        ScanIndexForward=True  # Orden ascendente por timestamp
    )

    events = events_resp.get("Items", [])

    # Construir timeline de la orden
    timeline = []
    for event in events:
        timeline.append({
            "status": event.get("status"),
            "timestamp": event.get("ts"),
            "attended_by": event.get("by", "N/A"),
            "role": event.get("by_role", "N/A")
        })

    # Calcular tiempos de cada fase
    created_at = order.get("created_at")
    phase_metrics = {}

    phases = [
        ("cooking", "COOKING", "Cocinero preparando"),
        ("packing", "PACKING", "Empacando pedido"),
        ("delivering", "DELIVERING", "En camino al cliente"),
        ("delivered", "DELIVERED", "Pedido entregado")
    ]

    for phase_key, phase_status, phase_description in phases:
        phase_start = order.get(f"{phase_key}_started_at")
        if phase_start:
            time_from_start = calculate_time_diff(created_at, phase_start)
            phase_metrics[phase_status] = {
                "description": phase_description,
                "started_at": phase_start,
                "time_from_order_creation": time_from_start,
                "attended_by": order.get(f"{phase_key}_by", "N/A")
            }

    # Calcular tiempo total si está completado
    current_status = order.get("status")
    is_completed = current_status == "DELIVERED"
    total_time = None

    if is_completed and order.get("delivered_started_at"):
        total_time = calculate_time_diff(created_at, order.get("delivered_started_at"))

    # Calcular tiempo estimado restante (estimación simple)
    estimated_remaining = None
    if not is_completed:
        # Tiempos promedio estimados por fase (en minutos)
        avg_times = {
            "RECEIVED": 10,   # 10 min para que cocina tome la orden
            "COOKING": 20,    # 20 min cocinando
            "PACKING": 5,     # 5 min empacando
            "DELIVERING": 30  # 30 min entregando
        }

        # Calcular cuántos minutos faltan
        remaining_minutes = 0
        status_order = ["RECEIVED", "COOKING", "PACKING", "DELIVERING", "DELIVERED"]
        current_index = status_order.index(current_status) if current_status in status_order else 0

        for i in range(current_index, len(status_order) - 1):
            remaining_minutes += avg_times.get(status_order[i], 0)

        estimated_remaining = {
            "minutes": remaining_minutes,
            "hours": round(remaining_minutes / 60, 2)
        }

    metrics = {
        "order_id": order_id,
        "tenant_id": tenant_id,
        "current_status": current_status,
        "is_completed": is_completed,
        "created_at": created_at,
        "customer_name": order.get("customer_name", "N/A"),
        "timeline": timeline,
        "phase_metrics": phase_metrics,
        "total_time": total_time,
        "estimated_remaining_time": estimated_remaining
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(metrics, default=str)
    }
