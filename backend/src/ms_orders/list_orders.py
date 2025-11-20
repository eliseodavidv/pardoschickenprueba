import json
from boto3.dynamodb.conditions import Key
from common.db import orders_table

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")

    if not tenant_id:
        return {"statusCode": 400, "body": json.dumps({"message": "tenantId required"})}

    status_filter = (event.get("queryStringParameters") or {}).get("status")

    table = orders_table()
    resp = table.query(
        KeyConditionExpression=Key("tenant_id").eq(tenant_id)
    )
    items = resp.get("Items", [])

    if status_filter:
        items = [o for o in items if o.get("status") == status_filter]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
