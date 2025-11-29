#!/bin/bash

# Script para suscribir un email al SNS Topic de notificaciones
# Pardos Chicken - Sistema de Gestión de Pedidos

echo "========================================"
echo "📧 Suscripción de Email a SNS"
echo "========================================"
echo ""

# Configuración
STAGE="dev"
TOPIC_NAME="${STAGE}-pardos-order-notifications"

# Pedir el email al usuario
read -p "Ingresa tu email (ej: tu@gmail.com): " USER_EMAIL

if [ -z "$USER_EMAIL" ]; then
    echo "❌ Error: Debes ingresar un email"
    exit 1
fi

echo ""
echo "🔍 Buscando el SNS Topic ARN..."

# Obtener el ARN del topic
TOPIC_ARN=$(aws sns list-topics --query "Topics[?contains(TopicArn, '$TOPIC_NAME')].TopicArn" --output text)

if [ -z "$TOPIC_ARN" ]; then
    echo "❌ Error: No se encontró el topic '$TOPIC_NAME'"
    echo ""
    echo "Asegúrate de haber desplegado el backend primero:"
    echo "   cd backend/src"
    echo "   serverless deploy"
    exit 1
fi

echo "✅ Topic encontrado: $TOPIC_ARN"
echo ""

# Suscribir el email al topic
echo "📧 Suscribiendo email: $USER_EMAIL..."
echo ""

SUBSCRIPTION_ARN=$(aws sns subscribe \
    --topic-arn "$TOPIC_ARN" \
    --protocol email \
    --notification-endpoint "$USER_EMAIL" \
    --query 'SubscriptionArn' \
    --output text)

if [ $? -eq 0 ]; then
    echo "========================================"
    echo "✅ Suscripción Enviada!"
    echo "========================================"
    echo ""
    echo "📧 IMPORTANTE: Revisa tu bandeja de entrada"
    echo ""
    echo "Amazon SNS ha enviado un email de confirmación a:"
    echo "   $USER_EMAIL"
    echo ""
    echo "Debes hacer click en el link de confirmación"
    echo "que dice: 'Confirm subscription'"
    echo ""
    echo "Una vez confirmado, empezarás a recibir emails"
    echo "cada vez que se cree o actualice un pedido."
    echo ""
    echo "========================================"
    echo ""
    echo "📋 Detalles de la suscripción:"
    echo "   Topic ARN: $TOPIC_ARN"
    echo "   Email: $USER_EMAIL"
    echo "   Subscription ARN: $SUBSCRIPTION_ARN"
    echo "========================================"
else
    echo "❌ Error al suscribir el email"
    echo "Verifica tus credenciales de AWS"
fi
