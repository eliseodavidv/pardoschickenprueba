import json
from datetime import datetime, timezone

from common.db import orders_table, order_events_table
from common.events import publish_event

VALID_STATES = ["RECEIVED", "COOKING", "PACKING", "DELIVERING", "DELIVERED"]

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")
    order_id = path_params.get("orderId")

    if not tenant_id or not order_id:
        return {"statusCode": 400, "body": json.dumps({"message": "tenantId and orderId required"})}

    body = json.loads(event.get("body") or "{}")
    new_status = body.get("status")
    attended_by = body.get("attended_by", "")
    role = body.get("role", "")

    if new_status not in VALID_STATES:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid status"})}

    now = datetime.now(timezone.utc).isoformat()

    # Actualizar orden
    orders_table().update_item(
        Key={"tenant_id": tenant_id, "order_id": order_id},
        UpdateExpression="SET #s = :s, updated_at = :u",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": new_status, ":u": now},
    )

    # Registrar evento de workflow
    order_events_table().put_item(
        Item={
            "order_id": order_id,
            "ts": now,
            "status": new_status,
            "by": attended_by,
            "by_role": role,
        }
    )

    # Publicar evento de actualización (por si otra cosa quiere consumirlo)
    publish_event(
        source="pardos.orders",
        detail_type="order.updated",
        detail={
            "tenant_id": tenant_id,
            "order_id": order_id,
            "status": new_status,
            "by_role": role,
        },
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"order_id": order_id, "status": new_status}),
    }
