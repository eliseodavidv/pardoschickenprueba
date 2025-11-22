# 🍗 Pardos Chicken - Sistema de Gestión de Pedidos

Sistema completo de gestión de pedidos en tiempo real para restaurantes de comida rápida, implementado con arquitectura serverless multi-tenant y event-driven en AWS.

## 📋 Descripción del Proyecto

Sistema end-to-end que permite a los clientes realizar pedidos en línea y rastrear su progreso en tiempo real, mientras que el personal del restaurante gestiona el workflow completo desde la recepción hasta la entrega.

### Características Principales

- ✅ Arquitectura Multi-tenant (soporta múltiples restaurantes)
- ✅ Serverless 100% (AWS Lambda)
- ✅ Event-driven (EventBridge + Step Functions)
- ✅ Rastreo en tiempo real del workflow de pedidos
- ✅ Métricas de tiempo por cada fase
- ✅ Dashboard con estadísticas y promedios
- ✅ Aplicaciones web responsive para cliente y restaurante

---

## 🏗️ Arquitectura

### Stack Tecnológico

**Backend:**
- Runtime: Python 3.13
- Framework: Serverless Framework
- Cloud: AWS
  - Lambda (13 funciones)
  - DynamoDB (4 tablas)
  - API Gateway (HTTP API)
  - EventBridge (bus de eventos + reglas)
  - Step Functions (workflow automatizado)
  - S3 (almacenamiento de reportes)
  - CloudWatch (logs y métricas)

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- AWS Amplify (hosting)
- Integración con API Gateway

### Microservicios

1. **ms_orders** (Cliente)
   - Crear pedidos
   - Consultar pedidos
   - Ver métricas de pedidos

2. **ms_tenants_menu** (Configuración)
   - Gestión de tenants
   - Gestión de menú

3. **ms_workflow** (Restaurante)
   - Actualizar estados
   - Dashboard de métricas
   - Reportes diarios

---

## 📁 Estructura del Proyecto

```
pardoschickenprueba/
├── backend/                           # Backend Serverless
│   ├── BACKEND_IMPROVEMENTS.md       # Documentación detallada del backend
│   └── src/
│       ├── serverless.yml            # Configuración de infraestructura
│       ├── common/                   # Módulos compartidos
│       │   ├── db.py                # Abstracción de DynamoDB
│       │   └── events.py            # Abstracción de EventBridge
│       ├── ms_orders/               # Microservicio de Pedidos (Cliente)
│       │   ├── create_order.py
│       │   ├── get_order.py
│       │   ├── list_orders.py
│       │   └── get_order_metrics.py # ⭐ Nuevo
│       ├── ms_tenants_menu/         # Microservicio de Tenants y Menú
│       │   ├── get_tenants.py
│       │   ├── get_menu.py
│       │   └── put_menu_item.py
│       └── ms_workflow/             # Microservicio de Workflow (Restaurante)
│           ├── update_order_step.py        # ⭐ Mejorado
│           ├── get_dashboard_summary.py    # ⭐ Mejorado
│           ├── export_daily_report.py
│           ├── check_order_status.py       # ⭐ Nuevo
│           └── calculate_order_metrics.py  # ⭐ Nuevo
│
└── frontend/                         # Frontend Web Applications
    ├── README.md                     # Documentación del frontend
    ├── amplify.yml                   # Configuración de Amplify
    ├── client/                       # Aplicación del Cliente
    │   ├── index.html
    │   ├── styles.css
    │   ├── app.js
    │   └── config.js
    └── restaurant/                   # Aplicación del Restaurante
        ├── index.html
        ├── styles.css
        ├── app.js
        └── config.js
```

---

## 🚀 Instalación y Despliegue

### Prerrequisitos

- AWS CLI configurado
- Node.js 16+ y npm
- Python 3.13
- Serverless Framework: `npm install -g serverless`

### Paso 1: Desplegar el Backend

```bash
cd backend/src
serverless deploy --stage dev
```

**Output esperado:**
```
Service deployed to stack pardos-orders-dev
endpoint: POST - https://abc123xyz.execute-api.us-east-1.amazonaws.com
functions:
  createOrder: pardos-orders-dev-createOrder
  ...
```

**Guarda la URL del endpoint!**

### Paso 2: Configurar el Frontend

Edita los archivos `config.js` en ambas aplicaciones:

**frontend/client/config.js:**
```javascript
const API_CONFIG = {
    baseURL: 'https://TU_API_GATEWAY_URL',  // ← Pegar aquí
    tenantId: 'pardos-chicken'
};
```

