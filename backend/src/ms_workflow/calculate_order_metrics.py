import json
from datetime import datetime, timezone
from common.db import order_events_table
from boto3.dynamodb.conditions import Key


def handler(event, context):
    """
    Lambda para calcular métricas de tiempo de una orden.
    Calcula tiempo en cada estado del workflow.
    """
    order_id = event.get("order_id")

    if not order_id:
        return {
            "statusCode": 400,
            "error": "order_id required"
        }

    # Obtener todos los eventos de esta orden ordenados por tiempo
    events_resp = order_events_table().query(
        KeyConditionExpression=Key("order_id").eq(order_id),
        ScanIndexForward=True  # Orden ascendente por timestamp
    )

    events = events_resp.get("Items", [])

    if not events:
        return {
            "statusCode": 404,
            "error": "No events found for this order"
        }

    # Calcular tiempos entre cada transición de estado
    metrics = {
        "order_id": order_id,
        "total_events": len(events),
        "state_durations": {},
        "state_transitions": []
    }

    for i in range(len(events)):
        current_event = events[i]
        current_status = current_event.get("status")
        current_time = datetime.fromisoformat(current_event.get("ts"))

        transition = {
            "status": current_status,
            "timestamp": current_event.get("ts"),
            "attended_by": current_event.get("by", "N/A"),
            "role": current_event.get("by_role", "N/A")
        }

        # Si hay un evento siguiente, calcular duración en este estado
        if i < len(events) - 1:
            next_event = events[i + 1]
            next_time = datetime.fromisoformat(next_event.get("ts"))
            duration_seconds = (next_time - current_time).total_seconds()

            transition["duration_seconds"] = duration_seconds
            transition["duration_minutes"] = round(duration_seconds / 60, 2)

            metrics["state_durations"][current_status] = {
                "seconds": duration_seconds,
                "minutes": round(duration_seconds / 60, 2)
            }

        metrics["state_transitions"].append(transition)

    # Calcular tiempo total desde creación hasta último evento
    if len(events) >= 2:
        first_time = datetime.fromisoformat(events[0].get("ts"))
        last_time = datetime.fromisoformat(events[-1].get("ts"))
        total_seconds = (last_time - first_time).total_seconds()

        metrics["total_duration"] = {
            "seconds": total_seconds,
            "minutes": round(total_seconds / 60, 2),
            "hours": round(total_seconds / 3600, 2)
        }

    return {
        "statusCode": 200,
        "metrics": metrics
    }
