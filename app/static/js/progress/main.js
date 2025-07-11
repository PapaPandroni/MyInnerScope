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
        this.setup_data();
        this.init_charts();
        this.init_tooltips();
    }

    /**
     * Setup data from the server
     */
    setup_data() {
        // Get weekday data from the JSON script tag
        const weekday_data_element = document.getElementById('weekday_data');
        const weekday_config = JSON.parse(weekday_data_element.textContent);
        
        // Setup global data object for other modules to access
        window.progress_data = {
            points_data: JSON.parse(document.getElementById('points_data').textContent),
            weekday_config: weekday_config,
            goal_stats_data: JSON.parse(document.getElementById('goal_stats_data').textContent)
        };
    }

    /**
     * Initialize charts
     */
    init_charts() {
        this.charts = new ProgressCharts();
    }

    /**
     * Initialize Bootstrap tooltips
     */
    init_tooltips() {
        const tooltip_trigger_list = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltip_trigger_list.map(function (tooltip_trigger_el) {
            return new bootstrap.Tooltip(tooltip_trigger_el);
        });
    }
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.progress_page = new ProgressPage();

    const points_today_card = document.getElementById('points_today_card');
    if (points_today_card) {
        points_today_card.addEventListener('click', function() {
            fetch('/api/points-breakdown')
                .then(response => response.json())
                .then(data => {
                    const modal_title = document.getElementById('genericModalLabel');
                    const modal_body = document.getElementById('genericModalBody');
                    
                    modal_title.textContent = "Today's Points Breakdown";
                    
                    if (data.length === 0) {
                        modal_body.innerHTML = '<p>No points earned yet today. Go complete a goal or write a diary entry!</p>';
                    } else {
                        let content = '<ul class="list-group">';
                        data.forEach(item => {
                            content += `<li class="list-group-item d-flex justify-content-between align-items-center">${item.source}<span class="badge bg-primary rounded-pill">${item.points}</span></li>`;
                        });
                        content += '</ul>';
                        modal_body.innerHTML = content;
                    }

                    const modal = new bootstrap.Modal(document.getElementById('genericModal'));
                    modal.show();
                })
                .catch(error => {
                    console.error('Error fetching points breakdown:', error);
                    const modal_body = document.getElementById('genericModalBody');
                    modal_body.innerHTML = '<p>Could not load points breakdown. Please try again later.</p>';
                    const modal = new bootstrap.Modal(document.getElementById('genericModal'));
                    modal.show();
                });
        });
    }
});

// Word Cloud rendering
// Requires wordcloud2.js to be loaded on the page
if (window.wordcloud_data && document.getElementById('wordcloud')) {
    console.log('Wordcloud data available:', window.wordcloud_data);
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
        console.log('Creating wordcloud with data:', window.wordcloud_data);
        console.log('Raw wordcloud data type:', typeof window.wordcloud_data);
        console.log('Raw wordcloud data length:', window.wordcloud_data.length);
        console.log('First few raw items:', window.wordcloud_data.slice(0, 3));
        
        var words = window.wordcloud_data.map(function(item) {
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
        var exportCanvas = document.getElementById('wordcloud_canvas');
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
    console.log('- wordcloudData available:', !!window.wordcloud_data);
    console.log('- wordcloud element exists:', !!document.getElementById('wordcloud'));
    if (window.wordcloud_data) {
        console.log('- wordcloudData:', window.wordcloud_data);
    }
} 