**frontend/restaurant/config.js:**
```javascript
const API_CONFIG = {
    baseURL: 'https://TU_API_GATEWAY_URL',  // ← Pegar aquí
    tenantId: 'pardos-chicken'
};
```

### Paso 3: Probar Localmente

```bash
# Aplicación de Cliente
cd frontend/client
python3 -m http.server 8000

# Aplicación de Restaurante (nueva terminal)
cd frontend/restaurant
python3 -m http.server 8001
```

Abre:
- Cliente: http://localhost:8000
- Restaurante: http://localhost:8001

### Paso 4: Desplegar Frontend en Amplify

```bash
# Opción A: Desde AWS Console
# 1. Ir a AWS Amplify
# 2. New app → Host web app
# 3. Conectar repositorio
# 4. Configurar rutas: frontend/client y frontend/restaurant

# Opción B: Amplify CLI
cd frontend/client
amplify init
amplify add hosting
amplify publish
```

---

## 📖 Guía de Uso

### Para Clientes

1. **Hacer un Pedido:**
   - Abre la aplicación de cliente
   - Selecciona productos del menú (+/-)
   - Llena datos de entrega
   - Haz clic en "Hacer Pedido"
   - **Guarda tu ID de pedido**

2. **Rastrear Pedido:**
   - Ingresa tu ID de pedido
   - Haz clic en "Rastrear"
   - Ve el progreso en tiempo real

### Para Personal del Restaurante

1. **Ver Dashboard:**
   - Estadísticas generales
   - Pedidos activos
   - Tiempos promedio

2. **Actualizar Estados:**
   - Encuentra el pedido
   - Clic en "Actualizar Estado"
   - Selecciona nuevo estado + tu nombre + rol
   - Confirma

**Flujo de Estados:**
```
RECEIVED → COOKING → PACKING → DELIVERING → DELIVERED
```

**Roles:**
- RECEIVED → COOKING: Cocinero (KITCHEN_STAFF)
- COOKING → PACKING: Despachador (PACKER)
- PACKING → DELIVERING: Repartidor (DELIVERY_DRIVER)
- DELIVERING → DELIVERED: Repartidor (DELIVERY_DRIVER)

---

## 🎯 Requerimientos del Laboratorio

### ✅ Cumplimiento Completo

| Requerimiento | Estado | Implementación |
|---------------|--------|----------------|
| **Cliente puede colocar pedido desde app web** | ✅ | `frontend/client/` |
| **Cliente puede ver estado de su pedido** | ✅ | Rastreo en tiempo real + métricas |
| **App web para restaurante** | ✅ | `frontend/restaurant/` |
| **Workflow de atención de pedidos** | ✅ | Flujo completo implementado |
| **Arquitectura Multi-tenancy** | ✅ | Soporta múltiples restaurantes |
| **Arquitectura Serverless** | ✅ | 100% AWS Lambda |
| **Arquitectura Event-driven** | ✅ | EventBridge + Step Functions |
| **Mínimo 3 microservicios** | ✅ | ms_orders, ms_tenants_menu, ms_workflow |
| **AWS Amplify** | ✅ | Configurado para frontend |
| **AWS API Gateway** | ✅ | HTTP API con 9 endpoints |
| **AWS EventBridge** | ✅ | Bus de eventos + reglas |
| **AWS Step Functions** | ✅ | Workflow automatizado de monitoreo |
| **AWS Lambda** | ✅ | 13 funciones |
| **AWS DynamoDB** | ✅ | 4 tablas |
| **AWS S3** | ✅ | Bucket de reportes |
| **Rastreo de tiempos** | ✅ | Timestamps por fase |
| **Rastreo de personal** | ✅ | Registro de quién atendió |
| **Dashboard resumen** | ✅ | Métricas en tiempo real |

---

## 🔧 API Endpoints

### Cliente

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/tenants` | GET | Listar restaurantes |
| `/tenants/{tenantId}/menu` | GET | Obtener menú |
| `/tenants/{tenantId}/orders` | POST | Crear pedido |
| `/tenants/{tenantId}/orders` | GET | Listar pedidos |
| `/tenants/{tenantId}/orders/{orderId}` | GET | Obtener pedido |
| `/tenants/{tenantId}/orders/{orderId}/metrics` | GET | Métricas del pedido |

### Restaurante

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/tenants/{tenantId}/dashboard` | GET | Dashboard de métricas |
| `/tenants/{tenantId}/orders/{orderId}/step` | POST | Actualizar estado |
| `/tenants/{tenantId}/menu` | POST | Agregar producto al menú |

---

## 📊 Flujo de Datos

### Crear Pedido

