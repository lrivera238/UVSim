function fetchAccumulator() {
    fetch('/api/get_accumulator')
    .then(response => response.json())
    .then(data => {
        document.getElementById('accumulator').innerText = data.accumulator;
    })
    .catch(error => console.error('Error fetching accumulator:', error));
}

// Auto-update every 3 seconds
setInterval(fetchAccumulator, 3000);

// Fetch accumulator when the page loads
window.onload = fetchAccumulator;
