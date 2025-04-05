/**
 * Charts for visualizing evaluation results
 * Uses Chart.js to create bar and radar charts
 */
document.addEventListener('DOMContentLoaded', function() {
    // Bar chart for average scores by criterion
    const avgScoresCtx = document.getElementById('avgScoresChart');
    if (avgScoresCtx) {
        const labels = JSON.parse(avgScoresCtx.getAttribute('data-labels'));
        const values = JSON.parse(avgScoresCtx.getAttribute('data-values'));
        
        new Chart(avgScoresCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Average Score',
                    data: values,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 206, 86, 0.6)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Average Scores by Evaluation Criteria'
                    }
                }
            }
        });
    }
    
    // Radar chart for individual student evaluation
    const studentRadarCtx = document.getElementById('studentRadarChart');
    if (studentRadarCtx) {
        const scores = JSON.parse(studentRadarCtx.getAttribute('data-scores'));
        
        new Chart(studentRadarCtx, {
            type: 'radar',
            data: {
                labels: ['Relevance', 'Coverage', 'Structure'],
                datasets: [{
                    label: 'Your Scores',
                    data: [scores.relevance, scores.coverage, scores.structure],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    }
    
    // Distribution chart for scores
    const scoreDistributionCtx = document.getElementById('scoreDistributionChart');
    if (scoreDistributionCtx) {
        const scores = JSON.parse(scoreDistributionCtx.getAttribute('data-scores'));
        
        // Group scores into ranges
        const ranges = {
            '0-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0,
            '81-100': 0
        };
        
        scores.forEach(score => {
            if (score <= 20) ranges['0-20']++;
            else if (score <= 40) ranges['21-40']++;
            else if (score <= 60) ranges['41-60']++;
            else if (score <= 80) ranges['61-80']++;
            else ranges['81-100']++;
        });
        
        new Chart(scoreDistributionCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(ranges),
                datasets: [{
                    data: Object.values(ranges),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(54, 162, 235, 0.6)'
                    ],
                    borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Score Distribution'
                    }
                }
            }
        });
    }
});
