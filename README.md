# 🍗 Pardos Chicken - Sistema de Gestión de Pedidos

Sistema completo de gestión de pedidos para restaurantes usando arquitectura serverless en AWS. Incluye interfaz web para clientes y personal del restaurante, con notificaciones automáticas por email vía SendGrid.

## 📋 Qué hace este sistema

Este proyecto permite gestionar pedidos online para restaurantes de forma completamente serverless. Los clientes pueden ver el menú, hacer pedidos y recibir notificaciones por email en cada etapa del proceso. El personal del restaurante tiene un dashboard para gestionar todos los pedidos activos y ver estadísticas en tiempo real.

**Características principales:**
- Los clientes hacen pedidos desde la web y reciben emails automáticos cuando cambia el estado
- El personal actualiza el estado de los pedidos desde un dashboard (recibido → cocinando → empacando → en camino → entregado)
- Todo funciona con AWS Lambda, DynamoDB y EventBridge (sin servidores que mantener)
- Emails profesionales con SendGrid que se envían automáticamente
- Tracking completo de tiempos y métricas de cada pedido

## 🏗️ Cómo está construido

### Servicios AWS que usamos

- **AWS Lambda**: Toda la lógica del backend corre aquí (crear pedidos, actualizar estados, etc.)
- **API Gateway**: El frontend se comunica con el backend a través de esta API REST
- **DynamoDB**: Base de datos NoSQL donde guardamos todo (menú, pedidos, eventos)
- **EventBridge**: Cuando pasa algo (se crea un pedido, cambia de estado), se disparan eventos automáticos
- **Step Functions**: Workflow automatizado que monitorea el progreso de cada pedido
- **AWS Amplify**: Hosting del frontend con deploy automático desde GitHub
- **SendGrid**: Servicio de emails transaccionales para notificaciones a clientes

### Arquitectura Event-Driven

Todo el sistema funciona con eventos. Cuando se crea un pedido o cambia de estado, se publica un evento que dispara automáticamente otros procesos:

```
Cliente hace pedido → API Gateway → Lambda crea orden → DynamoDB
                                         ↓
                                    EventBridge publica evento
                                         ↓
                          ┌──────────────┴──────────────┐
                          ↓                             ↓
                    Step Functions               Lambda de Emails
                  (monitorea workflow)         (envía notificación)
```

## 📁 Estructura del proyecto

```
pardoschickenprueba/
├── frontend/
│   ├── client/                    # Interfaz para clientes
│   │   ├── index.html            # Página de pedidos
│   │   ├── app.js                # Lógica (carrito, menú, tracking)
│   │   ├── config.js             # URL del API
│   │   └── styles.css            # Estilos con glassmorphism
│   │
│   └── restaurant/               # Dashboard del restaurante
│       ├── index.html           # Login y dashboard
│       ├── app.js               # Gestión de pedidos
│       ├── config.js            # URL del API
│       └── styles.css           # Estilos del dashboard
│
├── backend/src/
│   ├── ms_tenants_menu/         # Microservicio del menú
│   │   ├── get_tenants.py
│   │   ├── get_menu.py
│   │   └── put_menu_item.py
│   │
│   ├── ms_orders/               # Microservicio de pedidos
│   │   ├── create_order.py      # POST /orders
│   │   ├── get_order.py         # GET /orders/{id}
│   │   ├── list_orders.py       # GET /orders
│   │   └── get_order_metrics.py # Métricas de tiempos
│   │
│   ├── ms_workflow/             # Microservicio de workflow
│   │   ├── update_order_step.py       # Actualizar estado
│   │   ├── get_dashboard_summary.py   # Data del dashboard
│   │   ├── check_order_status.py      # Para Step Functions
│   │   └── calculate_order_metrics.py # Calcular tiempos
│   │
│   ├── ms_notifications/        # Microservicio de emails
│   │   └── send_email_notification.py # SendGrid integration
│   │
│   ├── common/                  # Utilidades compartidas
│   │   ├── db.py               # Conexiones a DynamoDB
│   │   └── events.py           # Publicar eventos a EventBridge
│   │
│   └── serverless.yml          # Infraestructura como código
│
├── populate_menu.sh             # Script para cargar menú inicial
├── test_email_notifications.sh  # Script de prueba
└── README.md
```

