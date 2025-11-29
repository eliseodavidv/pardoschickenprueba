# 🍗 Pardos Chicken - Sistema de Gestión de Pedidos

Sistema completo de gestión de pedidos para restaurantes implementado con arquitectura serverless en AWS. Incluye interfazweb para clientes y personal administrativo, con notificaciones automáticas por email.

## 📋 Descripción del Proyecto

Sistema multi-tenant de gestión de pedidos en tiempo real que permite:
- **Clientes**: Hacer pedidos online, ver menú y rastrear estado de entrega
- **Personal del Restaurante**: Gestionar pedidos en dashboard administrativo con timeline completo
- **Notificaciones**: Emails automáticos con diseño profesional en cada cambio de estado del pedido

## 🏗️ Arquitectura del Sistema

### Servicios AWS Utilizados

- **AWS Lambda**: Funciones serverless para toda la lógica de negocio
- **Amazon API Gateway**: API REST para comunicación frontend-backend
- **Amazon DynamoDB**: Base de datos NoSQL para almacenamiento persistente
- **Amazon EventBridge**: Bus de eventos para arquitectura event-driven
- **AWS Step Functions**: Orquestación de workflows de pedidos
- **AWS Amplify**: Hosting y despliegue continuo del frontend
- **Amazon SES**: Servicio de emails (preparado para producción)

### Patrón de Arquitectura

El sistema implementa **Event-Driven Architecture (EDA)** donde cada acción genera eventos que disparan automáticamente otros procesos:

```
Cliente → API Gateway → Lambda → DynamoDB
                         ↓
                    EventBridge → Lambda Email
                         ↓
                    Step Functions (Workflow)
```

## 📁 Estructura del Proyecto

```
pardoschickenprueba/
├── frontend/                    # Aplicaciones web
│   ├── client/                 # Interfaz para clientes
│   │   ├── index.html         # Página principal de pedidos
│   │   ├── app.js             # Lógica del cliente
│   │   └── config.js          # Configuración de API
│   └── restaurant/            # Dashboard administrativo
│       ├── index.html         # Login y dashboard
│       ├── app.js             # Gestión de pedidos
│       └── styles.css         # Estilos del dashboard
│
├── backend/src/               # Backend serverless
│   ├── ms_tenants_menu/      # Microservicio de menú
│   │   ├── get_tenants.py
│   │   ├── get_menu.py
│   │   └── put_menu_item.py
│   │
│   ├── ms_orders/            # Microservicio de pedidos
│   │   ├── create_order.py   # Crear nuevo pedido
│   │   ├── get_order.py      # Consultar pedido
│   │   ├── list_orders.py    # Listar pedidos
│   │   └── get_order_metrics.py  # Métricas de tiempo
│   │
│   ├── ms_workflow/          # Microservicio de workflow
│   │   ├── update_order_step.py      # Actualizar estado
│   │   ├── get_dashboard_summary.py  # Dashboard data
│   │   ├── check_order_status.py     # Step Functions
│   │   └── calculate_order_metrics.py
│   │
│   ├── ms_notifications/     # Microservicio de emails
│   │   └── send_email_notification.py  # Envío de emails
│   │
│   ├── common/               # Utilidades compartidas
│   │   ├── db.py            # Conexiones a DynamoDB
│   │   └── events.py        # Publicación a EventBridge
│   │
│   └── serverless.yml       # Infraestructura como código
│
├── populate_menu.sh          # Script para poblar menú inicial
├── test_email_notifications.sh  # Script de prueba de emails
└── README.md                # Este archivo
```

## 🚀 Funcionalidades Principales

### 1. Sistema de Pedidos Online

**Para Clientes:**
- Ver menú completo de productos con precios organizados por categorías
- Agregar productos al carrito con controles de cantidad (+/-)
- Formulario de pedido con validación de datos de contacto
- Confirmación inmediata con ID único de pedido
- Rastreo en tiempo real del estado del pedido
- Timeline visual del progreso de entrega con timestamps

**Estados del Pedido:**
1. **RECEIVED** - Pedido recibido y confirmado
2. **COOKING** - En preparación en cocina
3. **PACKING** - Empacando para entrega
4. **DELIVERING** - En camino al cliente
5. **DELIVERED** - Entregado al cliente

### 2. Dashboard Administrativo

**Para Personal del Restaurante:**
- Vista general con estadísticas en tiempo real actualizadas automáticamente
- Contadores de pedidos por estado (activos vs completados)
- Métricas de tiempos promedio por cada fase del workflow
- Sistema de filtrado de pedidos por estado actual
- Tarjetas de pedido interactivas y clickeables
- Indicadores visuales de urgencia basados en tiempo transcurrido
- Botones de acción rápida para cambiar estados con un solo click
- Timeline detallada de cada pedido con todos los eventos
- Información completa del cliente (nombre, dirección, teléfono, email)
- Vista expandible de items del pedido con cantidades

