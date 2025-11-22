# Mejoras al Backend - Sistema de Gestión de Pedidos Pardos Chicken

## 📋 Resumen de Mejoras

Este documento detalla las mejoras realizadas al backend del sistema de gestión de pedidos para cumplir con todos los requerimientos del laboratorio.

---

## 🎯 Requerimientos Cumplidos

### ✅ Arquitectura
- **Multi-tenancy**: Soporta múltiples restaurantes (tenants)
- **Serverless**: 100% serverless usando AWS Lambda
- **Event-driven**: EventBridge para comunicación entre servicios
- **3+ Microservicios**: `ms_orders`, `ms_tenants_menu`, `ms_workflow`

### ✅ Servicios AWS Utilizados
- ✅ **Amplify**: Preparado para frontend (pendiente implementación)
- ✅ **API Gateway**: HTTP API con 9 endpoints
- ✅ **EventBridge**: Bus de eventos personalizado + Reglas
- ✅ **Step Functions**: Workflow completo de monitoreo de pedidos
- ✅ **Lambda**: 13 funciones serverless
- ✅ **DynamoDB**: 4 tablas (Tenants, MenuItems, Orders, OrderEvents)
- ✅ **S3**: Bucket para reportes diarios

---

## 🆕 Nuevas Funcionalidades

### 1. **Validación de Transiciones de Estado**

**Archivo**: `ms_workflow/update_order_step.py`

**Mejoras**:
- Validación de transiciones válidas según el flujo del workflow
- Solo permite transiciones lógicas (ej: RECEIVED → COOKING, no RECEIVED → DELIVERED)
- Validación de roles esperados para cada transición
- Registro automático de timestamps por cada fase

**Flujo de Estados**:
```
RECEIVED → COOKING → PACKING → DELIVERING → DELIVERED
```

**Roles Esperados**:
- `COOKING`: KITCHEN_STAFF (Cocinero)
- `PACKING`: PACKER (Despachador)
- `DELIVERING`: DELIVERY_DRIVER (Repartidor)
- `DELIVERED`: DELIVERY_DRIVER (Repartidor confirma entrega)

**Ejemplo de Request**:
```bash
POST /tenants/pardos-chicken/orders/{orderId}/step
Content-Type: application/json

{
  "status": "COOKING",
  "attended_by": "Juan Pérez",
  "role": "KITCHEN_STAFF"
}
```

**Ejemplo de Response**:
```json
{
  "order_id": "abc-123",
  "status": "COOKING",
  "previous_status": "RECEIVED",
  "attended_by": "Juan Pérez",
  "role": "KITCHEN_STAFF",
  "timestamp": "2025-11-22T10:30:00Z"
}
```

**Error si transición inválida**:
```json
{
  "message": "Invalid transition from RECEIVED to DELIVERED",
  "current_status": "RECEIVED",
  "allowed_next_states": ["COOKING"]
}
```

---

### 2. **Rastreo de Tiempos por Fase**

**Archivo**: `ms_workflow/update_order_step.py`

**Campos Agregados a Tabla Orders**:
Cuando se actualiza el estado, se agregan automáticamente:
- `cooking_started_at`: Timestamp cuando empezó a cocinarse
- `cooking_by`: Quién atendió (nombre del cocinero)
- `packing_started_at`: Timestamp cuando empezó el empaque
- `packing_by`: Quién empacó
- `delivering_started_at`: Timestamp cuando salió a delivery
- `delivering_by`: Quién entrega
- `delivered_started_at`: Timestamp de entrega final
- `delivered_by`: Quién entregó

**Tabla OrderEvents**:
Cada cambio de estado genera un evento con:
```json
{
  "order_id": "abc-123",
  "ts": "2025-11-22T10:30:00Z",
  "status": "COOKING",
  "by": "Juan Pérez",
  "by_role": "KITCHEN_STAFF",
  "previous_status": "RECEIVED",
  "tenant_id": "pardos-chicken"
}
```

---

### 3. **Dashboard Mejorado con Métricas de Tiempo**

**Archivo**: `ms_workflow/get_dashboard_summary.py`

**Endpoint**: `GET /tenants/{tenantId}/dashboard`

**Métricas Calculadas**:
- Total de órdenes
- Órdenes completadas vs en proceso
- Conteo por cada estado
- **Tiempo promedio total de entrega** (minutos y horas)
- **Tiempo promedio en cada fase**:
  - Cocina (cooking)
  - Empaque (packing)
  - Entrega (delivering)
- **10 órdenes más recientes con timeline completo**

