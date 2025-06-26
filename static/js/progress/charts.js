/**
 * Charts functionality for the progress page
 * Handles points over time chart and weekday performance chart
 */

class ProgressCharts {
    constructor() {
        this.pointsChart = null;
        this.weekdayChart = null;
        this.init();
    }

    init() {
        this.initPointsChart();
        this.initWeekdayChart();
    }

    initPointsChart() {
        const pointsData = window.progressData.pointsData;
        const dataPoints = pointsData.map(item => ({
            x: item[0],  // "YYYY-MM-DD"
            y: item[1]
        }));

        const ctx = document.getElementById('pointsChart').getContext('2d');
        Chart.register(ChartZoom);

        this.pointsChart = new Chart(ctx, {
            type: 'line',
            data: { 
                datasets: [{ 
                    label: 'Points Earned', 
                    data: dataPoints, 
                    borderColor: 'teal', 
                    tension: 0.1 
                }] 
            },
            options: {
                scales: {
                    x: { 
                        type: 'time', 
                        time: { 
                            parser: 'yyyy-MM-dd', 
                            unit: 'day' 
                        } 
                    },
                    y: { 
                        beginAtZero: true 
                    }
                },
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true,
                                modifierKey: "ctrl"
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x'
                        },
                        pan: {
                            enabled: true,
                            mode: 'x',
                            modifierKey: null 
                        },
                    }   
                }
            }
        });
    }

    initWeekdayChart() {
        const weekdayConfig = window.progressData.weekdayConfig;
        const weekdayData = weekdayConfig.weekdayData;
        const hasSufficientWeekdayData = weekdayConfig.hasSufficientWeekdayData;
        const sampleWeekdayData = weekdayConfig.sampleWeekdayData;

        // Always show sample data in background, real data if available
        const displayData = hasSufficientWeekdayData ? weekdayData : sampleWeekdayData;

        const weekdayLabels = displayData.map(item => item.name);
        const weekdayPoints = displayData.map(item => item.avg_points);

        // Create the weekday bar chart
        const weekdayCtx = document.getElementById('weekdayChart').getContext('2d');
        this.weekdayChart = new Chart(weekdayCtx, {
            type: 'bar',
            data: {
                labels: weekdayLabels,
                datasets: [{
                    label: 'Average Points',
                    data: weekdayPoints,
                    backgroundColor: hasSufficientWeekdayData ? 'rgba(0, 212, 255, 0.6)' : 'rgba(0, 212, 255, 0.2)',
                    borderColor: hasSufficientWeekdayData ? '#00d4ff' : 'rgba(0, 212, 255, 0.3)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Average Points',
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Day of Week',
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        // Apply visual effects for insufficient data
        if (!hasSufficientWeekdayData) {
            // The overlay will handle the visual blocking, chart stays visible but dimmed
            this.weekdayChart.canvas.style.opacity = '0.3';
            this.weekdayChart.canvas.style.pointerEvents = 'none';
        }
    }
}

// Export for use in other modules
window.ProgressCharts = ProgressCharts; 