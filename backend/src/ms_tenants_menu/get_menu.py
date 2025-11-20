import json
from boto3.dynamodb.conditions import Key
from common.db import menu_table

def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId", "pardos-chicken")

    table = menu_table()
    resp = table.query(
        KeyConditionExpression=Key("tenant_id").eq(tenant_id)
    )
    items = resp.get("Items", [])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
