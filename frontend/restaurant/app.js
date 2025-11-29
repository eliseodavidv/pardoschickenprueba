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

// Crear tarjeta de orden mejorada
function createOrderCard(order) {
    const card = document.createElement('div');
    card.className = 'order-card';
    card.dataset.orderId = order.order_id;

    // Calcular tiempo transcurrido
    const createdDate = new Date(order.created_at);
    const now = new Date();
    const minutesElapsed = Math.floor((now - createdDate) / 1000 / 60);

    const createdTimeStr = createdDate.toLocaleString('es-PE', {
        hour: '2-digit',
        minute: '2-digit'
    });

    // Determinar urgencia por tiempo
    let urgencyClass = '';
    if (minutesElapsed > 60) urgencyClass = 'urgent';
    else if (minutesElapsed > 30) urgencyClass = 'warning';

    let itemsList = '';
    let totalItems = 0;
    if (order.items && order.items.length > 0) {
        itemsList = '<div class="order-items-list">';
        order.items.forEach(item => {
            totalItems += item.quantity;
            itemsList += `
                <div class="order-item">
                    <span class="item-quantity">${item.quantity}x</span>
                    <span class="item-name">${item.name}</span>
                </div>
            `;
        });
        itemsList += '</div>';
    }

    // Botón de acción rápida según el estado
    let quickActionBtn = '';
    const nextStates = {
        'RECEIVED': { status: 'COOKING', label: '👨‍🍳 Iniciar Cocina', role: 'KITCHEN_STAFF' },
        'COOKING': { status: 'PACKING', label: '📦 Empacar', role: 'PACKER' },
        'PACKING': { status: 'DELIVERING', label: '🚗 Enviar', role: 'DELIVERY_DRIVER' },
        'DELIVERING': { status: 'DELIVERED', label: '✅ Entregar', role: 'DELIVERY_DRIVER' }
    };

    if (nextStates[order.status]) {
        const next = nextStates[order.status];
        quickActionBtn = `
            <button class="btn btn-quick-action" onclick="quickUpdateStatus('${order.order_id}', '${next.status}', '${next.role}')">
                ${next.label}
            </button>
        `;
    }

    card.innerHTML = `
        <div class="order-card-inner ${urgencyClass}">
            <div class="order-header" onclick="toggleOrderDetails('${order.order_id}')">
                <div class="order-title">
                    <span class="order-id">📋 #${order.order_id.substring(0, 8)}</span>
                    <span class="order-time ${urgencyClass}"">⏱️ ${minutesElapsed} min</span>
                </div>
                <span class="status-badge status-${order.status}">${getStatusText(order.status)}</span>
            </div>

            <div class="order-customer" onclick="toggleOrderDetails('${order.order_id}')">
                <div class="customer-name">👤 ${order.customer_name}</div>
                <div class="customer-address">📍 ${order.customer_address}</div>
                ${order.customer_phone ? `<div class="customer-phone">📞 ${order.customer_phone}</div>` : ''}
            </div>

            <div class="order-summary" onclick="toggleOrderDetails('${order.order_id}')">
                <span class="items-count">🍽️ ${totalItems} producto${totalItems !== 1 ? 's' : ''}</span>
                <span class="order-created">🕐 ${createdTimeStr}</span>
            </div>

            <div class="order-items-section" id="items-${order.order_id}" style="display: none;">
                <div class="items-header">📝 Detalles del Pedido:</div>
                ${itemsList}
            </div>

            <div class="order-actions">
                ${quickActionBtn}
                <button class="btn btn-details" onclick="viewOrderDetails('${order.order_id}')">
                    📊 Ver Timeline
                </button>
            </div>
        </div>
    `;

    return card;
}

// Toggle para mostrar/ocultar items
function toggleOrderDetails(orderId) {
    const itemsSection = document.getElementById(`items-${orderId}`);
    if (itemsSection) {
        const isVisible = itemsSection.style.display !== 'none';
        itemsSection.style.display = isVisible ? 'none' : 'block';

        // Animar la transición
        if (!isVisible) {
            itemsSection.style.maxHeight = '0';
            setTimeout(() => {
                itemsSection.style.maxHeight = '500px';
            }, 10);
        }
    }
}

