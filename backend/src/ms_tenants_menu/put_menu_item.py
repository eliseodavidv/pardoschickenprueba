import json
import uuid
from common.db import menu_table
from decimal import Decimal

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId", "pardos-chicken")

    body = json.loads(event.get("body") or "{}")
    name = body.get("name")
    price = body.get("price")

    if not name or price is None:
        return {"statusCode": 400, "body": json.dumps({"message": "name and price required"})}

    product_id = body.get("product_id") or str(uuid.uuid4())

    item = {
        "tenant_id": tenant_id,
        "product_id": product_id,
        "name": name,
        "price": float(price),
        "category": body.get("category", "default")
    }

    table = menu_table()
    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item),
    }
