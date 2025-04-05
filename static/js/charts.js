/**
 * Charts for visualizing evaluation results
 * Uses Chart.js to create bar and radar charts
 */

document.addEventListener('DOMContentLoaded', function() {
    // Bar chart for score distribution
    const scoreDistributionCtx = document.getElementById('scoreDistributionChart');
    if (scoreDistributionCtx) {
        const labels = JSON.parse(scoreDistributionCtx.dataset.labels);
        const data = JSON.parse(scoreDistributionCtx.dataset.values);
        const maxScore = parseInt(scoreDistributionCtx.dataset.maxScore);
        
        new Chart(scoreDistributionCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Score Distribution',
                    data: data,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: maxScore,
                        title: {
                            display: true,
                            text: 'Total Score'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Student Submissions'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: function(tooltipItems) {
                                return 'Submission #' + tooltipItems[0].label;
                            }
                        }
                    },
                    legend: {
                        display: false
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    // Radar chart for score dimensions
    const dimensionsChartCtx = document.getElementById('dimensionsChart');
    if (dimensionsChartCtx) {
        const labels = ['Relevance', 'Coverage', 'Structure'];
        const values = [
            parseFloat(dimensionsChartCtx.dataset.relevance),
            parseFloat(dimensionsChartCtx.dataset.coverage),
            parseFloat(dimensionsChartCtx.dataset.structure)
        ];
        
        new Chart(dimensionsChartCtx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Your Score',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 10
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw + '/10';
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    // Line chart for class average comparison
    const comparisonChartCtx = document.getElementById('comparisonChart');
    if (comparisonChartCtx) {
        const dimensions = ['Relevance', 'Coverage', 'Structure', 'Total'];
        const userScores = [
            parseFloat(comparisonChartCtx.dataset.userRelevance),
            parseFloat(comparisonChartCtx.dataset.userCoverage),
            parseFloat(comparisonChartCtx.dataset.userStructure),
            parseFloat(comparisonChartCtx.dataset.userTotal)
        ];
        const avgScores = [
            parseFloat(comparisonChartCtx.dataset.avgRelevance),
            parseFloat(comparisonChartCtx.dataset.avgCoverage),
            parseFloat(comparisonChartCtx.dataset.avgStructure),
            parseFloat(comparisonChartCtx.dataset.avgTotal)
        ];
        
        new Chart(comparisonChartCtx, {
            type: 'line',
            data: {
                labels: dimensions,
                datasets: [{
                    label: 'Your Score',
                    data: userScores,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Class Average',
                    data: avgScores,
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    tension: 0.3,
                    fill: true
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
                            text: 'Score'
                        }
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1);
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    // Add animation to charts when they scroll into view
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
        container.setAttribute('data-aos', 'fade-up');
        container.setAttribute('data-aos-duration', '1000');
    });
});
