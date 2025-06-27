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

// Word Cloud rendering
// Requires wordcloud2.js to be loaded on the page
if (window.wordcloudData && document.getElementById('wordcloud')) {
    // Dynamically load wordcloud2.js if not already loaded
    function loadWordCloudScript(callback) {
        if (window.WordCloud) {
            callback();
            return;
        }
        var script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js';
        script.onload = callback;
        document.head.appendChild(script);
    }

    loadWordCloudScript(function() {
        var words = window.wordcloudData.map(function(item) {
            return [item[0], item[1]];
        });
        var wordcloudElem = document.getElementById('wordcloud');
        WordCloud(wordcloudElem, {
            list: words,
            gridSize: 12,
            weightFactor: function (size) {
                return 18 + size * 5;
            },
            fontFamily: 'Orbitron, Arial, sans-serif',
            color: function() {
                // Sci-fi gradient colors
                var colors = ['#00d4ff', '#ff00ff', '#4fd1c7', '#fff', '#00ffb3', '#ff6ec7'];
                return colors[Math.floor(Math.random() * colors.length)];
            },
            backgroundColor: 'rgba(26, 26, 46, 1)',
            rotateRatio: 0.2,
            rotationSteps: 2,
            minSize: 14,
            click: function(item) {
                var word = item[0];
                window.location.href = '/read-diary?search=' + encodeURIComponent(word);
            },
            drawOutOfBound: false,
            shuffle: true,
            hover: window.innerWidth > 600
        });
        // Set pointer cursor on hover
        var canvas = wordcloudElem.querySelector('canvas');
        if (canvas) {
            canvas.style.cursor = 'pointer';
        }
    });
} 