## 🚀 Funcionalidades

### Para clientes

El sitio web del cliente muestra el menú completo con imágenes, precios y descripciones. Los productos están organizados por categorías (pollos, parrillas, entradas, bebidas, postres). El cliente puede:

- Agregar productos al carrito con botones +/-
- Llenar un formulario con sus datos (nombre, email, teléfono, dirección)
- Recibir confirmación inmediata con un ID de pedido único
- Rastrear el estado del pedido en tiempo real
- Ver el timeline completo con los tiempos de cada fase

**Nota importante:** Si un producto no tiene imagen en la base de datos, el frontend automáticamente le asigna una imagen por defecto según el nombre del producto. Esto funciona con un diccionario de fallback en `frontend/client/app.js` que mapea nombres de productos a URLs de imágenes.

### Para el personal del restaurante

El dashboard administrativo muestra todos los pedidos activos y completados del día. El personal puede:

- Ver estadísticas en tiempo real (pedidos activos, completados, tiempos promedio)
- Filtrar pedidos por estado
- Ver información completa de cada pedido (cliente, items, dirección, teléfono, email)
- Actualizar el estado del pedido con un solo click
- Ver el timeline completo de cada pedido con timestamps

Los pedidos pasan por estos estados:
1. **RECEIVED** - Pedido recibido
2. **COOKING** - En cocina (solo personal de cocina)
3. **PACKING** - Empacando (solo despachadores)
4. **DELIVERING** - En camino (solo repartidores)
5. **DELIVERED** - Entregado

### Sistema de notificaciones por email

Cada vez que se crea o actualiza un pedido, se envía automáticamente un email al cliente vía SendGrid. Los emails tienen diseño profesional con:

- Colores y emojis específicos para cada estado
- Timeline visual del progreso del pedido
- Información del pedido (número, estado actual)
- Botón para rastrear el pedido
- Branding de Pardos Chicken

**Emails que se envían:**
- ✅ RECEIVED: "¡Pedido Confirmado!"
- 👨‍🍳 COOKING: "¡Ya estamos preparando tu pedido!"
- 📦 PACKING: "¡Empacando tu pedido!"
- 🚗 DELIVERING: "¡Tu pedido viene en camino!"
- 🎉 DELIVERED: "¡Pedido Entregado!"

## 📦 Base de datos

Usamos DynamoDB con 4 tablas:

### 1. Tenants
Soporte multi-tenant (permite usar el mismo sistema para varios restaurantes).

```javascript
{
  "tenant_id": "pardos-chicken",
  "name": "Pardos Chicken",
  "contact_email": "contacto@pardoschicken.com",
  "active": true
}
```

### 2. MenuItems
Productos del menú con precios y categorías.

```javascript
{
  "tenant_id": "pardos-chicken",
  "product_id": "uuid-123",
  "name": "Pollo Entero",
  "price": 45.00,
  "category": "Pollo a la Brasa",
  "description": "Pollo a la brasa completo con papas",
  "image_url": "https://...",  // Opcional
  "available": true
}
```

### 3. Orders
Pedidos con toda la info del cliente y tracking de tiempos.

```javascript
{
  "tenant_id": "pardos-chicken",
  "order_id": "uuid-789",
  "status": "COOKING",
  "items": [
    {"product_id": "uuid-123", "name": "Pollo Entero", "quantity": 1}
  ],
  "customer_name": "Juan Pérez",
  "customer_email": "juan@example.com",
  "customer_phone": "+51999999999",
  "customer_address": "Av. Principal 123, Lima",
  "created_at": "2025-01-28T10:00:00Z",
  "cooking_started_at": "2025-01-28T10:05:00Z",
  "cooking_by": "Chef Carlos"
}
```

### 4. OrderEvents
Log completo de todos los cambios de estado (para timeline y auditoría).

```javascript
{
  "order_id": "uuid-789",
  "ts": "2025-01-28T10:15:00Z",
  "status": "COOKING",
  "by": "Chef Carlos",
  "by_role": "KITCHEN_STAFF",
  "previous_status": "RECEIVED"
}
```

## 🔄 Cómo funciona el flujo de eventos

### Cuando un cliente hace un pedido:

