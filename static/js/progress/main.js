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
    console.log('Wordcloud data available:', window.wordcloudData);
    console.log('Wordcloud element found:', document.getElementById('wordcloud'));
    
    // Dynamically load wordcloud2.js if not already loaded
    function loadWordCloudScript(callback) {
        if (window.WordCloud) {
            console.log('WordCloud library already loaded');
            callback();
            return;
        }
        console.log('Loading WordCloud library...');
        var script = document.createElement('script');
        // Try a different CDN
        script.src = 'https://unpkg.com/wordcloud@1.2.2/src/wordcloud2.min.js';
        script.onload = function() {
            console.log('WordCloud library loaded successfully');
            console.log('WordCloud function available:', typeof window.WordCloud);
            callback();
        };
        script.onerror = function() {
            console.error('Failed to load WordCloud library from unpkg, trying jsdelivr...');
            // Fallback to jsdelivr
            var fallbackScript = document.createElement('script');
            fallbackScript.src = 'https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js';
            fallbackScript.onload = function() {
                console.log('WordCloud library loaded successfully from jsdelivr');
                console.log('WordCloud function available:', typeof window.WordCloud);
                callback();
            };
            fallbackScript.onerror = function() {
                console.error('Failed to load WordCloud library from both CDNs');
            };
            document.head.appendChild(fallbackScript);
        };
        document.head.appendChild(script);
    }

    loadWordCloudScript(function() {
        console.log('Creating wordcloud with data:', window.wordcloudData);
        console.log('Raw wordcloud data type:', typeof window.wordcloudData);
        console.log('Raw wordcloud data length:', window.wordcloudData.length);
        console.log('First few raw items:', window.wordcloudData.slice(0, 3));
        
        var words = window.wordcloudData.map(function(item) {
            return [item[0], item[1]];
        });
        console.log('Processed words:', words);
        console.log('Sample word data:', words.slice(0, 3));
        console.log('Word data types:', words.slice(0, 3).map(w => [typeof w[0], typeof w[1]]));
        
        var wordcloudElem = document.getElementById('wordcloud');
        console.log('Wordcloud element:', wordcloudElem);
        
        // Render to visible div with real data
        WordCloud(wordcloudElem, {
            list: words,
            gridSize: 12,
            weightFactor: function (size) {
                // Better scaling with bounds - size comes from normalized backend data (10-100)
                const minSize = 14;
                const maxSize = 48;
                return minSize + ((size - 10) / 90) * (maxSize - minSize);
            },
            fontFamily: 'Orbitron, Arial, sans-serif',
            color: function() {
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
            hover: window.innerWidth > 600,
            shrinkToFit: true  // Added this option
        });

        // Render to hidden canvas for export with real data, matching the visible wordcloud's size
        var exportCanvas = document.getElementById('wordcloud-canvas');
        if (exportCanvas && wordcloudElem) {
            // Match the export canvas size to the visible wordcloud div
            var rect = wordcloudElem.getBoundingClientRect();
            exportCanvas.width = Math.floor(rect.width);
            exportCanvas.height = Math.floor(rect.height);

            WordCloud(exportCanvas, {
                list: words,
                gridSize: 12,
                weightFactor: function (size) {
                    // Same improved scaling for export canvas
                    const minSize = 14;
                    const maxSize = 48;
                    return minSize + ((size - 10) / 90) * (maxSize - minSize);
                },
                fontFamily: 'Orbitron, Arial, sans-serif',
                color: function() {
                    var colors = ['#00d4ff', '#ff00ff', '#4fd1c7', '#fff', '#00ffb3', '#ff6ec7'];
                    return colors[Math.floor(Math.random() * colors.length)];
                },
                backgroundColor: 'rgba(26, 26, 46, 1)',
                rotateRatio: 0.2,
                rotationSteps: 2,
                minSize: 14,
                drawOutOfBound: false,
                shuffle: true,
                shrinkToFit: true  // Added this option
            });
            console.log('Wordcloud rendered to export canvas');
        } else {
            console.error('Export canvas or wordcloud element not found!');
        }
    });
} else {
    console.log('Wordcloud conditions not met:');
    console.log('- wordcloudData available:', !!window.wordcloudData);
    console.log('- wordcloud element exists:', !!document.getElementById('wordcloud'));
    if (window.wordcloudData) {
        console.log('- wordcloudData:', window.wordcloudData);
    }
} 