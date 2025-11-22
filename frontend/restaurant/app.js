// Estado de la aplicación
let dashboardData = null;
let allOrders = [];
let currentFilter = 'all';
let selectedOrder = null;

// Cargar dashboard al iniciar
document.addEventListener('DOMContentLoaded', () => {
    refreshDashboard();
    setupUpdateForm();
    // Auto-refresh cada 30 segundos
    setInterval(refreshDashboard, 30000);
});

// Refrescar dashboard
async function refreshDashboard() {
    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/dashboard`
        );

        if (!response.ok) throw new Error('Error al cargar dashboard');

        dashboardData = await response.json();
        updateHeaderStats();
        updateMetrics();
        loadAllOrders();
        displayRecentOrders();

    } catch (error) {
        console.error('Error loading dashboard:', error);
        showNotification('Error al cargar el dashboard', 'error');
    }
}

// Actualizar estadísticas del header
function updateHeaderStats() {
    if (!dashboardData) return;

    document.getElementById('total-orders').textContent = dashboardData.total_orders || 0;
    document.getElementById('in-progress-orders').textContent = dashboardData.in_progress_orders || 0;
    document.getElementById('completed-orders').textContent = dashboardData.completed_orders || 0;
}

// Actualizar métricas de tiempo
function updateMetrics() {
    if (!dashboardData || !dashboardData.average_times) return;

    const avgTimes = dashboardData.average_times;

    document.getElementById('avg-total-time').textContent =
        `${avgTimes.total_delivery_minutes || 0} min`;

    document.getElementById('avg-cooking-time').textContent =
        `${avgTimes.phases.cooking_minutes || 0} min`;

    document.getElementById('avg-packing-time').textContent =
        `${avgTimes.phases.packing_minutes || 0} min`;

    document.getElementById('avg-delivery-time').textContent =
        `${avgTimes.phases.delivering_minutes || 0} min`;
}

// Cargar todas las órdenes
async function loadAllOrders() {
    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders`
        );

        if (!response.ok) throw new Error('Error al cargar órdenes');

        allOrders = await response.json();
        displayOrders();

    } catch (error) {
        console.error('Error loading orders:', error);
        showNotification('Error al cargar las órdenes', 'error');
    }
}

// Mostrar órdenes según el filtro
function displayOrders() {
    const container = document.getElementById('orders-container');

    let filteredOrders = allOrders;
    if (currentFilter !== 'all') {
        filteredOrders = allOrders.filter(order => order.status === currentFilter);
    }

    // Filtrar solo órdenes no completadas
    filteredOrders = filteredOrders.filter(order => order.status !== 'DELIVERED');

    if (filteredOrders.length === 0) {
        container.innerHTML = '<p class="loading">No hay pedidos activos</p>';
        return;
    }

    container.innerHTML = '';

    filteredOrders.forEach(order => {
        const orderCard = createOrderCard(order);
        container.appendChild(orderCard);
    });
}

// Crear tarjeta de orden
function createOrderCard(order) {
    const card = document.createElement('div');
    card.className = 'order-card';

    const createdDate = new Date(order.created_at).toLocaleString('es-PE', {
        dateStyle: 'short',
        timeStyle: 'short'
    });

    let itemsList = '';
    if (order.items && order.items.length > 0) {
        itemsList = '<ul>';
        order.items.forEach(item => {
            itemsList += `<li>${item.name} x ${item.quantity}</li>`;
        });
        itemsList += '</ul>';
    }

    card.innerHTML = `
        <div class="order-header">
            <span class="order-id">Pedido #${order.order_id.substring(0, 8)}</span>
            <span class="status-badge status-${order.status}">${getStatusText(order.status)}</span>
        </div>
        <div class="order-details">
            <p><strong>Cliente:</strong> ${order.customer_name}</p>
            <p><strong>Dirección:</strong> ${order.customer_address}</p>
            <p><strong>Teléfono:</strong> ${order.customer_phone || 'N/A'}</p>
            <p><strong>Creado:</strong> ${createdDate}</p>
            ${itemsList ? `<div class="order-items">${itemsList}</div>` : ''}
        </div>
        <div class="order-actions">
            <button class="btn btn-primary" onclick='openUpdateModal(${JSON.stringify(order)})'>
                Actualizar Estado
            </button>
            <button class="btn btn-secondary" onclick="viewOrderDetails('${order.order_id}')">
                Ver Detalles
            </button>
        </div>
    `;

    return card;
}

