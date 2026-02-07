/**
 * GeoPortal Porto Velho - Main JavaScript
 */

// Utility Functions
const GeoPortal = {
    // Format numbers with Brazilian locale
    formatNumber: function (num) {
        return new Intl.NumberFormat('pt-BR').format(num);
    },

    // Format area in hectares
    formatArea: function (ha) {
        return this.formatNumber(Math.round(ha)) + ' ha';
    },

    // Format date
    formatDate: function (dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('pt-BR');
    },

    // API helper
    fetchAPI: async function (endpoint) {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error('API Error');
            return await response.json();
        } catch (error) {
            console.error('API fetch error:', error);
            return null;
        }
    },

    // Create Leaflet map with default settings
    createMap: function (elementId, options = {}) {
        const defaults = {
            center: [-8.76, -63.90],
            zoom: 10,
            zoomControl: true,
            scrollWheelZoom: true
        };

        const config = { ...defaults, ...options };
        const map = L.map(elementId, config);

        // Add default base layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);

        // Add scale control
        L.control.scale({
            metric: true,
            imperial: false,
            position: 'bottomleft'
        }).addTo(map);

        return map;
    },

    // Add WMS layer
    addWMSLayer: function (map, layerName, options = {}) {
        const defaults = {
            format: 'image/png',
            transparent: true,
            attribution: 'Observatório de Conflitos Socioambientais e Direitos Humanos - PVH'
        };

        const geoserverUrl = window.GEOSERVER_URL || '/geoserver';

        return L.tileLayer.wms(`${geoserverUrl}/pvh/wms`, {
            layers: `pvh:${layerName}`,
            ...defaults,
            ...options
        }).addTo(map);
    },

    // Create Chart.js chart with defaults
    createChart: function (ctx, type, data, options = {}) {
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== null) {
                                label += GeoPortal.formatNumber(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        };

        return new Chart(ctx, {
            type: type,
            data: data,
            options: { ...defaultOptions, ...options }
        });
    },

    // Color palette for charts
    colors: {
        red: 'rgba(220, 53, 69, 0.7)',
        redBorder: 'rgba(220, 53, 69, 1)',
        yellow: 'rgba(255, 193, 7, 0.7)',
        yellowBorder: 'rgba(255, 193, 7, 1)',
        orange: 'rgba(255, 87, 34, 0.7)',
        orangeBorder: 'rgba(255, 87, 34, 1)',
        green: 'rgba(40, 167, 69, 0.7)',
        greenBorder: 'rgba(40, 167, 69, 1)',
        blue: 'rgba(13, 110, 253, 0.7)',
        blueBorder: 'rgba(13, 110, 253, 1)',
        gray: 'rgba(108, 117, 125, 0.7)',
        grayBorder: 'rgba(108, 117, 125, 1)'
    },

    // Show loading spinner
    showLoading: function (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center align-items-center h-100">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
            </div>
        `;
    },

    // Show error message
    showError: function (element, message = 'Erro ao carregar dados') {
        element.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="bi bi-exclamation-triangle"></i> ${message}
            </div>
        `;
    }
};

// Initialize tooltips and popovers on page load
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // Initialize Bootstrap popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    popoverTriggerList.forEach(el => new bootstrap.Popover(el));

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    console.log('GeoPortal Porto Velho initialized');
});

// Export for use in templates
window.GeoPortal = GeoPortal;
