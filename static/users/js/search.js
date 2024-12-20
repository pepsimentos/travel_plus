// Fetch the city data from the external JSON file
fetch('/static/users/json/cities.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to load city data');
    }
    return response.json();
  })
  .then(cities => {
    // Get the <datalist> element
    const datalist = document.getElementById('cities');

    // Populate the <datalist> with <option> elements
    cities.forEach(city => {
      const option = document.createElement('option');
      option.value = city;
      datalist.appendChild(option);
    });
  })
  .catch(error => {
    console.error('Error loading city data:', error);
  });

// Toggle visibility of end_date when the checkbox is checked/unchecked
document.getElementById('one_way_checkbox').addEventListener('change', function () {
  const endDateInput = document.getElementById('end_date');
  endDateInput.style.display = this.checked ? 'none' : 'block';
});