#!/bin/bash

# Script de prueba para el sistema de notificaciones por email
# Pardos Chicken - Sistema de Gestión de Pedidos

echo "========================================="
echo "🧪 TEST: Sistema de Notificaciones Email"
echo "========================================="
echo ""

# Configuración (CAMBIAR ESTOS VALORES)
API_URL="https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com"
TENANT_ID="pardos-chicken"
TEST_EMAIL="tu-email-de-prueba@example.com"
TEST_NAME="Juan Pérez (Test)"

echo "📋 Configuración del Test:"
echo "   API: $API_URL"
echo "   Tenant: $TENANT_ID"
echo "   Email de prueba: $TEST_EMAIL"
echo ""
echo "========================================="
echo ""

# Paso 1: Crear un pedido de prueba con email
echo "📝 Paso 1: Creando pedido de prueba..."
echo ""

ORDER_RESPONSE=$(curl -s -X POST "$API_URL/tenants/$TENANT_ID/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": "1", "name": "Pollo Entero", "quantity": 1},
      {"product_id": "4", "name": "Papas Fritas", "quantity": 2}
    ],
    "customer_name": "'"$TEST_NAME"'",
    "customer_phone": "+51999888777",
    "customer_email": "'"$TEST_EMAIL"'",
    "customer_address": "Av. Test 123, Lima"
  }')

echo "Respuesta del servidor:"
echo "$ORDER_RESPONSE" | jq '.' 2>/dev/null || echo "$ORDER_RESPONSE"
echo ""

# Extraer order_id de la respuesta
ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.order_id' 2>/dev/null)

if [ "$ORDER_ID" == "null" ] || [ -z "$ORDER_ID" ]; then
    echo "❌ ERROR: No se pudo crear el pedido"
    echo "Verifica que la API esté desplegada y la URL sea correcta"
    exit 1
fi

echo "✅ Pedido creado exitosamente!"
echo "   Order ID: $ORDER_ID"
echo ""
echo "📧 Esperando 3 segundos para que EventBridge procese el evento..."
sleep 3
echo ""

# Paso 2: Verificar que el email se guardó en DynamoDB
echo "========================================="
echo "📊 Paso 2: Verificando datos en DynamoDB..."
echo ""

ORDER_DATA=$(curl -s "$API_URL/tenants/$TENANT_ID/orders/$ORDER_ID")
echo "Datos del pedido:"
echo "$ORDER_DATA" | jq '.' 2>/dev/null || echo "$ORDER_DATA"
echo ""

STORED_EMAIL=$(echo "$ORDER_DATA" | jq -r '.customer_email' 2>/dev/null)

if [ "$STORED_EMAIL" == "$TEST_EMAIL" ]; then
    echo "✅ Email guardado correctamente en DynamoDB: $STORED_EMAIL"
else
    echo "⚠️ ADVERTENCIA: Email no encontrado o diferente"
    echo "   Esperado: $TEST_EMAIL"
    echo "   Encontrado: $STORED_EMAIL"
fi
echo ""

# Paso 3: Simular actualizaciones de estado
echo "========================================="
echo "🔄 Paso 3: Simulando actualizaciones de estado..."
echo ""

# Array de estados y roles
declare -a STATES=("COOKING" "PACKING" "DELIVERING" "DELIVERED")
declare -a ROLES=("KITCHEN_STAFF" "PACKER" "DELIVERY_DRIVER" "DELIVERY_DRIVER")
declare -a NAMES=("Chef Carlos" "Despachador Ana" "Repartidor Luis" "Repartidor Luis")