```
1. Frontend envía POST /orders con los datos del pedido
   ↓
2. Lambda create_order.py:
   - Genera un UUID para el pedido
   - Guarda en DynamoDB (tabla Orders)
   - Registra evento inicial (tabla OrderEvents)
   - Publica evento "order.created" a EventBridge
   ↓
3. EventBridge dispara automáticamente:
   - Step Functions → Workflow de monitoreo
   - Lambda de emails → Envía confirmación al cliente
   ↓
4. Cliente recibe:
   - Respuesta HTTP con order_id
   - Email "¡Pedido Confirmado!" en su inbox
```

### Cuando el personal actualiza el estado:

```
1. Personal hace click en botón "Mover a Cocina"
   ↓
2. Frontend envía POST /orders/{id}/step
   Body: {"status": "COOKING", "attended_by": "Chef Carlos", "role": "KITCHEN_STAFF"}
   ↓
3. Lambda update_order_step.py:
   - Valida que la transición sea válida (RECEIVED → COOKING ✓)
   - Valida que el rol sea correcto (KITCHEN_STAFF ✓)
   - Actualiza en DynamoDB con timestamp
   - Registra en OrderEvents
   - Publica evento "order.updated" a EventBridge
   ↓
4. EventBridge dispara Lambda de emails
   ↓
5. Cliente recibe email "¡Ya estamos preparando tu pedido!"
```

## 🛠️ Tecnologías

**Backend:**
- Python 3.11
- Serverless Framework (para deploy)
- Boto3 (SDK de AWS)

**Frontend:**
- HTML5 + CSS3 + JavaScript vanilla (sin frameworks)
- Fetch API para llamadas al backend
- LocalStorage para sesión

**Servicios externos:**
- SendGrid (emails transaccionales)

## 🚀 Cómo hacer el deployment

### Prerrequisitos

1. AWS CLI configurado
2. Serverless Framework instalado (`npm install -g serverless`)
3. Node.js 16+ y Python 3.11
4. Cuenta de SendGrid (plan gratuito permite 100 emails/día)

### Paso 1: Configurar credenciales de AWS

Si usas AWS Academy:

```bash
# 1. Ve a AWS Academy → Learner Lab → Start Lab
# 2. Cuando esté verde, click en "AWS Details"
# 3. Click en "Show" en AWS CLI
# 4. Copia y pega los comandos export en tu terminal

export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."

# Verificar que funciona
aws sts get-caller-identity
```

**Importante:** Las credenciales de AWS Academy expiran cada 4 horas aproximadamente.

### Paso 2: Configurar SendGrid