// Mostrar pedidos recientes
function displayRecentOrders() {
    if (!dashboardData || !dashboardData.recent_orders) return;

    const container = document.getElementById('recent-orders');
    container.innerHTML = '';

    dashboardData.recent_orders.forEach(order => {
        const item = document.createElement('div');
        item.className = 'timeline-item';

        let phasesHTML = '';
        if (order.phases) {
            phasesHTML = '<div class="timeline-phases">';
            for (const [phase, data] of Object.entries(order.phases)) {
                phasesHTML += `<span class="phase-badge">${getStatusText(phase.toUpperCase())}: ${data.time_from_creation_minutes} min</span>`;
            }
            phasesHTML += '</div>';
        }

        item.innerHTML = `
            <div class="timeline-content">
                <h4>Pedido #${order.order_id.substring(0, 8)}</h4>
                <p><span class="status-badge status-${order.status}">${getStatusText(order.status)}</span></p>
                <p><strong>Creado:</strong> ${new Date(order.created_at).toLocaleString('es-PE')}</p>
                ${order.total_time_minutes ? `<p><strong>Tiempo Total:</strong> ${order.total_time_minutes} minutos</p>` : ''}
                ${phasesHTML}
            </div>
        `;

        container.appendChild(item);
    });
}

// Cambiar tab de filtro
function showTab(filter) {
    currentFilter = filter;

    // Actualizar tabs activos
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');

    displayOrders();
}

// Abrir modal de actualización
function openUpdateModal(order) {
    selectedOrder = order;
    const modal = document.getElementById('updateModal');
    const modalInfo = document.getElementById('modal-order-info');

    modalInfo.innerHTML = `
        <p><strong>Pedido:</strong> #${order.order_id.substring(0, 8)}</p>
        <p><strong>Cliente:</strong> ${order.customer_name}</p>
        <p><strong>Estado Actual:</strong> <span class="status-badge status-${order.status}">${getStatusText(order.status)}</span></p>
    `;

    // Actualizar opciones de estado según el estado actual
    updateStateOptions(order.status);

    modal.classList.add('show');
}

// Cerrar modal
function closeUpdateModal() {
    const modal = document.getElementById('updateModal');
    modal.classList.remove('show');
    selectedOrder = null;
    document.getElementById('update-form').reset();
}

// Actualizar opciones de estado según el estado actual
function updateStateOptions(currentStatus) {
    const select = document.getElementById('new_status');
    const options = {
        'RECEIVED': ['COOKING'],
        'COOKING': ['PACKING'],
        'PACKING': ['DELIVERING'],
        'DELIVERING': ['DELIVERED'],
        'DELIVERED': []
    };

    const validNextStates = options[currentStatus] || [];

    select.innerHTML = '<option value="">Seleccionar...</option>';

    validNextStates.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = getStatusText(state);
        select.appendChild(option);
    });
}

// Configurar formulario de actualización
function setupUpdateForm() {
    const form = document.getElementById('update-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await updateOrderStatus();
    });
}

// Actualizar estado del pedido
async function updateOrderStatus() {
    if (!selectedOrder) return;

    const newStatus = document.getElementById('new_status').value;
    const attendedBy = document.getElementById('attended_by').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${selectedOrder.order_id}/step`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    status: newStatus,
                    attended_by: attendedBy,
                    role: role
                })
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Error al actualizar el estado');
        }

        const result = await response.json();

        showNotification(
            `Estado actualizado exitosamente a ${getStatusText(newStatus)}`,
            'success'
        );

        closeUpdateModal();

        // Refrescar dashboard después de 1 segundo
        setTimeout(refreshDashboard, 1000);

    } catch (error) {
        console.error('Error updating order:', error);
        showNotification(`Error: ${error.message}`, 'error');
    }
}

// Ver detalles de la orden
async function viewOrderDetails(orderId) {
    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${orderId}/metrics`
        );

        if (!response.ok) throw new Error('Error al cargar detalles');

        const metrics = await response.json();

        // Mostrar detalles en una notificación grande
        let details = `📦 Pedido #${orderId.substring(0, 8)}\n\n`;
        details += `Estado: ${getStatusText(metrics.current_status)}\n`;
        details += `Cliente: ${metrics.customer_name}\n\n`;

        if (metrics.timeline && metrics.timeline.length > 0) {
            details += `Timeline:\n`;
            metrics.timeline.forEach(event => {
                details += `• ${getStatusText(event.status)} - ${event.attended_by} (${new Date(event.timestamp).toLocaleTimeString('es-PE')})\n`;
            });
        }

        if (metrics.total_time) {
            details += `\nTiempo total: ${metrics.total_time.minutes} minutos`;
        }

        if (metrics.estimated_remaining_time) {
            details += `\nTiempo estimado restante: ${metrics.estimated_remaining_time.minutes} minutos`;
        }

        alert(details);

    } catch (error) {
        console.error('Error loading order details:', error);
        showNotification('Error al cargar los detalles', 'error');
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

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('updateModal');
    if (event.target === modal) {
        closeUpdateModal();
    }
}