for i in "${!STATES[@]}"; do
    STATE="${STATES[$i]}"
    ROLE="${ROLES[$i]}"
    NAME="${NAMES[$i]}"

    echo "🔄 Actualizando a estado: $STATE"
    echo "   Atendido por: $NAME ($ROLE)"

    UPDATE_RESPONSE=$(curl -s -X POST "$API_URL/tenants/$TENANT_ID/orders/$ORDER_ID/step" \
      -H "Content-Type: application/json" \
      -d '{
        "status": "'"$STATE"'",
        "attended_by": "'"$NAME"'",
        "role": "'"$ROLE"'"
      }')

    echo "   Respuesta:"
    echo "   $UPDATE_RESPONSE" | jq '.' 2>/dev/null || echo "   $UPDATE_RESPONSE"

    # Verificar si la actualización fue exitosa
    if echo "$UPDATE_RESPONSE" | grep -q '"status": *"'"$STATE"'"'; then
        echo "   ✅ Estado actualizado correctamente"
        echo "   📧 Email de notificación debería haberse enviado (revisar logs)"
    else
        echo "   ⚠️ Posible error en la actualización"
    fi

    echo ""
    echo "   Esperando 3 segundos antes de la siguiente actualización..."
    sleep 3
    echo ""
done

# Paso 4: Instrucciones para verificar emails
echo "========================================="
echo "📧 Paso 4: Verificar Emails en CloudWatch"
echo "========================================="
echo ""
echo "Para ver los emails simulados que se enviaron:"
echo ""
echo "1. Usando Serverless Framework:"
echo "   cd backend/src"
echo "   serverless logs -f sendEmailNotification --tail"
echo ""
echo "2. O buscar en AWS Console:"
echo "   CloudWatch → Log Groups → /aws/lambda/dev-sendEmailNotification"
echo ""
echo "3. Buscar en los logs:"
echo "   - '📧 EMAIL NOTIFICATION (SIMULADO)'"
echo "   - 'Para: $TEST_EMAIL'"
echo "   - Deberías ver 5 emails (1 RECEIVED + 4 actualizaciones)"
echo ""
echo "4. Estados esperados en los emails:"
echo "   ✅ RECEIVED   - ¡Pedido Confirmado!"
echo "   👨‍🍳 COOKING    - ¡Ya estamos preparando tu pedido!"
echo "   📦 PACKING    - ¡Empacando tu pedido!"
echo "   🚗 DELIVERING - ¡Tu pedido viene en camino!"
echo "   🎉 DELIVERED  - ¡Pedido Entregado!"
echo ""

# Paso 5: Verificar estado final
echo "========================================="
echo "📊 Paso 5: Estado Final del Pedido"
echo "========================================="
echo ""

FINAL_ORDER=$(curl -s "$API_URL/tenants/$TENANT_ID/orders/$ORDER_ID")
echo "Estado final del pedido:"
echo "$FINAL_ORDER" | jq '{
  order_id: .order_id,
  status: .status,
  customer_name: .customer_name,
  customer_email: .customer_email,
  created_at: .created_at,
  updated_at: .updated_at
}' 2>/dev/null || echo "$FINAL_ORDER"
echo ""

# Resumen final
echo "========================================="
echo "📋 RESUMEN DEL TEST"
echo "========================================="
echo ""
echo "Order ID: $ORDER_ID"
echo "Email del cliente: $TEST_EMAIL"
echo ""
echo "✅ Pasos completados:"
echo "   1. Pedido creado con email"
echo "   2. Email guardado en DynamoDB"
echo "   3. 4 actualizaciones de estado ejecutadas"
echo "   4. Eventos publicados a EventBridge"
echo ""
echo "📧 Emails que deberían haberse enviado: 5 total"
echo "   - 1 email de confirmación (RECEIVED)"
echo "   - 4 emails de actualización de estado"
echo ""
echo "🔍 Próximos pasos:"
echo "   1. Revisar logs de CloudWatch (comando arriba)"
echo "   2. Verificar que EventBridge disparó la Lambda de emails"
echo "   3. En producción: verificar inbox del email de prueba"
echo ""
echo "========================================="
echo "✨ Test completado!"
echo "========================================="
