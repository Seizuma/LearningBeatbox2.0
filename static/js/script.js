document.getElementById('start-btn').addEventListener('click', function () {
    fetch('/start', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === "started") {
                document.getElementById('start-btn').disabled = true;
                document.getElementById('stop-btn').disabled = false;
                document.getElementById('analyze-btn').disabled = true;
                document.getElementById('results').innerHTML = '';
            }
        });
});

document.getElementById('stop-btn').addEventListener('click', function () {
    fetch('/stop', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === "stopped") {
                document.getElementById('start-btn').disabled = false;
                document.getElementById('stop-btn').disabled = true;
                document.getElementById('analyze-btn').disabled = false;
            }
        });
});

document.getElementById('analyze-btn').addEventListener('click', function () {
    fetch('/analyze')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('results').innerHTML = `<p>${data.error}</p>`;
            } else {
                let resultsHTML = `<p>Overall Accuracy: ${data.overall_accuracy.toFixed(2)}%</p>`;
                resultsHTML += '<table><tr><th>Sound</th><th>Count</th><th>Avg Intensity</th><th>Avg Frequency</th><th>Avg Power</th></tr>';
                data.stats.forEach(stat => {
                    resultsHTML += `<tr><td>${stat.winner}</td><td>${stat.count}</td><td>${stat.avg_intensity.toFixed(2)}</td><td>${stat.avg_frequency.toFixed(2)}</td><td>${stat.avg_power.toFixed(2)}</td></tr>`;
                });
                resultsHTML += '</table>';
                document.getElementById('results').innerHTML = resultsHTML;
            }
        });
});