**Ejemplo de Response**:
```json
{
  "tenant_id": "pardos-chicken",
  "total_orders": 50,
  "completed_orders": 30,
  "in_progress_orders": 20,
  "by_status": {
    "RECEIVED": 5,
    "COOKING": 8,
    "PACKING": 3,
    "DELIVERING": 4,
    "DELIVERED": 30
  },
  "average_times": {
    "total_delivery_minutes": 65.5,
    "total_delivery_hours": 1.09,
    "phases": {
      "cooking_minutes": 25.3,
      "packing_minutes": 7.2,
      "delivering_minutes": 33.0
    }
  },
  "recent_orders": [
    {
      "order_id": "abc-123",
      "status": "DELIVERED",
      "created_at": "2025-11-22T10:00:00Z",
      "phases": {
        "cooking": {
          "started_at": "2025-11-22T10:05:00Z",
          "time_from_creation_minutes": 5.0,
          "attended_by": "Juan Pérez"
        },
        "packing": {
          "started_at": "2025-11-22T10:30:00Z",
          "time_from_creation_minutes": 30.0,
          "attended_by": "María López"
        },
        "delivering": {
          "started_at": "2025-11-22T10:38:00Z",
          "time_from_creation_minutes": 38.0,
          "attended_by": "Carlos Ruiz"
        },
        "delivered": {
          "started_at": "2025-11-22T11:05:00Z",
          "time_from_creation_minutes": 65.0,
          "attended_by": "Carlos Ruiz"
        }
      },
      "total_time_minutes": 65.0
    }
  ]
}
```

---

### 4. **Endpoint de Métricas para Cliente**

**Archivo**: `ms_orders/get_order_metrics.py`

**Endpoint**: `GET /tenants/{tenantId}/orders/{orderId}/metrics`

**Propósito**: Permite al cliente ver el progreso detallado de su pedido con tiempos estimados.

**Características**:
- Timeline completo de la orden
- Tiempo transcurrido en cada fase
- Quién atendió cada paso
- **Tiempo estimado restante** si no está completado
- Tiempo total si está completado

**Ejemplo de Response**:
```json
{
  "order_id": "abc-123",
  "tenant_id": "pardos-chicken",
  "current_status": "COOKING",
  "is_completed": false,
  "created_at": "2025-11-22T10:00:00Z",
  "customer_name": "Pedro García",
  "timeline": [
    {
      "status": "RECEIVED",
      "timestamp": "2025-11-22T10:00:00Z",
      "attended_by": "SYSTEM",
      "role": "SYSTEM"
    },
    {
      "status": "COOKING",
      "timestamp": "2025-11-22T10:05:00Z",
      "attended_by": "Juan Pérez",
      "role": "KITCHEN_STAFF"
    }
  ],
  "phase_metrics": {
    "COOKING": {
      "description": "Cocinero preparando",
      "started_at": "2025-11-22T10:05:00Z",
      "time_from_order_creation": {
        "seconds": 300,
        "minutes": 5.0,
        "hours": 0.08
      },
      "attended_by": "Juan Pérez"
    }
  },
  "total_time": null,
  "estimated_remaining_time": {
    "minutes": 55,
    "hours": 0.92
  }
}
```

---

### 5. **Step Functions - Workflow Real de Monitoreo**

**Archivo**: `serverless.yml` (líneas 171-431)

**Funciones Lambda Nuevas**:
1. `checkOrderStatus`: Verifica estado actual de una orden
2. `calculateOrderMetrics`: Calcula métricas de tiempo completas

**Flujo del Workflow**:

```
1. LogOrderReceived (Pass)
   ↓
2. CheckInitialStatus (Lambda)
   ↓
3. WaitForCooking (Wait 300s)
   ↓
4. CheckCookingStatus (Lambda)
   ↓
5. IsCooking (Choice)
   ├─ Si está RECEIVED → volver a WaitForCooking
   └─ Si está COOKING+ → continuar a WaitForPacking
   ↓
6. WaitForPacking (Wait 180s)
   ↓
7. CheckPackingStatus (Lambda)
   ↓
8. IsPacking (Choice)
   ├─ Si está RECEIVED/COOKING → volver a WaitForPacking
   └─ Si está PACKING+ → continuar a WaitForDelivery
   ↓
9. WaitForDelivery (Wait 600s)
   ↓
10. CheckDeliveryStatus (Lambda)
    ↓
11. IsDelivered (Choice)
    ├─ Si NO está DELIVERED → volver a WaitForDelivery
    └─ Si está DELIVERED → continuar
    ↓
12. CalculateFinalMetrics (Lambda)
    ↓
13. WorkflowCompleted (Succeed)
```

**Características**:
- ✅ Manejo de errores con reintentos (Retry)
- ✅ Estados de error (Catch)
- ✅ Verificación periódica del estado
- ✅ Cálculo de métricas finales al completar
- ✅ Se inicia automáticamente vía EventBridge

**Inicio Automático**:
El workflow se inicia automáticamente cuando:
- Se crea una nueva orden (evento `order.created` en EventBridge)
- La regla `OrderCreatedRule` captura el evento
- Extrae `tenant_id`, `order_id`, `status` del evento
- Inicia el Step Functions con esos parámetros

