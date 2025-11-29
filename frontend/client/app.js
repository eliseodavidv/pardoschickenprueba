// Estado de la aplicación
let menu = [];
let cart = [];
let currentOrderId = null;

// Cargar menú al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadMenu();
    setupOrderForm();
});

// Cargar menú desde el API
async function loadMenu() {
    try {
        const response = await fetch(`${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/menu`);
        if (!response.ok) throw new Error('Error al cargar el menú');

        menu = await response.json();
        displayMenu();
    } catch (error) {
        console.error('Error loading menu:', error);
        showNotification('Error al cargar el menú. Usando menú de ejemplo.', 'error');
        // Menú de ejemplo con imágenes
        menu = [
            { product_id: '1', name: 'Pollo Entero', price: 62.90, category: 'Pollos', description: 'Pollo a la brasa entero con papas y ensalada', image_url: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=500&q=80' },
            { product_id: '2', name: '1/2 Pollo', price: 35.90, category: 'Pollos', description: 'Medio pollo a la brasa con papas y ensalada', image_url: 'https://images.unsplash.com/photo-1594221708779-94832f4320d1?w=500&q=80' },
            { product_id: '3', name: '1/4 Pollo', price: 21.90, category: 'Pollos', description: 'Cuarto de pollo a la brasa con papas y ensalada', image_url: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80' },
            { product_id: '4', name: 'Parrilla Personal', price: 42.90, category: 'Parrillas', description: 'Anticuchos, chorizo, mollejitas y papas', image_url: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80' },
            { product_id: '5', name: 'Anticuchos (3 unid)', price: 18.90, category: 'Entradas', description: 'Anticuchos de corazón con papa y choclo', image_url: 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500&q=80' },
            { product_id: '6', name: 'Inca Kola 1.5L', price: 8.90, category: 'Bebidas', description: 'Gaseosa Inca Kola de 1.5 litros', image_url: 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=500&q=80' },
            { product_id: '7', name: 'Ensalada César', price: 24.90, category: 'Ensaladas', description: 'Lechuga, pollo, crutones y aderezo césar', image_url: 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=500&q=80' },
            { product_id: '8', name: 'Brownie con Helado', price: 14.90, category: 'Postres', description: 'Brownie de chocolate con helado de vainilla', image_url: 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80' }
        ];
        displayMenu();
    }
}

// Mostrar menú en la interfaz
function displayMenu() {
    const container = document.getElementById('menu-container');
    container.innerHTML = '';

    menu.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'menu-item';

        // Imagen por defecto si no tiene image_url
        const imageUrl = item.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80';

        itemDiv.innerHTML = `
            ${item.image_url ? `<div class="menu-item-image" style="background-image: url('${imageUrl}')"></div>` : ''}
            <div class="menu-item-content">
                <h3>${item.name}</h3>
                <span class="category">${item.category || 'General'}</span>
                ${item.description ? `<p class="description">${item.description}</p>` : ''}
                <p class="price">S/ ${Number(item.price).toFixed(2)}</p>
                <div class="quantity-controls">
                    <button onclick="decreaseQuantity('${item.product_id}')">-</button>
                    <span id="qty-${item.product_id}">0</span>
                    <button onclick="increaseQuantity('${item.product_id}')">+</button>
                </div>
            </div>
        `;
        container.appendChild(itemDiv);
    });
}

// Aumentar cantidad
function increaseQuantity(productId) {
    const product = menu.find(p => p.product_id === productId);
    const existing = cart.find(item => item.product_id === productId);

    if (existing) {
        existing.quantity++;
    } else {
        cart.push({
            product_id: productId,
            name: product.name,
            price: product.price,
            quantity: 1
        });
    }

    updateQuantityDisplay(productId);
    updateCartSummary();
}

// Disminuir cantidad
function decreaseQuantity(productId) {
    const existing = cart.find(item => item.product_id === productId);

    if (existing) {
        existing.quantity--;
        if (existing.quantity === 0) {
            cart = cart.filter(item => item.product_id !== productId);
        }
    }

    updateQuantityDisplay(productId);
    updateCartSummary();
}

// Actualizar display de cantidad
function updateQuantityDisplay(productId) {
    const existing = cart.find(item => item.product_id === productId);
    const qtyElement = document.getElementById(`qty-${productId}`);
    qtyElement.textContent = existing ? existing.quantity : 0;
}

// Actualizar resumen del carrito
function updateCartSummary() {
    const cartSummary = document.getElementById('cart-summary');
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const orderForm = document.getElementById('order-form');

    if (cart.length === 0) {
        cartSummary.style.display = 'none';
        orderForm.style.display = 'none';
        return;
    }

    cartSummary.style.display = 'block';
    orderForm.style.display = 'block';

    let total = 0;
    cartItems.innerHTML = '';

    cart.forEach(item => {
        const subtotal = item.price * item.quantity;
        total += subtotal;

        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <span>${item.name} x ${item.quantity}</span>
            <span>S/ ${subtotal.toFixed(2)}</span>
        `;
        cartItems.appendChild(itemDiv);
    });

    cartTotal.textContent = total.toFixed(2);
}

// Configurar formulario de pedido
function setupOrderForm() {
    const form = document.getElementById('order-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await createOrder();
    });
}

// Crear pedido
async function createOrder() {
    if (cart.length === 0) {
        showNotification('Tu carrito está vacío', 'error');
        return;
    }

    const customerName = document.getElementById('customer_name').value;
    const customerPhone = document.getElementById('customer_phone').value;
    const customerEmail = document.getElementById('customer_email').value;
    const customerAddress = document.getElementById('customer_address').value;

    const orderData = {
        items: cart.map(item => ({
            product_id: item.product_id,
            name: item.name,
            quantity: item.quantity
            // price removido temporalmente por incompatibilidad con DynamoDB
        })),
        customer_name: customerName,
        customer_phone: customerPhone,
        customer_email: customerEmail,
        customer_address: customerAddress
    };

    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderData)
            }
        );

        if (!response.ok) throw new Error('Error al crear el pedido');

        const result = await response.json();
        currentOrderId = result.order_id;

        showNotification(
            `¡Pedido creado exitosamente! 🎉\nTu ID de pedido es: ${result.order_id}\n\nGuarda este ID para rastrear tu pedido.`,
            'success'
        );

        // Limpiar carrito y formulario
        cart = [];
        document.getElementById('order-form').reset();
        updateCartSummary();

        // Resetear cantidades en el menú
        menu.forEach(item => {
            document.getElementById(`qty-${item.product_id}`).textContent = '0';
        });

        // Mostrar automáticamente el estado del pedido
        document.getElementById('order_id_input').value = currentOrderId;
        setTimeout(() => trackOrder(), 1000);

    } catch (error) {
        console.error('Error creating order:', error);
        showNotification('Error al crear el pedido. Por favor intenta de nuevo.', 'error');
    }
}

// Rastrear pedido
async function trackOrder() {
    const orderId = document.getElementById('order_id_input').value.trim();

    if (!orderId) {
        showNotification('Por favor ingresa un ID de pedido', 'error');
        return;
    }

    try {
        // Obtener información del pedido
        const orderResponse = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${orderId}`
        );

        if (!orderResponse.ok) throw new Error('Pedido no encontrado');

        const order = await orderResponse.json();

        // Obtener métricas del pedido
        const metricsResponse = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${orderId}/metrics`
        );

        let metrics = null;
        if (metricsResponse.ok) {
            metrics = await metricsResponse.json();
        }

        displayOrderStatus(order, metrics);

    } catch (error) {
        console.error('Error tracking order:', error);
        showNotification('No se pudo encontrar el pedido. Verifica el ID.', 'error');
    }
}

// Mostrar estado del pedido
function displayOrderStatus(order, metrics) {
    const statusContainer = document.getElementById('order-status');
    const infoContainer = document.getElementById('order-info');
    const timelineContainer = document.getElementById('order-timeline');
    const metricsContainer = document.getElementById('order-metrics');

    statusContainer.style.display = 'block';

    // Información básica
    infoContainer.innerHTML = `
        <h3>Pedido #${order.order_id.substring(0, 8)}</h3>
        <p><strong>Cliente:</strong> ${order.customer_name}</p>
        <p><strong>Dirección:</strong> ${order.customer_address}</p>
        <p><strong>Estado Actual:</strong> <span class="status-badge status-${order.status}">${getStatusText(order.status)}</span></p>
        <p><strong>Creado:</strong> ${new Date(order.created_at).toLocaleString('es-PE')}</p>
    `;

    // Timeline
    if (metrics && metrics.timeline) {
        timelineContainer.innerHTML = '<h3>Progreso del Pedido</h3><div class="timeline">';

        metrics.timeline.forEach(event => {
            timelineContainer.innerHTML += `
                <div class="timeline-item">
                    <div class="timeline-content">
                        <strong>${getStatusText(event.status)}</strong>
                        <p>Atendido por: ${event.attended_by}</p>
                        <p>Rol: ${event.role}</p>
                        <small>${new Date(event.timestamp).toLocaleString('es-PE')}</small>
                    </div>
                </div>
            `;
        });

        timelineContainer.innerHTML += '</div>';
    }

    // Métricas de tiempo
    if (metrics) {
        metricsContainer.innerHTML = '<h3>Tiempos</h3><div class="metrics-grid">';

        if (metrics.total_time) {
            metricsContainer.innerHTML += `
                <div class="metric-card">
                    <h4>Tiempo Total</h4>
                    <div class="value">${metrics.total_time.minutes} min</div>
                </div>
            `;
        }

        if (metrics.estimated_remaining_time && !metrics.is_completed) {
            metricsContainer.innerHTML += `
                <div class="metric-card">
                    <h4>Tiempo Estimado</h4>
                    <div class="value">${metrics.estimated_remaining_time.minutes} min</div>
                </div>
            `;
        }

        metricsContainer.innerHTML += '</div>';
    }
}

// Convertir estado a texto legible
function getStatusText(status) {
    const statusTexts = {
        'RECEIVED': 'Recibido',
        'COOKING': 'En Cocina',
        'PACKING': 'Empacando',
        'DELIVERING': 'En Camino',
        'DELIVERED': 'Entregado'
    };
    return statusTexts[status] || status;
}

// Mostrar notificación
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.className = 'notification';
    }, 5000);
}
