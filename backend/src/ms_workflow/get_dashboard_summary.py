import json
from collections import Counter
from boto3.dynamodb.conditions import Key

from common.db import orders_table

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

    counts = Counter(o.get("status", "UNKNOWN") for o in items)

    summary = {
        "total_orders": len(items),
        "by_status": counts,
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(summary),
    }
