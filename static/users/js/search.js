document.addEventListener("DOMContentLoaded", () => {
  /*** ONE-WAY / RETURN FLIGHT TOGGLING ***/
  const returnDateInput = document.querySelector('input[name="end_date"]');
  const flightTypeRadios = document.querySelectorAll(
    'input[name="flight_type"]'
  );

  // Function to toggle return date visibility
  const toggleReturnDate = () => {
    const selectedType = document.querySelector(
      'input[name="flight_type"]:checked'
    ).value;
    if (selectedType === "return") {
      returnDateInput.style.display = "block";
    } else {
      returnDateInput.style.display = "none";
      returnDateInput.value = ""; // Clear the return date
    }
  };

  // Attach event listeners to flight type radios
  flightTypeRadios.forEach((radio) => {
    radio.addEventListener("change", toggleReturnDate);
  });

  // Initialize on page load
  toggleReturnDate();

  /*** AUTOCOMPLETE FUNCTIONALITY ***/
  const destinationInput = document.querySelector('input[name="destination"]');
  const autocompleteResults = document.createElement("div");
  autocompleteResults.classList.add("autocomplete-results");
  destinationInput.parentNode.appendChild(autocompleteResults);

  let debounceTimer;

  destinationInput.addEventListener("input", () => {
    const query = destinationInput.value.trim();

    // Clear previous results
    autocompleteResults.innerHTML = "";

    if (query.length > 1) {
      // Debounce to avoid rapid requests
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        fetch(`/users/autocomplete/?q=${query}`)
          .then((response) => response.json())
          .then((data) => {
            if (data.length > 0) {
              data.forEach((item) => {
                const resultItem = document.createElement("div");
                resultItem.textContent = item;
                resultItem.classList.add("autocomplete-item");
                resultItem.addEventListener("click", () => {
                  destinationInput.value = item;
                  autocompleteResults.innerHTML = "";
                });
                autocompleteResults.appendChild(resultItem);
              });
            } else {
              const noResult = document.createElement("div");
              noResult.textContent = "No results found";
              noResult.classList.add("autocomplete-no-results");
              autocompleteResults.appendChild(noResult);
            }
          });
      }, 300); // 300ms debounce delay
    }
  });

  // Close autocomplete dropdown when clicking outside
  document.addEventListener("click", (event) => {
    if (!destinationInput.contains(event.target)) {
      autocompleteResults.innerHTML = "";
    }
  });
});
