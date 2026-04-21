// API Base URL
const API_URL = window.location.origin;

// Message Helper
function showMessage(message, type = 'info') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message show ${type}`;
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 5000);
}

// Fetch Weather for a City
async function fetchWeather() {
    const city = document.getElementById('cityInput').value.trim();
    
    if (!city) {
        showMessage('Please enter a city name', 'error');
        return;
    }
    
    showMessage('Fetching weather...', 'info');
    
    try {
        const response = await fetch(
            `${API_URL}/fetch-weather?city=${encodeURIComponent(city)}`
        );
        
        const data = await response.json();
        
        if (response.ok) {
            displayCurrentWeather(data.data);
            showMessage(`✅ Weather for ${city} fetched successfully!`, 'success');
            updateStats();
        } else {
            showMessage(`❌ Error: ${data.detail}`, 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Display Current Weather
function displayCurrentWeather(data) {
    const weatherEl = document.getElementById('currentWeather');
    
    weatherEl.innerHTML = `
        <h2>🌍 ${data.city.toUpperCase()}</h2>
        <div class="weather-item">
            <strong>Temperature</strong>
            <span>${data.temperature}°C</span>
        </div>
        <div class="weather-item">
            <strong>Feels Like</strong>
            <span>${data.feels_like}°C</span>
        </div>
        <div class="weather-item">
            <strong>Humidity</strong>
            <span>${data.humidity}%</span>
        </div>
        <div class="weather-item">
            <strong>Condition</strong>
            <span style="text-transform: capitalize;">${data.description}</span>
        </div>
    `;
}

// Get All Unique Weather (Latest per city)
async function getUniqueWeather() {
    showMessage('Loading weather data...', 'info');
    
    try {
        const response = await fetch(`${API_URL}/weather/unique`);
        const data = await response.json();
        
        if (response.ok) {
            displayWeatherGrid(data.data);
            showMessage(`✅ Loaded ${data.count} unique weather records!`, 'success');
            updateStats();
        } else {
            showMessage('❌ Error loading data', 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Display Weather Grid
function displayWeatherGrid(weatherList) {
    const gridEl = document.getElementById('weatherData');
    
    if (!weatherList || weatherList.length === 0) {
        gridEl.innerHTML = '<p class="loading">No weather data available</p>';
        return;
    }
    
    gridEl.innerHTML = weatherList.map(weather => `
        <div class="weather-item-card">
            <h3>${weather.city}</h3>
            <p class="temp">${weather.temperature}°C</p>
            <p><strong>Feels:</strong> ${weather.feels_like}°C</p>
            <p><strong>Humidity:</strong> ${weather.humidity}%</p>
            <p class="description">${weather.description}</p>
            <p style="font-size: 0.8em; margin-top: 10px;">
                📅 ${new Date(weather.timestamp).toLocaleString()}
            </p>
        </div>
    `).join('');
}

// Count Duplicates
async function countDuplicates() {
    try {
        const response = await fetch(`${API_URL}/weather/duplicates/count`);
        const data = await response.json();
        
        if (response.ok) {
            const message = `
📊 Statistics:
- Total Records: ${data.total_records}
- Unique Cities: ${data.unique_cities}
- Duplicate Records: ${data.total_duplicate_records}
- Cities with Duplicates: ${data.cities_with_duplicates}
            `;
            showMessage(message, 'info');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Cleanup Duplicates
async function cleanupDuplicates() {
    if (!confirm('Are you sure you want to delete duplicate records? This action cannot be undone.')) {
        return;
    }
    
    showMessage('Cleaning up duplicates...', 'info');
    
    try {
        const response = await fetch(`${API_URL}/cleanup-duplicates`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(
                `✅ Cleanup complete!\n🗑️ Deleted: ${data.deleted_records} records\n✨ Kept: ${data.kept_records} records`,
                'success'
            );
            getUniqueWeather();
            updateStats();
        } else {
            showMessage('❌ Error during cleanup', 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Update Statistics
async function updateStats() {
    try {
        const allResponse = await fetch(`${API_URL}/weather`);
        const allData = await allResponse.json();
        
        const duplicateResponse = await fetch(`${API_URL}/weather/duplicates/count`);
        const duplicateData = await duplicateResponse.json();
        
        document.getElementById('totalRecords').textContent = allData.count;
        document.getElementById('uniqueCities').textContent = duplicateData.unique_cities;
        document.getElementById('duplicateRecords').textContent = duplicateData.total_duplicate_records;
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Go to API Docs
function goToDocs() {
    window.open(`${API_URL}/docs`, '_blank');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
});

// Allow Enter key to search
document.getElementById('cityInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchWeather();
    }
});