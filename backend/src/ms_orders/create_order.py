import json
import uuid
from datetime import datetime, timezone

from common.db import orders_table, order_events_table
from common.events import publish_event

def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId", "pardos-chicken")

    items = body.get("items", [])
    customer_name = body.get("customer_name", "Anonimo")
    customer_address = body.get("customer_address", "")
    customer_phone = body.get("customer_phone", "")
    customer_email = body.get("customer_email", "")

    if not items:
        return {"statusCode": 400, "body": json.dumps({"message": "items is required"})}

    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    order = {
        "tenant_id": tenant_id,
        "order_id": order_id,
        "status": "RECEIVED",
        "items": items,
        "customer_name": customer_name,
        "customer_address": customer_address,
        "customer_phone": customer_phone,
        "customer_email": customer_email,
        "created_at": now,
        "updated_at": now,
    }

    orders_table().put_item(Item=order)

    # Evento en tabla de eventos
    order_events_table().put_item(
        Item={
            "order_id": order_id,
            "ts": now,
            "status": "RECEIVED",
            "by_role": "SYSTEM",
        }
    )

    # Publicación al bus de eventos -> Step Functions y Email Notifications
    publish_event(
        source="pardos.orders",
        detail_type="order.created",
        detail={
            "tenant_id": tenant_id,
            "order_id": order_id,
            "status": "RECEIVED",
            "customer_email": customer_email,
            "customer_name": customer_name,
        },
    )

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"order_id": order_id, "status": "RECEIVED"}),
    }
