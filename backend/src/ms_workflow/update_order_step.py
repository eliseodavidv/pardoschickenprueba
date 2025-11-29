import json
from datetime import datetime, timezone

from common.db import orders_table, order_events_table
from common.events import publish_event

# Estados válidos y transiciones permitidas
VALID_STATES = ["RECEIVED", "COOKING", "PACKING", "DELIVERING", "DELIVERED"]

# Definir transiciones válidas (flujo del workflow)
VALID_TRANSITIONS = {
    "RECEIVED": ["COOKING"],
    "COOKING": ["PACKING"],
    "PACKING": ["DELIVERING"],
    "DELIVERING": ["DELIVERED"],
    "DELIVERED": []  # Estado final, no hay transiciones
}

# Roles esperados para cada transición
EXPECTED_ROLES = {
    "COOKING": "KITCHEN_STAFF",      # Cocinero
    "PACKING": "PACKER",             # Despachador
    "DELIVERING": "DELIVERY_DRIVER", # Repartidor
    "DELIVERED": "DELIVERY_DRIVER"   # Repartidor confirma entrega
}


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

    # Obtener el estado actual de la orden
    resp = orders_table().get_item(
        Key={"tenant_id": tenant_id, "order_id": order_id}
    )

    if "Item" not in resp:
        return {"statusCode": 404, "body": json.dumps({"message": "Order not found"})}

    current_order = resp["Item"]
    current_status = current_order.get("status", "RECEIVED")

    # Validar que la transición sea válida
    if new_status not in VALID_TRANSITIONS.get(current_status, []):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Invalid transition from {current_status} to {new_status}",
                "current_status": current_status,
                "allowed_next_states": VALID_TRANSITIONS.get(current_status, [])
            })
        }

    # Advertir si el rol no es el esperado (no bloquear, solo advertir)
    expected_role = EXPECTED_ROLES.get(new_status)
    role_warning = None
    if expected_role and role != expected_role:
        role_warning = f"Expected role {expected_role} but got {role}"

    now = datetime.now(timezone.utc).isoformat()

    # Crear campos dinámicos para rastrear tiempos de cada fase
    # Por ejemplo: cooking_started_at, packing_started_at, etc.
    phase_field = f"{new_status.lower()}_started_at"
    phase_by_field = f"{new_status.lower()}_by"

    # Actualizar orden con estado nuevo y timestamps
    orders_table().update_item(
        Key={"tenant_id": tenant_id, "order_id": order_id},
        UpdateExpression="SET #s = :s, updated_at = :u, #phase = :phase_time, #phase_by = :phase_by",
        ExpressionAttributeNames={
            "#s": "status",
            "#phase": phase_field,
            "#phase_by": phase_by_field
        },
        ExpressionAttributeValues={
            ":s": new_status,
            ":u": now,
            ":phase_time": now,
            ":phase_by": attended_by
        },
    )

    # Registrar evento de workflow con más detalle
    order_events_table().put_item(
        Item={
            "order_id": order_id,
            "ts": now,
            "status": new_status,
            "by": attended_by,
            "by_role": role,
            "previous_status": current_status,
            "tenant_id": tenant_id
        }
    )

    # Publicar evento de actualización (por si otra cosa quiere consumirlo)
    # Incluir datos del cliente para notificaciones por email
    publish_event(
        source="pardos.orders",
        detail_type="order.updated",
        detail={
            "tenant_id": tenant_id,
            "order_id": order_id,
            "status": new_status,
            "previous_status": current_status,
            "by_role": role,
            "attended_by": attended_by,
            "customer_email": current_order.get("customer_email", ""),
            "customer_name": current_order.get("customer_name", "Cliente"),
        },
    )

    response_body = {
        "order_id": order_id,
        "status": new_status,
        "previous_status": current_status,
        "attended_by": attended_by,
        "role": role,
        "timestamp": now
    }

    if role_warning:
        response_body["warning"] = role_warning

    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
    }