// Actualización rápida de estado
async function quickUpdateStatus(orderId, newStatus, role) {
    const userName = localStorage.getItem('restaurantUser') || 'admin';

    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${orderId}/step`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    status: newStatus,
                    by: userName,
                    by_role: role
                })
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Error al actualizar el estado');
        }

        showNotification(
            `✅ Pedido actualizado a ${getStatusText(newStatus)}`,
            'success'
        );

        // Animar la tarjeta antes de actualizar
        const card = document.querySelector(`[data-order-id="${orderId}"]`);
        if (card) {
            card.style.transform = 'scale(0.95)';
            card.style.opacity = '0.5';
        }

        setTimeout(refreshDashboard, 500);

    } catch (error) {
        console.error('Error updating order:', error);
        showNotification(`❌ Error: ${error.message}`, 'error');
    }
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
                    by: attendedBy,
                    by_role: role
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

// Ver detalles de la orden con modal mejorado
async function viewOrderDetails(orderId) {
    try {
        const response = await fetch(
            `${API_CONFIG.baseURL}/tenants/${API_CONFIG.tenantId}/orders/${orderId}/metrics`
        );

        if (!response.ok) throw new Error('Error al cargar detalles');

        const metrics = await response.json();

        // Crear modal personalizado para timeline
        let timelineHTML = '<div class="timeline-modal">';
        timelineHTML += `<h3>📊 Timeline del Pedido #${orderId.substring(0, 8)}</h3>`;
        timelineHTML += `<div class="timeline-info">`;
        timelineHTML += `<p><strong>Cliente:</strong> ${metrics.customer_name}</p>`;
        timelineHTML += `<p><strong>Estado:</strong> <span class="status-badge status-${metrics.current_status}">${getStatusText(metrics.current_status)}</span></p>`;
        timelineHTML += `</div>`;

        if (metrics.timeline && metrics.timeline.length > 0) {
            timelineHTML += '<div class="timeline-steps">';
            metrics.timeline.forEach((event, index) => {
                const time = new Date(event.timestamp).toLocaleTimeString('es-PE');
                timelineHTML += `
                    <div class="timeline-step ${index === metrics.timeline.length - 1 ? 'current' : ''}">
                        <div class="step-marker">${index + 1}</div>
                        <div class="step-content">
                            <div class="step-status">${getStatusText(event.status)}</div>
                            <div class="step-details">
                                ${event.attended_by} - ${time}
                            </div>
                        </div>
                    </div>
                `;
            });
            timelineHTML += '</div>';
        }

        if (metrics.total_time) {
            timelineHTML += `<div class="timeline-summary">`;
            timelineHTML += `<p><strong>⏱️ Tiempo total:</strong> ${metrics.total_time.minutes} minutos</p>`;
            if (metrics.estimated_remaining_time) {
                timelineHTML += `<p><strong>⏳ Tiempo estimado restante:</strong> ${metrics.estimated_remaining_time.minutes} minutos</p>`;
            }
            timelineHTML += `</div>`;
        }

        timelineHTML += '</div>';

        // Mostrar en alert mejorado (temporal, se puede mejorar con un modal)
        const detailsModal = document.createElement('div');
        detailsModal.className = 'details-modal-overlay';
        detailsModal.innerHTML = `
            <div class="details-modal-content">
                ${timelineHTML}
                <button class="btn btn-close" onclick="this.closest('.details-modal-overlay').remove()">Cerrar</button>
            </div>
        `;
        document.body.appendChild(detailsModal);

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

// Función para cerrar sesión
function logout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        localStorage.removeItem('restaurantAuth');
        localStorage.removeItem('restaurantUser');
        window.location.href = '../restaurant-login.html';
    }
}
