import json
import os
from datetime import datetime
import boto3

# Usar SNS para enviar emails (disponible en AWS Academy Learner Lab)
sns_client = boto3.client('sns', region_name='us-east-1')

# Variable de entorno para el SNS Topic ARN
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

def handler(event, context):
    """
    Lambda que envía notificaciones por email cuando cambia el estado de un pedido.
    Se dispara desde EventBridge cuando ocurren eventos de pedidos.

    Usa Amazon SNS para enviar emails reales (funciona en AWS Academy).
    """

    try:
        # Extraer información del evento de EventBridge
        detail = event.get('detail', {})
        detail_type = event.get('detail-type', '')

        order_id = detail.get('order_id')
        status = detail.get('status')
        customer_email = detail.get('customer_email')
        customer_name = detail.get('customer_name', 'Cliente')
        tenant_id = detail.get('tenant_id', 'pardos-chicken')

        if not customer_email:
            print(f"No email provided for order {order_id}, skipping notification")
            return {'statusCode': 200, 'body': json.dumps({'message': 'No email to send'})}

        # Generar el contenido del email según el tipo de evento
        email_subject, email_body = generate_email_content(
            detail_type=detail_type,
            status=status,
            order_id=order_id,
            customer_name=customer_name
        )

        # Enviar email usando SNS
        if SNS_TOPIC_ARN:
            try:
                # Publicar al topic de SNS
                response = sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=email_subject,
                    Message=email_body,
                    MessageAttributes={
                        'order_id': {'DataType': 'String', 'StringValue': order_id},
                        'status': {'DataType': 'String', 'StringValue': status}
                    }
                )

                print(f"""
                ========================================
                📧 EMAIL ENVIADO via SNS
                ========================================
                Para: Suscriptores del Topic SNS
                Topic ARN: {SNS_TOPIC_ARN}
                Asunto: {email_subject}
                Estado: {status}
                Order ID: {order_id}
                MessageId: {response['MessageId']}
                ========================================
                """)

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Email notification sent successfully via SNS',
                        'email': customer_email,
                        'order_id': order_id,
                        'status': status,
                        'messageId': response['MessageId']
                    })
                }

            except Exception as sns_error:
                print(f"Error enviando via SNS: {str(sns_error)}")
                # Continuar con log simulado si falla SNS

        # Fallback: Log simulado si no hay SNS configurado
        print(f"""
        ========================================
        📧 EMAIL NOTIFICATION (Log)
        ========================================
        Para: {customer_email}
        Asunto: {email_subject}
        Estado: {status}
        Order ID: {order_id}

        NOTA: Configure SNS_TOPIC_ARN para enviar emails reales
        ========================================
        """)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Email logged (SNS not configured)',
                'email': customer_email,
                'order_id': order_id,
                'status': status
            })
        }

    except Exception as e:
        print(f"Error sending email notification: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def generate_email_content(detail_type, status, order_id, customer_name):
    """
    Genera el asunto y contenido de texto del email según el tipo de evento.
    Para SNS usamos texto plano ya que no soporta HTML bien.
    """

    status_info = {
        'RECEIVED': {
            'emoji': '✅',
            'title': '¡Pedido Confirmado!',
            'message': 'Hemos recibido tu pedido correctamente',
        },
        'COOKING': {
            'emoji': '👨‍🍳',
            'title': '¡Ya estamos preparando tu pedido!',
            'message': 'Nuestros chefs están cocinando tu delicioso pollo',
        },
        'PACKING': {
            'emoji': '📦',
            'title': '¡Empacando tu pedido!',
            'message': 'Estamos empacando tu pedido con mucho cuidado',
        },
        'DELIVERING': {
            'emoji': '🚗',
            'title': '¡Tu pedido viene en camino!',
            'message': 'El delivery está en camino a tu dirección',
        },
        'DELIVERED': {
            'emoji': '🎉',
            'title': '¡Pedido Entregado!',
            'message': '¡Disfruta tu delicioso Pardos Chicken!',
        }
    }

    info = status_info.get(status, status_info['RECEIVED'])

    subject = f"{info['emoji']} Pardos Chicken - {info['title']}"

    # Generar cuerpo de texto plano para SNS
    text_body = f"""
========================================
🍗 PARDOS CHICKEN - NOTIFICACIÓN DE PEDIDO
========================================

{info['emoji']} {info['title']}

Hola {customer_name},

{info['message']}

----------------------------------------
DETALLES DEL PEDIDO
----------------------------------------
Número de Pedido: #{order_id[:8]}
Estado Actual: {get_status_text(status)}

----------------------------------------
PROGRESO DE TU PEDIDO
----------------------------------------
{get_progress_text(status)}

----------------------------------------
¿Necesitas ayuda?
Contáctanos: +51 999 999 999

Rastrear pedido:
https://main.d1xkjrxtpyszor.amplifyapp.com/client/

© 2025 Pardos Chicken
Sistema de Gestión de Pedidos
========================================
    """

    return subject, text_body.strip()


def generate_email_html(customer_name, order_id, title, message, status, color, emoji):
    """
    Genera el HTML profesional del email con diseño responsive.
    Inspirado en diseños de Rappi, Uber Eats, etc.
    """

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; max-width: 100%; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">

                    <!-- Header con color corporativo -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #d84315 0%, #bf360c 100%); padding: 40px 20px; text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 10px;">🍗</div>
                            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">Pardos Chicken</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 14px;">El mejor pollo a la brasa</p>
                        </td>
                    </tr>

                    <!-- Estado del pedido con icono -->
                    <tr>
                        <td style="padding: 40px 30px; text-align: center;">
                            <div style="font-size: 64px; margin-bottom: 20px;">{emoji}</div>
                            <h2 style="color: {color}; margin: 0 0 10px 0; font-size: 26px;">{title}</h2>
                            <p style="color: #666; font-size: 16px; line-height: 1.5; margin: 0;">
                                Hola <strong>{customer_name}</strong>,<br>
                                {message}
                            </p>
                        </td>
                    </tr>

                    <!-- Información del pedido -->
                    <tr>
                        <td style="padding: 0 30px 30px 30px;">
                            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 20px;">
                                <table style="width: 100%;">
                                    <tr>
                                        <td style="padding: 10px 0; border-bottom: 1px solid #e0e0e0;">
                                            <span style="color: #666; font-size: 14px;">Número de Pedido</span>
                                        </td>
                                        <td align="right" style="padding: 10px 0; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #333; font-size: 14px;">#{order_id[:8]}</strong>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 10px 0;">
                                            <span style="color: #666; font-size: 14px;">Estado Actual</span>
                                        </td>
                                        <td align="right" style="padding: 10px 0;">
                                            <span style="background-color: {color}; color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                                                {get_status_text(status)}
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>

                    <!-- Botón de rastreo (solo si no está entregado) -->
                    {f'''
                    <tr>
                        <td style="padding: 0 30px 30px 30px; text-align: center;">
                            <a href="https://main.d1xkjrxtpyszor.amplifyapp.com/client/index.html"
                               style="display: inline-block; background-color: {color}; color: white; text-decoration: none; padding: 15px 40px; border-radius: 8px; font-weight: bold; font-size: 16px;">
                                📍 Rastrear mi Pedido
                            </a>
                        </td>
                    </tr>
                    ''' if status != 'DELIVERED' else ''}

                    <!-- Timeline visual (opcional para estados intermedios) -->
                    <tr>
                        <td style="padding: 0 30px 30px 30px;">
                            <div style="background-color: #f0f7ff; border-radius: 8px; padding: 20px; text-align: center;">
                                <p style="margin: 0 0 15px 0; color: #666; font-size: 13px;">Progreso de tu pedido:</p>
                                <div style="display: flex; justify-content: space-between; align-items: center; max-width: 400px; margin: 0 auto;">
                                    <div style="text-align: center; flex: 1;">
                                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {get_progress_color('RECEIVED', status)}; margin: 0 auto 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">
                                            ✓
                                        </div>
                                        <span style="font-size: 11px; color: #666;">Recibido</span>
                                    </div>
                                    <div style="flex: 1; height: 2px; background-color: {get_progress_color('COOKING', status)}; margin: 0 5px 15px;"></div>
                                    <div style="text-align: center; flex: 1;">
                                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {get_progress_color('COOKING', status)}; margin: 0 auto 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">
                                            {get_progress_icon('COOKING', status)}
                                        </div>
                                        <span style="font-size: 11px; color: #666;">Cocina</span>
                                    </div>
                                    <div style="flex: 1; height: 2px; background-color: {get_progress_color('PACKING', status)}; margin: 0 5px 15px;"></div>
                                    <div style="text-align: center; flex: 1;">
                                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {get_progress_color('PACKING', status)}; margin: 0 auto 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">
                                            {get_progress_icon('PACKING', status)}
                                        </div>
                                        <span style="font-size: 11px; color: #666;">Empaque</span>
                                    </div>
                                    <div style="flex: 1; height: 2px; background-color: {get_progress_color('DELIVERING', status)}; margin: 0 5px 15px;"></div>
                                    <div style="text-align: center; flex: 1;">
                                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {get_progress_color('DELIVERING', status)}; margin: 0 auto 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">
                                            {get_progress_icon('DELIVERING', status)}
                                        </div>
                                        <span style="font-size: 11px; color: #666;">Entrega</span>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9f9f9; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                            <p style="margin: 0 0 15px 0; color: #999; font-size: 12px;">
                                ¿Necesitas ayuda? Contáctanos:<br>
                                <a href="tel:+51999999999" style="color: #d84315; text-decoration: none;">📞 +51 999 999 999</a>
                            </p>
                            <p style="margin: 0; color: #999; font-size: 11px;">
                                © 2025 Pardos Chicken - Sistema de Gestión de Pedidos<br>
                                Desarrollado con tecnología Cloud Computing
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """


def get_status_text(status):
    """Retorna el texto legible del estado"""
    status_texts = {
        'RECEIVED': 'Recibido',
        'COOKING': 'En Cocina',
        'PACKING': 'Empacando',
        'DELIVERING': 'En Camino',
        'DELIVERED': 'Entregado'
    }
    return status_texts.get(status, status)


def get_progress_text(current_status):
    """Genera una representación de texto del progreso del pedido"""
    steps = [
        ('RECEIVED', 'Recibido', '✓'),
        ('COOKING', 'En Cocina', '👨‍🍳'),
        ('PACKING', 'Empacando', '📦'),
        ('DELIVERING', 'En Camino', '🚗'),
        ('DELIVERED', 'Entregado', '🎉')
    ]

    steps_order = ['RECEIVED', 'COOKING', 'PACKING', 'DELIVERING', 'DELIVERED']
    current_index = steps_order.index(current_status) if current_status in steps_order else 0

    progress = []
    for i, (step_status, step_name, emoji) in enumerate(steps):
        if i <= current_index:
            progress.append(f"✅ {emoji} {step_name}")
        else:
            progress.append(f"⏳ {step_name}")

    return '\n'.join(progress)
