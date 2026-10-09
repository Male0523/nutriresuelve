// Nombre de la clave en el almacenamiento local del navegador
const QUEUE_KEY = 'nutriguajira_offline_queue';

// 1. Ejecutar la sincronización automáticamente al cargar la página si hay elementos pendientes
document.addEventListener('DOMContentLoaded', () => {
    sincronizarPendientes();
});

// 2. Escuchar cuando el navegador recupera la conexión a la red en tiempo real
window.addEventListener('online', () => {
    console.log("Conexión restablecida. Sincronizando datos con el servidor...");
    sincronizarPendientes();
});

// 3. Interceptor global para envíos de formularios (Soporta red offline y servidor caído)
document.addEventListener('submit', async function (event) {
    const form = event.target;
    const actionUrl = form.getAttribute('action') || window.location.pathname;
    const method = (form.method || 'POST').toUpperCase();
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Si el navegador marca explícitamente offline, guardamos localmente de inmediato
    if (!navigator.onLine) {
        event.preventDefault(); // Evita la navegación del navegador
        registrarEnvioOffline(actionUrl, method, data);
        form.reset();
        return;
    }

    // Si la red marca online pero el servidor está inalcanzable (ej: Django apagado o error de red)
    event.preventDefault(); // Detiene el envío síncrono del navegador

    try {
        const response = await fetch(actionUrl, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("¡Registro guardado con éxito en el servidor!");
            window.location.href = actionUrl.includes('registrar') ? '/pacientes/' : window.location.pathname;
        } else {
            console.error("Error en el servidor al procesar la solicitud:", response.statusText);
            alert("Ocurrió un error en el servidor al procesar los datos.");
        }
    } catch (error) {
        // Entra aquí si falla la petición por falta de servidor (ERR_CONNECTION_REFUSED) o timeout
        console.warn("Servidor no disponible. Guardando datos en modo offline local...", error);
        registrarEnvioOffline(actionUrl, method, data);
        form.reset();
    }
});

// 4. Función para guardar envíos en localStorage
function registrarEnvioOffline(url, method, data) {
    const queue = JSON.parse(localStorage.getItem(QUEUE_KEY) || '[]');
    queue.push({ url, method, data, timestamp: new Date().toISOString() });
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
    
    alert("⚠️ Servidor o red no disponible. Los datos se guardaron localmente en el navegador y se enviarán automáticamente en cuanto el sistema vuelva a estar en línea.");
}

// 5. Sincronizar peticiones guardadas con el servidor Django
async function sincronizarPendientes() {
    const queue = JSON.parse(localStorage.getItem(QUEUE_KEY) || '[]');
    if (queue.length === 0) return;

    console.log(`Iniciando sincronización de ${queue.length} elementos pendientes...`);
    const pendientesActualizados = [];

    for (const item of queue) {
        try {
            const response = await fetch(item.url, {
                method: item.method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(item.data)
            });

            // Si la respuesta no fue exitosa (código 4xx o 5xx), mantenemos el ítem en la cola
            if (!response.ok) {
                console.error(`Error al sincronizar elemento en ${item.url}:`, response.statusText);
                pendientesActualizados.push(item);
            }
        } catch (error) {
            console.error(`Fallo de red durante la sincronización en ${item.url}:`, error);
            pendientesActualizados.push(item);
        }
    }

    // Actualizar localStorage con las peticiones que no pudieron enviarse
    localStorage.setItem(QUEUE_KEY, JSON.stringify(pendientesActualizados));

    if (pendientesActualizados.length === 0) {
        alert("¡Todos los datos guardados en modo offline han sido sincronizados con éxito!");
        window.location.reload(); // Recargar la página para visualizar los nuevos registros en la interfaz
    }
}

// 6. Función auxiliar para obtener la cookie CSRF que exige Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}