---

### 6. **EventBridge - Integración Completa**

**Archivo**: `serverless.yml` (líneas 166-192)

**Bus de Eventos**: `{stage}-pardos-orders-bus`

**Regla**: `OrderCreatedRule`
- **Trigger**: Evento `order.created` de source `pardos.orders`
- **Acción**: Inicia Step Functions workflow
- **Input Transformation**: Extrae datos del evento para Step Functions

**Eventos Publicados**:

| Evento | Source | DetailType | Cuándo |
|--------|--------|-----------|--------|
| order.created | pardos.orders | order.created | Al crear orden (create_order.py) |
| order.updated | pardos.orders | order.updated | Al actualizar estado (update_order_step.py) |

**Flujo Event-Driven**:
```
1. Cliente crea orden (POST /orders)
   ↓
2. create_order.py publica evento "order.created" a EventBridge
   ↓
3. OrderCreatedRule captura el evento
   ↓
4. Step Functions workflow se inicia automáticamente
   ↓
5. Step Functions monitorea la orden hasta completarla
```

---

## 📊 Arquitectura de Microservicios

### Microservicio 1: `ms_orders` (Cliente)
**Responsabilidad**: Gestión de pedidos desde la perspectiva del cliente

| Función | Endpoint | Método | Descripción |
|---------|----------|--------|-------------|
| createOrder | `/tenants/{tenantId}/orders` | POST | Crear nuevo pedido |
| getOrder | `/tenants/{tenantId}/orders/{orderId}` | GET | Obtener detalles de pedido |
| listOrders | `/tenants/{tenantId}/orders` | GET | Listar pedidos |
| **getOrderMetrics** | `/tenants/{tenantId}/orders/{orderId}/metrics` | GET | **Ver métricas y tiempos** |

### Microservicio 2: `ms_tenants_menu` (Configuración)
**Responsabilidad**: Gestión de tenants y menú de productos

| Función | Endpoint | Método | Descripción |
|---------|----------|--------|-------------|
| getTenants | `/tenants` | GET | Listar restaurantes |
| getMenu | `/tenants/{tenantId}/menu` | GET | Ver menú |
| putMenuItem | `/tenants/{tenantId}/menu` | POST | Agregar/actualizar ítem |

### Microservicio 3: `ms_workflow` (Restaurante)
**Responsabilidad**: Gestión del workflow de preparación y entrega

| Función | Endpoint | Método | Descripción |
|---------|----------|--------|-------------|
| **updateOrderStep** | `/tenants/{tenantId}/orders/{orderId}/step` | POST | **Actualizar estado (mejorado)** |
| **getDashboardSummary** | `/tenants/{tenantId}/dashboard` | GET | **Dashboard con métricas** |
| exportDailyReport | CloudWatch Events | - | Exportar reporte a S3 |
| **checkOrderStatus** | Llamado por Step Functions | - | **Verificar estado** |
| **calculateOrderMetrics** | Llamado por Step Functions | - | **Calcular métricas** |

---

## 🗄️ Esquema de Datos Mejorado

### Tabla: Orders (Mejorada)
```json
{
  "tenant_id": "pardos-chicken",        // HASH key
  "order_id": "uuid",                   // RANGE key
  "status": "COOKING",
  "items": [...],
  "customer_name": "Pedro García",
  "customer_address": "Av. Principal 123",
  "customer_phone": "+51999999999",
  "created_at": "2025-11-22T10:00:00Z",
  "updated_at": "2025-11-22T10:30:00Z",

  // ⭐ NUEVOS CAMPOS - Rastreo de tiempos por fase
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

### Tabla: OrderEvents (Mejorada)
```json
{
  "order_id": "uuid",                   // HASH key
  "ts": "2025-11-22T10:30:00Z",        // RANGE key (timestamp)
  "status": "COOKING",
  "by": "Juan Pérez",
  "by_role": "KITCHEN_STAFF",
  "previous_status": "RECEIVED",        // ⭐ NUEVO
  "tenant_id": "pardos-chicken"         // ⭐ NUEVO
}
```

---

## 📝 Ejemplos de Uso

### Flujo Completo de un Pedido

#### 1. Cliente crea pedido
```bash
POST /tenants/pardos-chicken/orders
Content-Type: application/json

{
  "items": [
    {"product_id": "prod-1", "quantity": 2, "name": "Pollo Entero"}
  ],
  "customer_name": "Pedro García",
  "customer_address": "Av. Larco 123",
  "customer_phone": "+51999999999"
}

# Response:
{
  "order_id": "abc-123",
  "status": "RECEIVED"
}

