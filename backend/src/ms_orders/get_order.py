import json
from common.db import orders_table
from decimal import Decimal

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")
    order_id = path_params.get("orderId")

    if not tenant_id or not order_id:
        return {"statusCode": 400, "body": json.dumps({"message": "tenantId and orderId required"})}

    resp = orders_table().get_item(
        Key={"tenant_id": tenant_id, "order_id": order_id}
    )

    if "Item" not in resp:
        return {"statusCode": 404, "body": json.dumps({"message": "Order not found"})}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(resp["Item"]),
    }