**Roles del Personal:**
- **KITCHEN_STAFF**: Cocineros (inician proceso de cocción)
- **PACKER**: Despachadores (empacan pedidos listos)
- **DELIVERY_DRIVER**: Repartidores (entregan pedidos al cliente)

### 3. Sistema de Notificaciones por Email

**Características:**
- Email automático de confirmación al crear pedido
- Email automático en cada cambio de estado del pedido
- Diseño profesional responsive compatible con todos los dispositivos
- 5 plantillas HTML diferentes con diseño único según el estado
- Branding corporativo consistente de Pardos Chicken
- Timeline visual del progreso incluido en cada email
- Botón "Rastrear mi Pedido" con link directo a la aplicación
- Información completa del pedido y estado actual
- Colores y emojis específicos para cada fase

**Emails enviados:**
- ✅ RECEIVED: "¡Pedido Confirmado!" (Verde #06d6a0)
- 👨‍🍳 COOKING: "¡Ya estamos preparando tu pedido!" (Naranja #f77f00)
- 📦 PACKING: "¡Empacando tu pedido!" (Azul #3a86ff)
- 🚗 DELIVERING: "¡Tu pedido viene en camino!" (Morado #8338ec)
- 🎉 DELIVERED: "¡Pedido Entregado!" (Verde #06d6a0)

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.11**: Lenguaje de programación principal
- **Serverless Framework**: Infrastructure as Code (IaC) para deployment
- **Boto3**: SDK oficial de AWS para Python
- **UUID**: Generación de identificadores únicos
- **JSON**: Formato de serialización de datos

### Frontend
- **HTML5**: Estructura semántica de las páginas
- **CSS3**: Estilos modernos con gradientes y animaciones
- **JavaScript (Vanilla)**: Sin frameworks, JavaScript puro para máximo control
- **Fetch API**: Llamadas HTTP asíncronas al backend
- **LocalStorage**: Persistencia de sesión del usuario

### DevOps
- **Git**: Control de versiones distribuido
- **AWS CLI**: Herramienta de línea de comandos para AWS
- **Bash Scripts**: Automatización de tareas repetitivas

## 📦 Base de Datos - DynamoDB

### Tablas Implementadas

#### 1. **Tenants** (Multi-tenancy)
Permite que el sistema soporte múltiples restaurantes en la misma infraestructura.

```javascript
{
  "tenant_id": "pardos-chicken",          // Partition Key
  "name": "Pardos Chicken",
  "contact_email": "contacto@pardoschicken.com",
  "active": true,
  "created_at": "2025-01-28T00:00:00Z"
}
```

#### 2. **MenuItems** (Productos del Menú)
Almacena todos los productos disponibles para pedidos.

```javascript
{
  "tenant_id": "pardos-chicken",          // Partition Key
  "product_id": "uuid-123-456",           // Sort Key
  "name": "Pollo Entero",
  "price": 45.00,
  "category": "Pollo a la Brasa",
  "description": "Pollo a la brasa completo con papas",
  "available": true
}
```

#### 3. **Orders** (Pedidos)
Almacena todos los pedidos con tracking completo de tiempos y personal.

```javascript
{
  "tenant_id": "pardos-chicken",          // Partition Key
  "order_id": "uuid-789-012",             // Sort Key
  "status": "COOKING",
  "items": [
    {"product_id": "uuid-123", "name": "Pollo Entero", "quantity": 1},
    {"product_id": "uuid-456", "name": "Papas Fritas", "quantity": 2}
  ],
  "customer_name": "Juan Pérez",
  "customer_email": "juan@example.com",
  "customer_phone": "+51999999999",
  "customer_address": "Av. Principal 123, Lima",
  "created_at": "2025-01-28T10:00:00Z",
  "updated_at": "2025-01-28T10:15:00Z",

  // Timestamps de cada fase
  "cooking_started_at": "2025-01-28T10:05:00Z",
  "cooking_by": "Chef Carlos",
  "packing_started_at": "2025-01-28T10:20:00Z",
  "packing_by": "María López"
}
```

#### 4. **OrderEvents** (Eventos de Pedidos)
Registro completo de todos los cambios de estado para auditoría y timeline.

```javascript
{
  "order_id": "uuid-789-012",             // Partition Key
  "ts": "2025-01-28T10:15:00Z",          // Sort Key
  "status": "COOKING",
  "by": "Chef Carlos",
  "by_role": "KITCHEN_STAFF",
  "previous_status": "RECEIVED",
  "tenant_id": "pardos-chicken"
}
```

## 🔄 Flujo de Eventos (Event-Driven)

### 1. Creación de Pedido

```
Cliente completa formulario y envía pedido
    ↓
Frontend POST /tenants/pardos-chicken/orders
    ↓
Lambda: create_order.py
    ↓
1. Valida datos del pedido
2. Genera UUID único para order_id
3. Guarda en DynamoDB tabla Orders
4. Registra evento inicial en OrderEvents
5. Publica evento a EventBridge
    ↓
EventBridge recibe evento "order.created"
    ↓
Dispara 2 procesos en paralelo:
  ├─> Step Functions: Inicia workflow de monitoreo
  └─> Lambda Email: Envía confirmación al cliente
    ↓
Cliente recibe:
  - Respuesta HTTP 201 con order_id
  - Email de confirmación "¡Pedido Confirmado!"
```

### 2. Actualización de Estado por Staff

```
Staff del restaurante actualiza estado desde dashboard
    ↓
Frontend POST /tenants/pardos-chicken/orders/{orderId}/step
  Body: { "status": "COOKING", "attended_by": "Chef Carlos", "role": "KITCHEN_STAFF" }
    ↓
Lambda: update_order_step.py
    ↓
1. Obtiene pedido actual de DynamoDB
2. Valida que la transición sea permitida (RECEIVED → COOKING)
3. Valida que el rol sea el esperado (KITCHEN_STAFF)
4. Actualiza estado en tabla Orders
5. Guarda campos cooking_started_at y cooking_by
6. Registra evento en tabla OrderEvents
7. Publica evento "order.updated" a EventBridge
    ↓
EventBridge recibe evento "order.updated"
    ↓
Lambda Email: send_email_notification.py
    ↓
1. Extrae datos del evento (customer_email, status, order_id)
2. Genera HTML profesional específico para estado "COOKING"
3. En producción: Envía email vía Amazon SES
4. En desarrollo: Registra email simulado en logs
    ↓
Cliente recibe email: "👨‍🍳 ¡Ya estamos preparando tu pedido!"
```

### 3. Workflow Automatizado con Step Functions

```
EventBridge "order.created" → Inicia Step Function
    ↓
State Machine: pardos-order-workflow
    ↓
1. LogOrderReceived (Pass State)
    ↓
2. CheckInitialStatus (Lambda)
   - Verifica estado actual del pedido
    ↓
3. WaitForCooking (Wait 5 minutos)
    ↓
4. CheckCookingStatus (Lambda)
   - ¿Ya pasó a COOKING?
    ├─> NO: Volver a esperar 5 minutos
    └─> SÍ: Continuar
    ↓
5. WaitForPacking (Wait 3 minutos)
    ↓
6. CheckPackingStatus (Lambda)
    ↓
7. WaitForDelivery (Wait 10 minutos)
    ↓
8. CheckDeliveryStatus (Lambda)
    ↓
9. IsDelivered? (Choice State)
    ├─> NO: Volver a esperar
    └─> SÍ: Continuar
    ↓
10. CalculateFinalMetrics (Lambda)
    - Calcula tiempo total del pedido
    - Calcula tiempo por cada fase
    - Actualiza métricas en DynamoDB
    ↓
11. WorkflowCompleted (Succeed State)
```

## 📊 Métricas y Tiempos

El sistema calcula automáticamente:

### Métricas por Pedido
- **Tiempo total del pedido**: Desde creación hasta entrega completa
- **Tiempo por fase**:
  - Tiempo en cocina (RECEIVED → COOKING → PACKING)
  - Tiempo de empaque (PACKING → DELIVERING)
  - Tiempo de entrega (DELIVERING → DELIVERED)
- **Tiempo estimado restante**: Basado en promedios históricos

### Métricas Agregadas del Día
- **Pedidos completados**: Total de pedidos en estado DELIVERED
- **Pedidos activos**: Total de pedidos en proceso
- **Tiempo promedio total**: Promedio de tiempo de todos los pedidos completados
- **Tiempo promedio por fase**:
  - Promedio de tiempo en cocina
  - Promedio de tiempo de empaque
  - Promedio de tiempo de entrega

## 🔐 Seguridad y Validaciones

### Validaciones de Negocio

#### 1. Transiciones de Estado Válidas
Solo se permiten transiciones específicas en el workflow:

```python
VALID_TRANSITIONS = {
    "RECEIVED": ["COOKING"],
    "COOKING": ["PACKING"],
    "PACKING": ["DELIVERING"],
    "DELIVERING": ["DELIVERED"],
    "DELIVERED": []  # Estado final
}
```

Si se intenta una transición inválida (ej: RECEIVED → DELIVERING), el sistema retorna error 400.

#### 2. Roles del Personal Esperados
Cada fase debe ser manejada por el rol apropiado:

```python
EXPECTED_ROLES = {
    "COOKING": "KITCHEN_STAFF",      # Solo cocineros
    "PACKING": "PACKER",             # Solo despachadores
    "DELIVERING": "DELIVERY_DRIVER", # Solo repartidores
    "DELIVERED": "DELIVERY_DRIVER"   # Solo repartidores
}
```

Si el rol no coincide, el sistema genera un warning pero permite la operación.

#### 3. Validación de Datos de Entrada
- **Pedidos**: items requerido y no vacío
- **Email**: formato válido HTML5
- **Cantidades**: números positivos
- **IDs**: formato UUID válido

### Permisos IAM

El sistema utiliza **LabRole** de AWS Academy con permisos para:
- **DynamoDB**: GetItem, PutItem, UpdateItem, Query, Scan
- **EventBridge**: PutEvents en el bus personalizado
- **Lambda**: InvokeFunction para Step Functions
- **Step Functions**: StartExecution de state machines
- **CloudWatch**: CreateLogGroup, CreateLogStream, PutLogEvents

## 🚀 Deployment

### Prerrequisitos

1. **AWS CLI** configurado con credenciales activas
2. **Serverless Framework** versión 3.x o superior
3. **Node.js** versión 16 o superior
4. **Python** versión 3.11

### Instalación de Herramientas

```bash
# Instalar Serverless Framework globalmente
npm install -g serverless

# Verificar instalación
serverless --version
```

### Paso 1: Configurar Credenciales AWS

```bash
# En AWS Academy Learner Lab, obtener credenciales de:
# AWS Details → AWS CLI → Show

# Copiar y ejecutar los comandos export en tu terminal
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."

# Verificar configuración
aws sts get-caller-identity
```

**Nota**: Las credenciales de AWS Academy expiran después de ~4 horas. Deberás renovarlas si trabajas por períodos prolongados.

### Paso 2: Desplegar Backend

```bash
# Navegar al directorio del backend
cd backend/src

# Instalar dependencias de Serverless
npm install

# Desplegar toda la infraestructura
serverless deploy --stage dev

# Output esperado:
# ✓ Service deployed to stack dev-pardos-orders
#
# endpoints:
#   GET - https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com/tenants
#   POST - https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com/tenants/{tenantId}/orders
#   GET - https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com/tenants/{tenantId}/orders/{orderId}
#   ...
#
# functions:
#   createOrder: dev-createOrder
#   updateOrderStep: dev-updateOrderStep
#   sendEmailNotification: dev-sendEmailNotification
#   ...
```

**IMPORTANTE**: Guarda la URL base del API Gateway (https://xxx.execute-api.us-east-1.amazonaws.com)

### Paso 3: Poblar Menú Inicial

El sistema necesita productos en el menú para funcionar. Ejecuta:

```bash
# Desde la raíz del proyecto
chmod +x populate_menu.sh
./populate_menu.sh
```

Este script crea 19 productos organizados en 6 categorías:
- **Pollos** (6 productos): Pollo entero, 1/2 pollo, 1/4 pollo, etc.
- **Parrillas** (4 productos): Parrilla mixta, anticuchos, etc.
- **Entradas** (3 productos): Tequeños, papa a la huancaína, etc.
- **Ensaladas** (3 productos): Ensalada fresca, ensalada cesar, etc.
- **Bebidas** (2 productos): Inca Kola, Chicha morada
- **Postres** (1 producto): Suspiro limeño

### Paso 4: Configurar URLs en Frontend

Actualizar la URL del API en ambos frontends:

#### `frontend/client/config.js`
```javascript
const API_CONFIG = {
    baseURL: 'https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com', // ← Tu URL aquí
    tenantId: 'pardos-chicken'
};
```

#### `frontend/restaurant/config.js`
```javascript
const API_CONFIG = {
    baseURL: 'https://c1qx4jzzy2.execute-api.us-east-1.amazonaws.com', // ← Tu URL aquí
    tenantId: 'pardos-chicken'
};
```

### Paso 5: Desplegar Frontend en AWS Amplify

#### Opción A: Desde AWS Console (Recomendado)

1. Ir a AWS Console → AWS Amplify
2. Click en "New app" → "Host web app"
3. Conectar con repositorio de GitHub
4. AWS detectará automáticamente `amplify.yml`
5. Confirmar configuración de build
6. Deploy automático se iniciará

#### Opción B: Deployment Manual

```bash
# Commit de cambios de configuración
git add frontend/client/config.js frontend/restaurant/config.js
git commit -m "Update API URLs"
git push

# Amplify detectará el push y desplegará automáticamente
```

**Resultado esperado**:
- URL Cliente: `https://main.xxxxx.amplifyapp.com/client/`
- URL Restaurant: `https://main.xxxxx.amplifyapp.com/restaurant/`

### Paso 6: Verificar Deployment

```bash
# Verificar que las Lambda Functions estén activas
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `dev-`)].FunctionName'

# Verificar que las tablas de DynamoDB existan
aws dynamodb list-tables --query 'TableNames[?starts_with(@, `dev-`)]'

# Verificar que EventBridge esté configurado
aws events list-rules --event-bus-name dev-pardos-orders-bus
```

## 🧪 Pruebas

### Probar Sistema de Emails

Ejecuta el script de prueba automatizado:

```bash
chmod +x test_email_notifications.sh
./test_email_notifications.sh
```

Este script:
1. Crea un pedido de prueba con email
2. Verifica que se guardó correctamente en DynamoDB
3. Simula todas las transiciones de estado (RECEIVED → COOKING → PACKING → DELIVERING → DELIVERED)
4. Muestra instrucciones para ver los logs de los emails

### Ver Logs de Emails en CloudWatch

```bash
cd backend/src
serverless logs -f sendEmailNotification --tail
```

Deberías ver en los logs:
```
========================================
📧 EMAIL NOTIFICATION (SIMULADO)
========================================
Para: cliente@example.com
Asunto: ✅ Pardos Chicken - ¡Pedido Confirmado!
Tipo de evento: order.created
Estado del pedido: RECEIVED
ID del pedido: 7002c010-3ddc-4dae-85c5-2c11c5e4a971
========================================
```

### Probar API Manualmente con cURL

#### Crear un Pedido:
```bash
curl -X POST "https://TU_API_URL/tenants/pardos-chicken/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": "1", "name": "Pollo Entero", "quantity": 1},
      {"product_id": "4", "name": "Papas Fritas", "quantity": 2}
    ],
    "customer_name": "Juan Pérez",
    "customer_email": "juan@example.com",
    "customer_phone": "+51999999999",
    "customer_address": "Av. Principal 123, Lima"
  }'
```

#### Consultar un Pedido:
```bash
curl "https://TU_API_URL/tenants/pardos-chicken/orders/{order_id}"
```

#### Actualizar Estado:
```bash
curl -X POST "https://TU_API_URL/tenants/pardos-chicken/orders/{order_id}/step" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COOKING",
    "attended_by": "Chef Carlos",
    "role": "KITCHEN_STAFF"
  }'
```

## 📈 Monitoreo y Logs

### CloudWatch Logs

Cada Lambda function tiene su propio Log Group en CloudWatch:

- `/aws/lambda/dev-createOrder`
- `/aws/lambda/dev-getOrder`
- `/aws/lambda/dev-updateOrderStep`
- `/aws/lambda/dev-sendEmailNotification`
- `/aws/lambda/dev-getDashboardSummary`
- `/aws/lambda/dev-checkOrderStatus`
- `/aws/lambda/dev-calculateOrderMetrics`

### Comandos Útiles para Ver Logs

```bash
# Ver logs de función específica en tiempo real
serverless logs -f createOrder --tail

# Ver logs de función de emails
serverless logs -f sendEmailNotification --tail

# Ver logs de los últimos 30 minutos
serverless logs -f updateOrderStep --startTime 30m

# Buscar errores en los logs
serverless logs -f createOrder | grep ERROR
```

### Métricas en CloudWatch

Métricas disponibles para cada Lambda:
- **Invocations**: Total de invocaciones
- **Duration**: Tiempo de ejecución (ms)
- **Errors**: Número de errores
- **Throttles**: Invocaciones limitadas por concurrencia
- **ConcurrentExecutions**: Ejecuciones simultáneas

### EventBridge Metrics

- **Invocations**: Total de eventos procesados
- **FailedInvocations**: Eventos que fallaron
- **TriggeredRules**: Reglas que se dispararon
- **MatchedEvents**: Eventos que coincidieron con patrones

## 🎨 Personalización

### Modificar Diseño de Emails

Editar `backend/src/ms_notifications/send_email_notification.py`:

#### Cambiar Colores y Textos por Estado (líneas 89-120):
```python
status_info = {
    'RECEIVED': {
        'emoji': '✅',
        'title': '¡Pedido Confirmado!',
        'message': 'Hemos recibido tu pedido correctamente',
        'color': '#06d6a0'  # Cambiar color aquí
    },
    'COOKING': {
        'emoji': '👨‍🍳',
        'title': 'Tu título personalizado',  # Personalizar
        'message': 'Tu mensaje personalizado',
        'color': '#f77f00'
    },
    # ... agregar más estados si es necesario
}
```

#### Modificar HTML del Email (líneas 146-279):
```python
def generate_email_html(customer_name, order_id, title, message, status, color, emoji):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <!-- Agregar estilos personalizados aquí -->
    </head>
    <body>
        <!-- Modificar estructura del email -->
    </body>
    </html>
    """
```

### Agregar Nuevos Productos al Menú

Puedes usar el script `populate_menu.sh` como referencia para agregar productos:

```bash
aws dynamodb put-item \
    --table-name dev-MenuItems \
    --item '{
        "tenant_id": {"S": "pardos-chicken"},
        "product_id": {"S": "nuevo-prod-001"},
        "name": {"S": "Nuevo Producto"},
        "price": {"N": "35.00"},
        "category": {"S": "Categoría Nueva"},
        "description": {"S": "Descripción del producto"},
        "available": {"BOOL": true}
    }'
```

### Modificar Tiempos de Espera en Workflow

Editar `backend/src/serverless.yml` (líneas 260-390):

```yaml
"WaitForCooking": {
  "Type": "Wait",
  "Seconds": 300,  # Cambiar de 300 (5 min) a lo que necesites
  "Next": "CheckCookingStatus"
},
"WaitForPacking": {
  "Type": "Wait",
  "Seconds": 180,  # Cambiar de 180 (3 min) a lo que necesites
  "Next": "CheckPackingStatus"
}
```

## 🔧 Troubleshooting

### Error: "Internal Server Error" (500)

**Síntomas**: La API retorna 500 al crear o actualizar pedidos.

**Diagnóstico**:
```bash
# Ver logs de la función específica
serverless logs -f createOrder --tail
```

**Causas comunes**:
1. Error en la lógica de Python (revisar stack trace en logs)
2. Permisos insuficientes para acceder a DynamoDB
3. Formato de datos incorrecto en el request

**Solución**:
1. Verificar logs de CloudWatch para identificar el error exacto
2. Validar que los permisos de LabRole incluyan DynamoDB
3. Verificar formato JSON del request body

### Error: "Credentials Expired"

**Síntomas**: `serverless deploy` falla con error de credenciales.

**Causa**: Las credenciales de AWS Academy expiran después de ~4 horas.

**Solución**:
```bash
# 1. Ir a AWS Academy Learner Lab
# 2. Click en "AWS Details"
# 3. Click en "Show" junto a "AWS CLI"
# 4. Copiar y ejecutar los comandos export

export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."

# 5. Verificar que funciona
aws sts get-caller-identity
```

### Frontend No Se Conecta al Backend

**Síntomas**: Errores de CORS o "Network Error" en consola del navegador.

**Diagnóstico**:
1. Abrir DevTools del navegador (F12)
2. Ir a pestaña Network
3. Ver detalles del request fallido

**Causas comunes**:
1. URL del API incorrecta en `config.js`
2. CORS no habilitado en API Gateway
3. Backend no desplegado correctamente

**Solución**:
```bash
# 1. Verificar que CORS esté habilitado en serverless.yml
provider:
  httpApi:
    cors: true  # ← Debe estar presente

# 2. Verificar URL en config.js
# Debe coincidir exactamente con la URL de API Gateway

# 3. Redesplegar backend si es necesario
cd backend/src
serverless deploy --stage dev
```

### Emails No Se Envían

**En AWS Academy**:
Amazon SES no está disponible en Learner Lab. Los emails solo se **simulan** en los logs de CloudWatch.

**Solución para AWS Academy**:
```bash
# Ver logs para confirmar que los emails se están generando
serverless logs -f sendEmailNotification --tail

# Buscar "📧 EMAIL NOTIFICATION (SIMULADO)"
```

**Para Activar SES en Producción**:

1. Verificar email o dominio en Amazon SES:
```bash
aws ses verify-email-identity --email-address noreply@pardoschicken.com
```

2. Descomentar código en `send_email_notification.py`:
```python
# Líneas 5-7: Importar boto3
import boto3
ses_client = boto3.client('ses', region_name='us-east-1')

# Líneas 41-46: Habilitar envío real
send_email_ses(
    to_email=customer_email,
    subject=email_subject,
    html_body=email_html
)
```

3. Redesplegar:
```bash
serverless deploy --stage prod
```

### Pedidos No Aparecen en Dashboard

**Síntomas**: Dashboard muestra "No hay pedidos activos" aunque existen pedidos.

**Diagnóstico**:
```bash
# Verificar que hay pedidos en DynamoDB
aws dynamodb scan --table-name dev-Orders --max-items 5

# Ver logs del dashboard
serverless logs -f getDashboardSummary --tail
```

**Causas comunes**:
1. tenant_id incorrecto en la consulta
2. Error al cargar datos del dashboard
3. JavaScript error en el frontend

**Solución**:
1. Verificar que tenant_id sea "pardos-chicken" en ambos lados
2. Revisar consola del navegador (F12) para errores JS
3. Verificar que `loadDashboard()` se ejecute correctamente

## 📚 Recursos Adicionales

### Documentación Oficial de AWS
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/)
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/)

### Serverless Framework
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs)
- [AWS Provider Guide](https://www.serverless.com/framework/docs/providers/aws/)
- [Serverless Examples](https://github.com/serverless/examples)

### Tutoriales y Guías
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [EventBridge Patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [Step Functions ASL](https://states-language.net/spec.html)

## 🎓 Conceptos Cloud Computing Implementados

Este proyecto demuestra dominio de los siguientes conceptos:

### 1. Arquitectura Serverless
- **Sin servidores que gestionar**: Todo corre en Lambda functions
- **Escalado automático**: AWS escala según demanda
- **Pay-per-use**: Solo pagas por las invocaciones reales
- **Alta disponibilidad**: AWS maneja redundancia

### 2. Event-Driven Architecture (EDA)
- **Eventos como mensajes**: Comunicación desacoplada entre servicios
- **Publishers y Subscribers**: EventBridge conecta productores con consumidores
- **Event Sourcing**: Todos los cambios quedan registrados como eventos
- **Procesamiento asíncrono**: Notificaciones sin bloquear el flujo principal

### 3. Microservicios
- **Servicios especializados**: ms_orders, ms_workflow, ms_notifications
- **Desacoplamiento**: Cada servicio puede desplegarse independientemente
- **Single Responsibility**: Cada microservicio tiene una responsabilidad clara
- **APIs bien definidas**: Contratos de comunicación mediante API Gateway

### 4. Infrastructure as Code (IaC)
- **Serverless Framework**: Todo definido en `serverless.yml`
- **Versionamiento**: Infraestructura en Git junto con el código
- **Reproducibilidad**: Mismo stack en dev, staging y prod
- **Deployment automatizado**: Un comando despliega todo

### 5. NoSQL Databases
- **DynamoDB**: Base de datos totalmente administrada
- **Partition Keys**: Distribución eficiente de datos
- **Sort Keys**: Queries eficientes de ranges
- **Escalabilidad horizontal**: Automática según demanda

### 6. API Design
- **RESTful**: Endpoints semánticos y verbos HTTP correctos
- **CORS**: Configurado para permitir llamadas cross-origin
- **JSON**: Formato estándar de comunicación
- **HTTP Status Codes**: Uso correcto (200, 201, 400, 404, 500)

### 7. State Machines
- **AWS Step Functions**: Orquestación visual de workflows
- **Amazon States Language**: Definición declarativa del flujo
- **Error Handling**: Reintentos y fallbacks automáticos
- **Monitoring**: Visualización del estado en tiempo real

### 8. Asynchronous Processing
- **EventBridge**: Bus de eventos asíncrono
- **Lambda Async Invocation**: Invocaciones no bloqueantes
- **Eventual Consistency**: Modelo eventual de consistencia
- **Message Queuing**: Eventos como cola de mensajes

### 9. Multi-tenancy
- **Aislamiento de datos**: Cada restaurante tiene sus propios datos
- **Partition Keys**: tenant_id como partition key
- **Escalabilidad**: Soporte para N restaurantes sin cambios
- **Seguridad**: Filtrado automático por tenant

### 10. DevOps y CI/CD
- **Git**: Control de versiones distribuido
- **Automated Deployment**: AWS Amplify para frontend
- **Logging**: CloudWatch Logs para debugging
- **Monitoring**: CloudWatch Metrics para observability

## 💡 Lecciones Técnicas Aprendidas

### Sobre Arquitectura Serverless

**Ventajas**:
- No hay servidores que administrar ni parchear
- Escalado automático sin configuración
- Costos basados solo en uso real
- Alta disponibilidad por defecto

**Consideraciones**:
- **Cold starts**: Primera invocación puede ser lenta (~1-2 segundos)
- **Límites**: 15 minutos max de ejecución en Lambda
- **Memoria**: Configurar correctamente para balance costo/performance
- **Concurrency**: Límites de ejecuciones simultáneas

### Sobre DynamoDB

**Decisiones de Diseño**:
- **Partition Key = tenant_id**: Permite aislar datos por restaurante
- **Sort Key = order_id/product_id**: Permite queries eficientes
- **Denormalización**: Guardar datos duplicados para evitar joins
- **Timestamps en ISO**: Facilita sorting y comparaciones

**Best Practices Aplicadas**:
- Usar UUID para IDs únicos globalmente
- Incluir tenant_id en todas las tablas para multi-tenancy
- Timestamps en UTC para evitar problemas de zonas horarias
- Pay-per-request billing para workloads impredecibles

### Sobre EventBridge

**Patrones Implementados**:
- **Publisher-Subscriber**: Múltiples consumers del mismo evento
- **Event Routing**: Rules que filtran eventos específicos
- **Event Transformation**: InputTransformer para Step Functions
- **Retry Policies**: Configuración de reintentos automáticos

**Ventajas**:
- Desacopla completamente servicios
- Fácil agregar nuevos consumers sin modificar publishers
- Logs automáticos de todos los eventos
- Integración nativa con múltiples targets

### Sobre Frontend Sin Frameworks

**Decisión de usar JavaScript Vanilla**:
- **Pros**:
  - No hay dependencias que mantener
  - Bundle size mínimo (solo código propio)
  - Control total sobre el código
  - Más fácil de debuggear
  - No hay learning curve de framework

- **Contras**:
  - Más código manual (sin reactivity)
  - No hay state management sofisticado
  - Manipulación directa del DOM

**Cuándo usar Vanilla JS**:
- Aplicaciones pequeñas/medianas
- Proyectos académicos/learning
- Cuando el performance es crítico
- Cuando quieres entender los fundamentos

## 🔮 Mejoras Futuras Posibles

### Corto Plazo (1-2 semanas)
- [ ] Activar Amazon SES para emails reales en producción
- [ ] Implementar autenticación con Amazon Cognito
- [ ] Agregar panel de administración de menú (CRUD completo)
- [ ] Implementar sistema de búsqueda de productos
- [ ] Agregar imágenes de productos (almacenadas en S3)

### Mediano Plazo (1-2 meses)
- [ ] WebSockets (API Gateway WebSocket) para updates en tiempo real
- [ ] Sistema de pagos online con Stripe o PayPal
- [ ] Cálculo automático de precios totales con impuestos
- [ ] Sistema de cupones y descuentos promocionales
- [ ] Ratings y reviews de productos por clientes
- [ ] Historial completo de pedidos del cliente

### Largo Plazo (3-6 meses)
- [ ] Aplicación móvil nativa con React Native o Flutter
- [ ] Tracking GPS en tiempo real del repartidor
- [ ] Integración con sistemas de punto de venta (POS)
- [ ] Machine Learning para predicción de demanda
- [ ] Sistema de recomendaciones personalizadas
- [ ] Analytics dashboard con QuickSight
- [ ] Multi-idioma (i18n) para internacionalización
- [ ] Sistema de fidelización de clientes

## 📝 Notas Técnicas Importantes

### Sobre AWS Academy Learner Lab

**Limitaciones**:
- Credenciales expiran cada ~4 horas
- Amazon SES no disponible (sandbox restrictions)
- Algunos servicios pueden tener límites reducidos
- No persistence entre sesiones de lab

**Recomendaciones**:
- Siempre guardar el código en Git
- Documentar URLs de APIs y recursos
- Tomar screenshots de recursos desplegados
- Exportar datos importantes de DynamoDB

### Sobre Costos en AWS

**Servicios con Free Tier Generoso**:
- Lambda: 1M requests/mes gratis
- DynamoDB: 25GB storage gratis
- API Gateway: 1M requests/mes gratis
- EventBridge: Todos los eventos custom gratis

**Costos a Considerar en Producción**:
- DynamoDB: $0.25 per million write requests
- Lambda: $0.20 per million requests
- Step Functions: $0.025 per 1000 transitions
- SES: $0.10 per 1000 emails

**Optimizaciones**:
- Usar PAY_PER_REQUEST en DynamoDB
- Configurar memoria óptima en Lambda
- Implementar caching cuando sea posible
- Usar compression en API Gateway


**© 2025 Pardos Chicken - Sistema de Gestión de Pedidos**
Proyecto de Cloud Computing - Arquitectura Serverless en AWS