# 🎯 Automáticamente se inicia Step Functions workflow
```

#### 2. Cocinero toma el pedido
```bash
POST /tenants/pardos-chicken/orders/abc-123/step
Content-Type: application/json

{
  "status": "COOKING",
  "attended_by": "Juan Pérez",
  "role": "KITCHEN_STAFF"
}

# Response:
{
  "order_id": "abc-123",
  "status": "COOKING",
  "previous_status": "RECEIVED",
  "attended_by": "Juan Pérez",
  "role": "KITCHEN_STAFF",
  "timestamp": "2025-11-22T10:05:00Z"
}
```

#### 3. Cliente verifica progreso
```bash
GET /tenants/pardos-chicken/orders/abc-123/metrics

# Response: (ver ejemplo en sección 4 arriba)
# Incluye timeline, tiempos transcurridos, tiempo estimado restante
```

#### 4. Despachador empaca
```bash
POST /tenants/pardos-chicken/orders/abc-123/step
Content-Type: application/json

{
  "status": "PACKING",
  "attended_by": "María López",
  "role": "PACKER"
}
```

#### 5. Repartidor toma para delivery
```bash
POST /tenants/pardos-chicken/orders/abc-123/step
Content-Type: application/json

{
  "status": "DELIVERING",
  "attended_by": "Carlos Ruiz",
  "role": "DELIVERY_DRIVER"
}
```

#### 6. Repartidor confirma entrega
```bash
POST /tenants/pardos-chicken/orders/abc-123/step
Content-Type: application/json

{
  "status": "DELIVERED",
  "attended_by": "Carlos Ruiz",
  "role": "DELIVERY_DRIVER"
}

# 🎯 Step Functions calcula métricas finales y completa el workflow
```

#### 7. Gerente ve dashboard
```bash
GET /tenants/pardos-chicken/dashboard

# Response: Dashboard completo con métricas de tiempo
```

---

## 🔧 Configuración y Despliegue

### Prerrequisitos
- AWS CLI configurado
- Node.js y npm instalados
- Serverless Framework instalado: `npm install -g serverless`
- Python 3.13

### Despliegue
```bash
cd backend/src
serverless deploy --stage dev

# Output incluirá:
# - URL del API Gateway
# - ARN del Step Functions
# - Nombres de las tablas DynamoDB
# - Nombre del EventBus
```

### Variables de Entorno
Todas las funciones Lambda tienen acceso a:
```
TENANTS_TABLE: dev-Tenants
MENU_TABLE: dev-MenuItems
ORDERS_TABLE: dev-Orders
ORDER_EVENTS_TABLE: dev-OrderEvents
EVENTS_BUS_NAME: dev-pardos-orders-bus
REPORTS_BUCKET: dev-pardos-orders-reports
```

---

## 📈 Monitoreo y Observabilidad

### CloudWatch Logs
Cada función Lambda genera logs en CloudWatch:
- `/aws/lambda/pardos-orders-dev-createOrder`
- `/aws/lambda/pardos-orders-dev-updateOrderStep`
- etc.

### Step Functions Console
Ver ejecuciones del workflow en:
AWS Console → Step Functions → `dev-pardos-order-workflow`

Cada ejecución muestra:
- Estados completados
- Tiempos de cada estado
- Input/output de cada Lambda
- Errores si los hay

### EventBridge Monitoring
Ver eventos en:
AWS Console → EventBridge → Event buses → `dev-pardos-orders-bus`

### DynamoDB Metrics
Monitorear en CloudWatch:
- Read/Write capacity units
- Throttled requests
- Latency

---

## 🚀 Próximos Pasos (Frontend)

Para completar el sistema según los requerimientos, falta:

1. **Aplicación Web de Cliente** (Amplify)
   - Hacer pedidos
   - Ver estado en tiempo real
   - Ver métricas de tiempo estimado

2. **Aplicación Web de Restaurante** (Amplify)
   - Dashboard de órdenes activas
   - Botones para actualizar estados
   - Vista de métricas y tiempos
   - Gestión de menú

3. **Amplify Hosting**
   - Configurar Amplify para hosting
   - CI/CD automático desde git

---

## 📚 Referencias

- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/)
- [AWS EventBridge](https://docs.aws.amazon.com/eventbridge/)
- [Serverless Framework](https://www.serverless.com/framework/docs/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

---

## 👥 Roles del Sistema

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| SYSTEM | Sistema automático | Crear órdenes |
| KITCHEN_STAFF | Cocinero | Marcar como COOKING |
| PACKER | Despachador | Marcar como PACKING |
| DELIVERY_DRIVER | Repartidor | Marcar como DELIVERING, DELIVERED |
| MANAGER | Gerente | Ver dashboard, reportes |

---

**Última actualización**: 2025-11-22
**Versión**: 2.0 (Backend Mejorado)
**Equipo**: Grupo 4 - Pardos Chicken
