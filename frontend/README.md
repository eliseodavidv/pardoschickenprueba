# Frontend - Sistema de Gestión de Pedidos Pardos Chicken

## 📱 Aplicaciones Web

Este proyecto contiene dos aplicaciones web para el sistema de gestión de pedidos de Pardos Chicken:

1. **Aplicación de Cliente** (`frontend/client/`)
   - Hacer pedidos en línea
   - Rastrear estado del pedido en tiempo real
   - Ver métricas de tiempo

2. **Aplicación de Restaurante** (`frontend/restaurant/`)
   - Dashboard con métricas en tiempo real
   - Gestión de pedidos activos
   - Actualización de estados del workflow
   - Visualización de tiempos promedio

---

## 🏗️ Arquitectura

### Stack Tecnológico
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Hosting**: AWS Amplify
- **API**: Integración con AWS API Gateway
- **Actualización**: Tiempo real mediante polling

### Estructura de Archivos

```
frontend/
├── client/                      # Aplicación del Cliente
│   ├── index.html              # Página principal
│   ├── styles.css              # Estilos CSS
│   ├── app.js                  # Lógica de la aplicación
│   └── config.js               # Configuración del API
│
├── restaurant/                  # Aplicación del Restaurante
│   ├── index.html              # Dashboard principal
│   ├── styles.css              # Estilos CSS
│   ├── app.js                  # Lógica del dashboard
│   └── config.js               # Configuración del API
│
├── amplify.yml                 # Configuración de Amplify
└── README.md                   # Este archivo
```

---

## 🚀 Configuración e Instalación

### Paso 1: Desplegar el Backend

Primero debes desplegar el backend serverless:

```bash
cd ../backend/src
serverless deploy --stage dev
```

Esto te dará una **URL del API Gateway**. Por ejemplo:
```
https://abc123xyz.execute-api.us-east-1.amazonaws.com
```

### Paso 2: Configurar las URLs del API

Edita los archivos `config.js` en ambas aplicaciones y reemplaza la URL:

**`frontend/client/config.js`:**
```javascript
const API_CONFIG = {
    baseURL: 'https://TU_API_GATEWAY_URL',  // ← Reemplazar
    tenantId: 'pardos-chicken'
};
```

**`frontend/restaurant/config.js`:**
```javascript
const API_CONFIG = {
    baseURL: 'https://TU_API_GATEWAY_URL',  // ← Reemplazar
    tenantId: 'pardos-chicken'
};
```

### Paso 3: Probar Localmente

Puedes probar las aplicaciones localmente usando cualquier servidor HTTP:

**Opción 1: Python**
```bash
# Aplicación de Cliente
cd frontend/client
python3 -m http.server 8000

# Aplicación de Restaurante (en otra terminal)
cd frontend/restaurant
python3 -m http.server 8001
```

**Opción 2: Node.js (http-server)**
```bash
# Instalar http-server
npm install -g http-server

# Aplicación de Cliente
cd frontend/client
http-server -p 8000

# Aplicación de Restaurante
cd frontend/restaurant
http-server -p 8001
```

Luego abre:
- Cliente: http://localhost:8000
- Restaurante: http://localhost:8001

### Paso 4: Desplegar en AWS Amplify

#### Opción A: Desde la Consola de AWS

1. Ve a AWS Amplify Console
2. Haz clic en "New app" → "Host web app"
3. Conecta tu repositorio de GitHub
4. Configura las rutas:
   - App 1: `frontend/client`
   - App 2: `frontend/restaurant`
5. Haz deploy

#### Opción B: Usando Amplify CLI

```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Configurar Amplify
amplify configure

# Inicializar proyecto
cd frontend/client
amplify init

# Agregar hosting
amplify add hosting

# Publicar
amplify publish
```

---

## 📖 Guía de Uso

### Aplicación de Cliente

#### 1. Hacer un Pedido

1. Navega a la aplicación de cliente
2. Selecciona productos del menú usando los botones +/-
3. Llena los datos de entrega:
   - Nombre
   - Teléfono
   - Dirección
4. Haz clic en "Hacer Pedido"
5. **Guarda el ID del pedido** que se muestra

