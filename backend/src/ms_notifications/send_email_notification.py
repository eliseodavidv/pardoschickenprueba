import json
import os
from datetime import datetime

# NOTA: En producción real, usarías Amazon SES
# import boto3
# ses_client = boto3.client('ses', region_name='us-east-1')

def handler(event, context):
    """
    Lambda que envía notificaciones por email cuando cambia el estado de un pedido.
    Se dispara desde EventBridge cuando ocurren eventos de pedidos.

    En AWS Academy Learner Lab, esta función SIMULA el envío de emails.
    En producción real, usaría Amazon SES para enviar emails reales.
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
        email_subject, email_html = generate_email_content(
            detail_type=detail_type,
            status=status,
            order_id=order_id,
            customer_name=customer_name
        )

        # En producción real, aquí se enviaría el email con SES:
        # send_email_ses(
        #     to_email=customer_email,
        #     subject=email_subject,
        #     html_body=email_html
        # )

        # Por ahora, solo logeamos para demostración
        print(f"""
        ========================================
        📧 EMAIL NOTIFICATION (SIMULADO)
        ========================================
        Para: {customer_email}
        Asunto: {email_subject}
        Tipo de evento: {detail_type}
        Estado del pedido: {status}
        ID del pedido: {order_id}
        ========================================

        En producción real, este email se enviaría usando Amazon SES.
        El HTML del email está generado y listo para enviar.

        ========================================
        """)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Email notification sent successfully (simulated)',
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
    Genera el asunto y contenido HTML del email según el tipo de evento.
    """

    status_info = {
        'RECEIVED': {
            'emoji': '✅',
            'title': '¡Pedido Confirmado!',
            'message': 'Hemos recibido tu pedido correctamente',
            'color': '#06d6a0'
        },
        'COOKING': {
            'emoji': '👨‍🍳',
            'title': '¡Ya estamos preparando tu pedido!',
            'message': 'Nuestros chefs están cocinando tu delicioso pollo',
            'color': '#f77f00'
        },
        'PACKING': {
            'emoji': '📦',
            'title': '¡Empacando tu pedido!',
            'message': 'Estamos empacando tu pedido con mucho cuidado',
            'color': '#3a86ff'
        },
        'DELIVERING': {
            'emoji': '🚗',
            'title': '¡Tu pedido viene en camino!',
            'message': 'El delivery está en camino a tu dirección',
            'color': '#8338ec'
        },
        'DELIVERED': {
            'emoji': '🎉',
            'title': '¡Pedido Entregado!',
            'message': '¡Disfruta tu delicioso Pardos Chicken!',
            'color': '#06d6a0'
        }
    }

    info = status_info.get(status, status_info['RECEIVED'])

    subject = f"{info['emoji']} Pardos Chicken - {info['title']}"

    # Generar HTML bonito del email
    html_body = generate_email_html(
        customer_name=customer_name,
        order_id=order_id,
        title=info['title'],
        message=info['message'],
        status=status,
        color=info['color'],
        emoji=info['emoji']
    )

    return subject, html_body


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


def get_progress_color(step, current_status):
    """Retorna el color del paso según el progreso"""
    steps_order = ['RECEIVED', 'COOKING', 'PACKING', 'DELIVERING', 'DELIVERED']
    step_index = steps_order.index(step) if step in steps_order else -1
    current_index = steps_order.index(current_status) if current_status in steps_order else -1

    return '#06d6a0' if step_index <= current_index else '#ddd'


def get_progress_icon(step, current_status):
    """Retorna el icono del paso según el progreso"""
    steps_order = ['RECEIVED', 'COOKING', 'PACKING', 'DELIVERING', 'DELIVERED']
    step_index = steps_order.index(step) if step in steps_order else -1
    current_index = steps_order.index(current_status) if current_status in steps_order else -1

    return '✓' if step_index <= current_index else '○'


# Para uso con Amazon SES real (descomentado en producción):
# def send_email_ses(to_email, subject, html_body):
#     """Envía email usando Amazon SES"""
#     try:
#         response = ses_client.send_email(
#             Source='noreply@pardoschicken.com',  # Debe ser verificado en SES
#             Destination={'ToAddresses': [to_email]},
#             Message={
#                 'Subject': {'Data': subject, 'Charset': 'UTF-8'},
#                 'Body': {
#                     'Html': {'Data': html_body, 'Charset': 'UTF-8'}
#                 }
#             }
#         )
#         print(f"Email sent successfully to {to_email}: {response['MessageId']}")
#         return response
#     except Exception as e:
#         print(f"Error sending email via SES: {str(e)}")
#         raise