```
1. Cliente hace pedido (POST /orders)
   ↓
2. Lambda crea pedido en DynamoDB
   ↓
3. Lambda publica evento "order.created" a EventBridge
   ↓
4. EventBridge Rule detecta el evento
   ↓
5. Step Functions inicia workflow automático
   ↓
6. Workflow monitorea progreso del pedido
```

### Actualizar Estado

```
1. Personal actualiza estado (POST /orders/{id}/step)
   ↓
2. Lambda valida transición de estado
   ↓
3. Lambda actualiza DynamoDB con timestamps
   ↓
4. Lambda registra evento en OrderEvents
   ↓
5. Lambda publica evento "order.updated" a EventBridge
   ↓
6. Step Functions continúa monitoreo
```

---

## 📈 Métricas y Monitoreo

### Dashboard de Restaurante

El dashboard muestra:
- Total de pedidos
- Pedidos en proceso vs completados
- Tiempo promedio total de entrega
- Tiempo promedio en cada fase:
  - Cocina
  - Empaque
  - Entrega
- 10 pedidos más recientes con timeline

### Rastreo de Cliente

El cliente puede ver:
- Estado actual del pedido
- Timeline completo de eventos
- Quién atendió cada paso
- Tiempo transcurrido por fase
- Tiempo estimado restante

---

## 🗄️ Esquema de Base de Datos

### Tabla: Orders

```javascript
{
  "tenant_id": "pardos-chicken",        // HASH
  "order_id": "uuid",                   // RANGE
  "status": "COOKING",
  "items": [...],
  "customer_name": "Juan Pérez",
  "customer_address": "Av. Principal 123",
  "customer_phone": "+51999999999",
  "created_at": "2025-11-22T10:00:00Z",
  "updated_at": "2025-11-22T10:30:00Z",

  // Campos de rastreo de tiempos
  "cooking_started_at": "2025-11-22T10:05:00Z",
  "cooking_by": "Juan Pérez",
  "packing_started_at": "2025-11-22T10:30:00Z",
  "packing_by": "María López",
  "delivering_started_at": "2025-11-22T10:38:00Z",
  "delivering_by": "Carlos Ruiz",
  "delivered_started_at": "2025-11-22T11:05:00Z",
  "delivered_by": "Carlos Ruiz"
}
```

### Tabla: OrderEvents

```javascript
{
  "order_id": "uuid",                   // HASH
  "ts": "2025-11-22T10:30:00Z",        // RANGE
  "status": "COOKING",
  "by": "Juan Pérez",
  "by_role": "KITCHEN_STAFF",
  "previous_status": "RECEIVED",
  "tenant_id": "pardos-chicken"
}
```

---

## 🎨 Capturas de Pantalla

_(Agregar capturas después del deployment)_

### Aplicación de Cliente
- Menú de productos
- Carrito de compras
- Rastreo de pedido

### Aplicación de Restaurante
- Dashboard principal
- Lista de pedidos activos
- Modal de actualización de estado

---

## 📝 Documentación Adicional

- [Backend - Mejoras Detalladas](backend/BACKEND_IMPROVEMENTS.md)
- [Frontend - Guía Completa](frontend/README.md)

---

## 🐛 Troubleshooting

### Backend no despliega
```bash
# Verificar credenciales AWS
aws sts get-caller-identity

# Verificar Serverless Framework
serverless --version

# Ver logs detallados
serverless deploy --verbose
```

### Frontend no conecta con backend
1. Verifica la URL en `config.js`
2. Revisa CORS en API Gateway
3. Comprueba que el backend esté desplegado

### Pedidos no se crean
1. Verifica que haya productos en el menú
2. Revisa logs de Lambda en CloudWatch
3. Confirma que DynamoDB esté accesible

---

## 🚀 Mejoras Futuras

- [ ] Autenticación de usuarios (Cognito)
- [ ] WebSockets para actualización en tiempo real
- [ ] Notificaciones push
- [ ] Tracking GPS del repartidor
- [ ] Integración con pasarelas de pago
- [ ] Sistema de calificaciones
- [ ] Cupones y descuentos
- [ ] Reportes avanzados en S3

---

## 👥 Equipo

**Grupo 4 - Pardos Chicken**
Laboratorio de Cloud Computing
2025-2

---

## 📄 Licencia

Proyecto académico - Universidad

---

## 📞 Soporte

Para reportar issues:
- Abre un issue en GitHub
- Incluye logs y capturas de pantalla
- Describe los pasos para reproducir

---

**Última actualización**: 2025-11-22
**Versión**: 1.0.0
**Estado**: ✅ Producción Ready