#### 2. Rastrear Pedido

1. Ingresa tu ID de pedido en el campo "Rastrear mi Pedido"
2. Haz clic en "Rastrear"
3. Verás:
   - Estado actual
   - Timeline completo
   - Quién atendió cada paso
   - Tiempos transcurridos
   - Tiempo estimado restante

---

### Aplicación de Restaurante

#### 1. Dashboard Principal

El dashboard muestra:
- **Total de pedidos**
- **Pedidos en proceso**
- **Pedidos completados**
- **Tiempo promedio total** de entrega
- **Tiempos promedio** por fase:
  - Cocina
  - Empaque
  - Entrega

#### 2. Gestionar Pedidos Activos

**Filtros disponibles:**
- Todos
- Recibidos
- En Cocina
- Empacando
- En Camino

**Para actualizar un pedido:**

1. Busca el pedido en la lista
2. Haz clic en "Actualizar Estado"
3. Selecciona:
   - Nuevo estado (solo estados válidos se muestran)
   - Tu nombre
   - Tu rol (Cocinero, Despachador, Repartidor)
4. Haz clic en "Actualizar Estado"

**Estados válidos y flujo:**
```
RECEIVED → COOKING → PACKING → DELIVERING → DELIVERED
```

**Roles esperados:**
- `COOKING`: Cocinero (KITCHEN_STAFF)
- `PACKING`: Despachador (PACKER)
- `DELIVERING`: Repartidor (DELIVERY_DRIVER)
- `DELIVERED`: Repartidor (DELIVERY_DRIVER)

#### 3. Ver Detalles

Haz clic en "Ver Detalles" en cualquier pedido para ver:
- Timeline completo
- Tiempos transcurridos
- Personal que atendió cada paso

#### 4. Historial Reciente

La sección "Pedidos Recientes" muestra los últimos 10 pedidos con:
- Estado actual
- Tiempos de cada fase
- Tiempo total (si está completado)

---

## 🎨 Características del Frontend

### Aplicación de Cliente

✅ **Diseño Responsivo**
- Se adapta a móviles, tablets y desktop
- Interfaz intuitiva y fácil de usar

✅ **Menú Dinámico**
- Carga automática desde el backend
- Categorización de productos
- Precios actualizados

✅ **Carrito de Compras**
- Agregar/quitar productos
- Visualización de subtotales
- Total calculado automáticamente

✅ **Rastreo en Tiempo Real**
- Timeline visual del pedido
- Indicadores de estado con colores
- Métricas de tiempo

✅ **Notificaciones**
- Confirmación de pedido creado
- Errores y advertencias
- Auto-hide después de 5 segundos

### Aplicación de Restaurante

✅ **Dashboard en Tiempo Real**
- Auto-refresh cada 30 segundos
- Estadísticas actualizadas
- Métricas de rendimiento

✅ **Gestión de Pedidos**
- Vista de tarjetas organizadas
- Filtrado por estado
- Actualización rápida de estados

✅ **Validación de Flujo**
- Solo muestra estados válidos
- Previene transiciones incorrectas
- Sugiere roles apropiados

✅ **Visualización de Métricas**
- Gráficos de tiempo promedio
- Timeline de pedidos recientes
- Detalles de cada fase

---

## 🎨 Paleta de Colores

```css
--primary-color: #e63946   (Rojo Pardos)
--secondary-color: #f77f00 (Naranja)
--success-color: #06d6a0   (Verde)
--warning-color: #ffd60a   (Amarillo)
--dark: #1d3557            (Azul Oscuro)
--light: #f1faee           (Blanco Roto)
--gray: #a8dadc            (Gris Claro)
```

### Estados con Colores

| Estado | Color | Significado |
|--------|-------|-------------|
| RECEIVED | Amarillo | Pedido recibido, esperando cocina |
| COOKING | Naranja | En preparación |
| PACKING | Azul | Empacando pedido |
| DELIVERING | Púrpura | En camino al cliente |
| DELIVERED | Verde | Entregado exitosamente |

---

## 🔧 Personalización

### Cambiar el Tenant

Si quieres usar otro tenant (restaurante):

