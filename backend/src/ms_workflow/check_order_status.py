import json
from common.db import orders_table, order_events_table
from boto3.dynamodb.conditions import Key


def handler(event, context):
    """
    Lambda llamada por Step Functions para verificar el estado actual de una orden.
    Retorna el estado actual y los tiempos registrados.
    """
    tenant_id = event.get("tenant_id")
    order_id = event.get("order_id")

    if not tenant_id or not order_id:
        return {
            "statusCode": 400,
            "error": "tenant_id and order_id required"
        }

    # Obtener la orden actual
    resp = orders_table().get_item(
        Key={"tenant_id": tenant_id, "order_id": order_id}
    )

    if "Item" not in resp:
        return {
            "statusCode": 404,
            "error": "Order not found"
        }

    order = resp["Item"]

    # Obtener todos los eventos de esta orden para calcular tiempos
    events_resp = order_events_table().query(
        KeyConditionExpression=Key("order_id").eq(order_id),
        ScanIndexForward=True  # Ordenar por timestamp ascendente
    )

    events = events_resp.get("Items", [])

    return {
        "statusCode": 200,
        "tenant_id": tenant_id,
        "order_id": order_id,
        "current_status": order.get("status"),
        "created_at": order.get("created_at"),
        "updated_at": order.get("updated_at"),
        "workflow_events": events,
        "total_events": len(events)
    }
