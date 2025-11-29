import json
import os
from datetime import datetime
import urllib.request
import urllib.error

# SendGrid API Key desde variables de entorno
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
SENDGRID_FROM_EMAIL = 'eliseo.velasquez@utec.edu.pe'
SENDGRID_FROM_NAME = 'Pardos Chicken'

def handler(event, context):
    """
    Lambda que envía notificaciones por email cuando cambia el estado de un pedido.
    Se dispara desde EventBridge cuando ocurren eventos de pedidos.

    Usa SendGrid para enviar emails reales a cada cliente.
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
        email_subject, email_text = generate_email_content(
            detail_type=detail_type,
            status=status,
            order_id=order_id,
            customer_name=customer_name
        )

        # Enviar email usando SendGrid
        if SENDGRID_API_KEY:
            try:
                message_id = send_email_sendgrid(
                    to_email=customer_email,
                    to_name=customer_name,
                    subject=email_subject,
                    text_content=email_text
                )

                print(f"""
                ========================================
                📧 EMAIL ENVIADO via SendGrid
                ========================================
                Para: {customer_email}
                Nombre: {customer_name}
                Asunto: {email_subject}
                Estado: {status}
                Order ID: {order_id}
                MessageId: {message_id}
                ========================================
                """)

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Email sent successfully via SendGrid',
                        'email': customer_email,
                        'order_id': order_id,
                        'status': status,
                        'messageId': message_id
                    })
                }

            except Exception as sendgrid_error:
                print(f"Error enviando via SendGrid: {str(sendgrid_error)}")
                # Log del error y continuar
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': f'SendGrid error: {str(sendgrid_error)}',
                        'email': customer_email,
                        'order_id': order_id
                    })
                }

        # Fallback: Log simulado si no hay SendGrid configurado
        print(f"""
        ========================================
        📧 EMAIL NOTIFICATION (Log - SendGrid no configurado)
        ========================================
        Para: {customer_email}
        Asunto: {email_subject}
        Estado: {status}
        Order ID: {order_id}

        NOTA: Configure SENDGRID_API_KEY para enviar emails reales
        ========================================
        """)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Email logged (SendGrid not configured)',
                'email': customer_email,
                'order_id': order_id,
                'status': status
            })
        }

    except Exception as e:
        print(f"Error sending email notification: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def send_email_sendgrid(to_email, to_name, subject, text_content):
    """
    Envía un email usando la API de SendGrid
    """
    url = 'https://api.sendgrid.com/v3/mail/send'

    # Construir el payload según la API de SendGrid
    payload = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': to_email,
                        'name': to_name
                    }
                ],
                'subject': subject
            }
        ],
        'from': {
            'email': SENDGRID_FROM_EMAIL,
            'name': SENDGRID_FROM_NAME
        },
        'content': [
            {
                'type': 'text/plain',
                'value': text_content
            }
        ]
    }

    # Preparar la petición HTTP
    headers = {
        'Authorization': f'Bearer {SENDGRID_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')

            # SendGrid retorna 202 Accepted para emails enviados exitosamente
            if response.status == 202:
                # Obtener el Message ID del header
                message_id = response.headers.get('X-Message-Id', 'unknown')
                return message_id
            else:
                raise Exception(f"SendGrid returned status {response.status}: {response_body}")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"SendGrid API error ({e.code}): {error_body}")
    except Exception as e:
        raise Exception(f"Error calling SendGrid: {str(e)}")


def generate_email_content(detail_type, status, order_id, customer_name):
    """
    Genera el asunto y contenido de texto del email según el tipo de evento.
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

    # Generar cuerpo de texto plano
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