```javascript
// En config.js
const API_CONFIG = {
    baseURL: 'https://...',
    tenantId: 'mi-restaurante'  // ← Cambiar aquí
};
```

### Agregar Productos al Menú

Usa el endpoint `PUT /tenants/{tenantId}/menu`:

```javascript
fetch(`${API_URL}/tenants/pardos-chicken/menu`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        product_id: 'prod-7',
        name: 'Nuevo Producto',
        price: 20.00,
        category: 'Categoría'
    })
});
```

### Modificar Tiempos Estimados

En `frontend/client/app.js`, busca la función de tiempo estimado:

```javascript
// Tiempos promedio estimados por fase (en minutos)
const avg_times = {
    "RECEIVED": 10,   // ← Ajustar
    "COOKING": 20,    // ← Ajustar
    "PACKING": 5,     // ← Ajustar
    "DELIVERING": 30  // ← Ajustar
};
```

---

## 🐛 Troubleshooting

### Error: "Failed to fetch"

**Causa**: La URL del API Gateway no está configurada o es incorrecta.

**Solución**:
1. Verifica que `config.js` tenga la URL correcta
2. Asegúrate de que el backend esté desplegado
3. Revisa CORS en el API Gateway

### Error: "Order not found"

**Causa**: El ID del pedido es incorrecto o el pedido no existe.

**Solución**:
1. Verifica el ID del pedido
2. Asegúrate de usar el tenant correcto

### El menú no carga

**Causa**: No hay productos en la base de datos.

**Solución**:
1. Agrega productos usando el endpoint PUT `/tenants/{tenantId}/menu`
2. O usa el menú de ejemplo que se carga automáticamente en caso de error

### Los pedidos no se actualizan

**Causa**: Problemas de conexión con el backend.

**Solución**:
1. Haz clic en "Actualizar" manualmente
2. Verifica la URL del API en `config.js`
3. Revisa la consola del navegador para errores

---

## 📊 Integración con el Backend

### Endpoints Utilizados

#### Aplicación de Cliente

| Endpoint | Método | Uso |
|----------|--------|-----|
| `/tenants/{tenantId}/menu` | GET | Cargar menú |
| `/tenants/{tenantId}/orders` | POST | Crear pedido |
| `/tenants/{tenantId}/orders/{orderId}` | GET | Obtener pedido |
| `/tenants/{tenantId}/orders/{orderId}/metrics` | GET | Obtener métricas |

#### Aplicación de Restaurante

| Endpoint | Método | Uso |
|----------|--------|-----|
| `/tenants/{tenantId}/dashboard` | GET | Obtener dashboard |
| `/tenants/{tenantId}/orders` | GET | Listar pedidos |
| `/tenants/{tenantId}/orders/{orderId}/step` | POST | Actualizar estado |
| `/tenants/{tenantId}/orders/{orderId}/metrics` | GET | Ver detalles |

---

## 🚀 Mejoras Futuras

### Funcionalidades Pendientes

- [ ] Autenticación de usuarios
- [ ] WebSockets para actualización en tiempo real
- [ ] Notificaciones push
- [ ] Exportar reportes en PDF
- [ ] Gestión de menú desde la UI
- [ ] Integración con pasarelas de pago
- [ ] Tracking GPS del repartidor
- [ ] Calificación de pedidos
- [ ] Sistema de cupones y descuentos

### Optimizaciones Técnicas

- [ ] Service Workers para modo offline
- [ ] Cache de datos locales
- [ ] Optimización de imágenes
- [ ] Lazy loading de componentes
- [ ] Bundle optimization (migrar a React/Vue)
- [ ] Tests unitarios e integración

---

## 📝 Licencia

Este proyecto es parte de un laboratorio académico de Cloud Computing.

---

## 👥 Equipo

**Grupo 4 - Pardos Chicken**
Laboratorio de Cloud Computing
Universidad: 2025-2

---

## 📞 Soporte

Para reportar issues o sugerencias:
1. Abre un issue en el repositorio de GitHub
2. Describe el problema con capturas de pantalla
3. Incluye logs de la consola del navegador

---

**Última actualización**: 2025-11-22
**Versión**: 1.0.0
**Estado**: Producción Ready ✅
