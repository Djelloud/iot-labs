const BACKEND_URL = 'http://localhost:8080'; // Backend API URL for local testing

let tempGraph, humGraph;

// Initialize charts
function initCharts() {
    // Temperature chart
    const tempCtx = document.getElementById('tempGraph').getContext('2d');
    tempGraph = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Humidity chart
    const humCtx = document.getElementById('humGraph').getContext('2d');
    humGraph = new Chart(humCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity (%)',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Error handling
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Fetch temperature data
async function fetchTemperatureData() {
    try {
        // Current value
        const currentResponse = await fetch(`${BACKEND_URL}/capteurs/temp`);
        if (currentResponse.ok) {
            const currentTemp = await currentResponse.text();
            document.getElementById('currentTemp').textContent = currentTemp + '°C';
        }

        // Average of 30 values
        const avgResponse = await fetch(`${BACKEND_URL}/capteurs/temp/30/moy`);
        if (avgResponse.ok) {
            const avgTemp = await avgResponse.text();
            document.getElementById('avgTemp').textContent = avgTemp + '°C';
        }

        // History of 30 values
        const historyResponse = await fetch(`${BACKEND_URL}/capteurs/temp/30`);
        if (historyResponse.ok) {
            const history = await historyResponse.json();
            updateTemperatureTable(history);
            updateTemperatureChart(history);
        }

    } catch (error) {
        showError('Error fetching temperature data: ' + error.message);
    }
}

// Fetch humidity data
async function fetchHumidityData() {
    try {
        // Current value
        const currentResponse = await fetch(`${BACKEND_URL}/capteurs/hum`);
        if (currentResponse.ok) {
            const currentHum = await currentResponse.text();
            document.getElementById('currentHum').textContent = currentHum;
        }

        // Average of 30 values
        const avgResponse = await fetch(`${BACKEND_URL}/capteurs/hum/30/moy`);
        if (avgResponse.ok) {
            const avgHum = await avgResponse.text();
            document.getElementById('avgHum').textContent = avgHum;
        }

        // History of 30 values
        const historyResponse = await fetch(`${BACKEND_URL}/capteurs/hum/30`);
        if (historyResponse.ok) {
            const history = await historyResponse.json();
            updateHumidityTable(history);
            updateHumidityChart(history);
        }

    } catch (error) {
        showError('Error fetching humidity data: ' + error.message);
    }
}

// Update temperature table
function updateTemperatureTable(history) {
    const tbody = document.querySelector('#tempTable tbody');
    tbody.innerHTML = '';
    
    history.forEach(([timestamp, value]) => {
        const row = tbody.insertRow();
        row.insertCell(0).textContent = timestamp;
        row.insertCell(1).textContent = value.toFixed(1);
    });
}

// Update humidity table
function updateHumidityTable(history) {
    const tbody = document.querySelector('#humTable tbody');
    tbody.innerHTML = '';
    
    history.forEach(([timestamp, value]) => {
        const row = tbody.insertRow();
        row.insertCell(0).textContent = timestamp;
        row.insertCell(1).textContent = value.toFixed(1);
    });
}

// Update temperature chart
function updateTemperatureChart(history) {
    const labels = history.map(([timestamp]) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
    });
    const data = history.map(([, value]) => value);
    
    tempGraph.data.labels = labels;
    tempGraph.data.datasets[0].data = data;
    tempGraph.update();
}

// Update humidity chart
function updateHumidityChart(history) {
    const labels = history.map(([timestamp]) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
    });
    const data = history.map(([, value]) => value);
    
    humGraph.data.labels = labels;
    humGraph.data.datasets[0].data = data;
    humGraph.update();
}

// Refresh all data
function refreshData() {
    fetchTemperatureData();
    fetchHumidityData();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    refreshData();
    
    // Auto-refresh every 3 seconds
    setInterval(refreshData, 3000);
});