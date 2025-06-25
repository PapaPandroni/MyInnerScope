/**
 * Main initialization for the progress page
 * Handles data setup and initializes all components
 */

class ProgressPage {
    constructor() {
        this.charts = null;
        this.init();
    }

    init() {
        this.setupData();
        this.initCharts();
        this.initTooltips();
    }

    /**
     * Setup data from the server
     */
    setupData() {
        // Get weekday data from the JSON script tag
        const weekdayDataElement = document.getElementById('weekday-data');
        const weekdayConfig = JSON.parse(weekdayDataElement.textContent);
        
        // Setup global data object for other modules to access
        window.progressData = {
            pointsData: JSON.parse(document.getElementById('points-data').textContent),
            weekdayConfig: weekdayConfig
        };
    }

    /**
     * Initialize charts
     */
    initCharts() {
        this.charts = new ProgressCharts();
    }

    /**
     * Initialize Bootstrap tooltips
     */
    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.progressPage = new ProgressPage();
}); 