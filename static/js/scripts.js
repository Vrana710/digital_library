function updateDateTime() {
    const now = new Date();
    const options = { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit',
      hour12: true 
    };
    document.getElementById('datetime').textContent = now.toLocaleDateString('en-US', options);
  }

  // Update date and time every second
  setInterval(updateDateTime, 1000);

  // Initial call to display date and time immediately
  updateDateTime();