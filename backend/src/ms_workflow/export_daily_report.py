import os
import json
from datetime import datetime, timezone
import boto3
from boto3.dynamodb.conditions import Key

from common.db import orders_table

s3 = boto3.client("s3")
REPORTS_BUCKET = os.environ["REPORTS_BUCKET"]

def handler(event, context):
    # Exporta todas las órdenes del día actual (simplificado)
    now = datetime.now(timezone.utc)
    date_prefix = now.strftime("%Y-%m-%d")

    # En escenario real filtrarías por fecha; aquí exportamos todo.
    table = orders_table()
    # Para demo: scan (si crece mucho, habría que paginar)
    scan = table.scan()
    orders = scan.get("Items", [])

    key = f"pardos-chicken/{date_prefix}/orders.json"
    s3.put_object(
        Bucket=REPORTS_BUCKET,
        Key=key,
        Body=json.dumps(orders).encode("utf-8"),
        ContentType="application/json",
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "report generated", "key": key}),
    }