1. Crea una cuenta en [SendGrid](https://signup.sendgrid.com/)
2. Verifica tu email en Settings → Sender Authentication
3. Crea una API Key en Settings → API Keys
   - Nombre: "Pardos Chicken"
   - Permisos: "Full Access" o al menos "Mail Send"
   - Guarda la API key (empieza con `SG.`)

4. Configura el email en el código:

Edita `backend/src/ms_notifications/send_email_notification.py` línea 9:
```python
SENDGRID_FROM_EMAIL = 'tu-email@ejemplo.com'  # El que verificaste en SendGrid
```

### Paso 3: Deploy del backend

```bash
cd backend/src

# Configurar la API key de SendGrid
export SENDGRID_API_KEY='SG.tu-api-key-aqui'

# Deploy
sls deploy

# Guarda la URL del API que aparece en el output
# Ejemplo: https://c9sut9oprg.execute-api.us-east-1.amazonaws.com
```

El deploy crea:
- 12 funciones Lambda
- 4 tablas DynamoDB
- 1 EventBus personalizado
- 1 Step Function (workflow)
- API Gateway con CORS habilitado

### Paso 4: Poblar el menú

```bash
# Desde la raíz del proyecto
chmod +x populate_menu.sh
./populate_menu.sh
```

Esto crea 18 productos en diferentes categorías (pollos, parrillas, entradas, bebidas, postres).

**Nota:** Si algunos productos fallan al insertar imágenes, no te preocupes. El frontend tiene un sistema de fallback que asigna imágenes automáticamente según el nombre del producto.

### Paso 5: Configurar el frontend

Actualiza la URL del API en ambos archivos de configuración:

**`frontend/client/config.js`:**
```javascript
const API_CONFIG = {
    baseURL: 'https://tu-url-aqui.execute-api.us-east-1.amazonaws.com',
    tenantId: 'pardos-chicken'
};
```

**`frontend/restaurant/config.js`:**
```javascript
const API_CONFIG = {
    baseURL: 'https://tu-url-aqui.execute-api.us-east-1.amazonaws.com',
    tenantId: 'pardos-chicken'
};
```

### Paso 6: Deploy del frontend con Amplify

1. Sube los cambios a GitHub:
```bash
git add .
git commit -m "Configure API URLs"
git push
```

2. En AWS Console:
   - Ve a AWS Amplify
   - Click "New app" → "Host web app"
   - Conecta tu repositorio de GitHub
   - AWS detectará automáticamente `amplify.yml`
   - Confirma y espera el deploy

3. URLs resultantes:
   - Cliente: `https://main.xxxxx.amplifyapp.com/client/`
   - Dashboard: `https://main.xxxxx.amplifyapp.com/restaurant/`

### Paso 7: Probar que todo funciona

1. Abre el sitio del cliente
2. Agrega productos al carrito
3. Llena el formulario con **tu email real**
4. Envía el pedido
5. Revisa tu email (debería llegar en 10-30 segundos)
6. Abre el dashboard del restaurante
7. Verifica que aparece el pedido
8. Actualiza el estado y revisa que llegue otro email

## 🧪 Troubleshooting

### Los emails no llegan

**Diagnóstico:**

```bash
# Ver logs de la Lambda de emails
cd backend/src
sls logs -f sendEmailNotification --tail
```

**Causas comunes:**

1. **SENDGRID_API_KEY no configurada**
   - Solución: Verificar que hiciste `export SENDGRID_API_KEY="..."` antes del deploy
   - Verificar en AWS Lambda Console → Configuration → Environment variables

2. **Email del remitente no verificado en SendGrid**
   - Solución: Ve a SendGrid → Settings → Sender Authentication y verifica el email

3. **Campo de email vacío en el formulario**
   - El sistema solo envía emails si customer_email no está vacío
   - Verifica que estés llenando el campo de email al hacer el pedido

4. **API Key inválida o revocada**
   - Verifica en los logs si hay error "SendGrid API error"
   - Crea una nueva API key y redeploy

**Para redeployar con nueva API key:**

```bash
cd backend/src
export SENDGRID_API_KEY='SG.nueva-api-key'
sls deploy
```

### El menú no muestra imágenes

No te preocupes, esto es normal. El sistema tiene un fallback automático:

1. Primero intenta cargar la imagen de la base de datos (campo `image_url`)
2. Si no existe, busca en el diccionario de fallback en `frontend/client/app.js` (líneas 15-34)
3. Si tampoco encuentra ahí, muestra una imagen genérica de Unsplash

**Para agregar imágenes manualmente:**

Edita `frontend/client/app.js` líneas 15-34:

```javascript
const imageDefaults = {
    'Nombre del Producto': {
        image_url: 'https://url-de-la-imagen.jpg',
        description: 'Descripción del producto'
    },
    // Agregar más productos...
}
```

Luego sube los cambios a GitHub y Amplify lo deployará automáticamente.

### Credenciales de AWS expiradas

**Síntoma:** `serverless deploy` falla con error de credenciales

**Solución:**

```bash
# Ve a AWS Academy → AWS Details → Show
# Copia los nuevos comandos export y ejecútalos

export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."

# Verificar
aws sts get-caller-identity
```

### Frontend no se conecta al backend

**Diagnóstico:**
- Abre DevTools del navegador (F12)
- Ve a la pestaña Network
- Intenta hacer un pedido
- Mira si hay errores CORS o de red

**Soluciones:**

1. Verifica que la URL en `config.js` sea correcta (sin `/` al final)
2. Verifica que CORS esté habilitado en `serverless.yml`:
```yaml
provider:
  httpApi:
    cors: true
```
3. Redeploy si es necesario: `sls deploy`

### Dashboard no muestra pedidos

**Diagnóstico:**

```bash
# Ver si hay pedidos en DynamoDB
aws dynamodb scan --table-name dev-Orders --max-items 5

# Ver logs del dashboard
sls logs -f getDashboardSummary --tail
```

**Soluciones:**

1. Verifica que el `tenant_id` en `config.js` sea `"pardos-chicken"`
2. Abre la consola del navegador (F12) y busca errores de JavaScript
3. Verifica que estés logueado en el dashboard

## 📊 Ver logs y métricas

### CloudWatch Logs

Cada Lambda tiene su propio log group:

```bash
# Ver logs en tiempo real
sls logs -f createOrder --tail
sls logs -f sendEmailNotification --tail
sls logs -f updateOrderStep --tail

# Ver logs de los últimos 30 minutos
sls logs -f createOrder --startTime 30m
```

### Métricas en CloudWatch

Ve a AWS Console → CloudWatch → Metrics:
- Invocations (cuántas veces se ejecutó)
- Duration (tiempo de ejecución)
- Errors (errores)
- Throttles (invocaciones limitadas)

## 💡 Conceptos de cloud computing aplicados

Este proyecto implementa varios patrones modernos:

**Arquitectura Serverless**
- No hay servidores que mantener
- AWS escala automáticamente según la demanda
- Solo pagas por lo que usas (pay-per-request)

**Event-Driven Architecture**
- Los servicios se comunican mediante eventos
- Desacoplamiento total entre componentes
- Fácil agregar nuevas funcionalidades sin modificar código existente

**Microservicios**
- Cada funcionalidad tiene su propio microservicio
- Se pueden deployar independientemente
- Más fácil de mantener y debuggear

**Infrastructure as Code**
- Todo definido en `serverless.yml`
- Se puede versionar con Git
- Fácil replicar el entorno (dev, staging, prod)

**NoSQL y patrones de acceso**
- DynamoDB con partition keys y sort keys
- Denormalización para evitar joins
- Queries eficientes con índices

## 🎓 Lecciones aprendidas

**Sobre Lambda:**
- Los cold starts pueden agregar 1-2 segundos la primera vez
- Configurar bien la memoria (1024 MB funciona bien para este proyecto)
- Usar variables de entorno para configuración

**Sobre DynamoDB:**
- Partition key = tenant_id permite multi-tenancy
- Sort key = order_id/product_id permite queries eficientes
- Siempre usar timestamps en formato ISO para facilitar ordenamiento

**Sobre EventBridge:**
- Permite desacoplar completamente los servicios
- Fácil agregar nuevos consumers sin modificar publishers
- Los eventos quedan logueados automáticamente

**Sobre Frontend sin frameworks:**
- Para proyectos pequeños, Vanilla JS es suficiente
- No hay bundle size ni dependencias que mantener
- Más control sobre el código y performance

**Sobre SendGrid:**
- El plan gratuito (100 emails/día) es suficiente para desarrollo
- Los emails se envían en ~1-2 segundos
- Importante verificar el email del remitente antes de enviar

## 🔮 Mejoras futuras

Algunas ideas para extender el proyecto:

- Agregar WebSockets para updates en tiempo real del dashboard
- Sistema de pagos online (Stripe/PayPal)
- Tracking GPS del repartidor en tiempo real
- Aplicación móvil con React Native
- Sistema de cupones y descuentos
- Ratings y reviews de productos
- Analytics dashboard con QuickSight
- Machine learning para predicción de demanda

## 📝 Notas importantes

### Sobre AWS Academy

- Las credenciales expiran cada 4 horas
- Algunos servicios tienen límites (como SES que no está disponible, por eso usamos SendGrid)
- Siempre guarda tu código en Git porque el lab se puede resetear

### Sobre costos

**Free tier de AWS incluye:**
- Lambda: 1M requests/mes
- DynamoDB: 25GB storage + 25 WCU + 25 RCU
- API Gateway: 1M requests/mes
- EventBridge: Eventos custom ilimitados

**SendGrid:**
- Plan gratuito: 100 emails/día
- Para producción considerar plan de pago

Este proyecto debería mantenerse dentro del free tier si es solo para pruebas.

---

**© 2025 - Sistema de Gestión de Pedidos para Restaurantes**

Proyecto de Cloud Computing - Arquitectura Serverless con AWS
