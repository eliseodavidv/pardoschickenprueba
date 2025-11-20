import json
from common.db import tenants_table

# Para el curso, devolvemos el tenant Pardos, pero la tabla permite más.
def handler(event, context):
    table = tenants_table()

    # Para simplificar, escanear (pocos tenants)
    resp = table.scan()
    items = resp.get("Items", [])

    # Si la tabla está vacía, devolver Pardos por defecto
    if not items:
        items = [{
            "tenant_id": "pardos-chicken",
            "name": "Pardos Chicken",
            "active": True
        }]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
