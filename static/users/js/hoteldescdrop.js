document.addEventListener('DOMContentLoaded', function () {
    // Counts and dropdown logic
    const counts = {
        adults: 2,
        children: 0,
        rooms: 1,
    };

    const MAX_ADULTS = 30;
    const MAX_CHILDREN = 10;
    const MAX_ROOMS = 30;

    const updateDropdownText = () => {
        document.querySelector('.dropdown-toggler').textContent =
            `${counts.adults} adults · ${counts.children} children · ${counts.rooms} room${counts.rooms > 1 ? 's' : ''}`;
    };

    // Prevent dropdown from closing when interacting with the menu
    const dropdownMenu = document.querySelector('.dropdown-menu');
    dropdownMenu.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent click propagation to the dropdown toggle
    });

    // Event listeners for + and - buttons (adults, children, rooms)
    document.querySelectorAll('.plus-btn, .minus-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default action
            event.stopPropagation(); // Stop propagation to prevent closing the dropdown

            const type = button.dataset.type;

            if (button.classList.contains('plus-btn')) {
                if (type === 'adults' && counts.adults < MAX_ADULTS) {
                    counts[type]++;
                } else if (type === 'children' && counts.children < MAX_CHILDREN) {
                    counts[type]++;
                } else if (type === 'rooms' && counts.rooms < MAX_ROOMS) {
                    counts[type]++;
                }
            } else if (button.classList.contains('minus-btn') && counts[type] > 0) {
                counts[type]--;
            }

            // Update the count display
            document.getElementById(`${type}-count`).textContent = counts[type];

            // Show/hide children's ages section
            if (type === 'children') {
                const childrenAges = document.getElementById('children-ages');
                if (counts.children > 0) {
                    childrenAges.style.display = 'block';
                    // Add age inputs dynamically
                    childrenAges.innerHTML = '';
                    for (let i = 0; i < counts.children; i++) {
                        const input = document.createElement('input');
                        input.type = 'number';
                        input.min = '1';
                        input.max = '17';
                        input.placeholder = 'Age';
                        input.style.margin = '5px';
                        input.style.width = '50px';
                        childrenAges.appendChild(input);
                    }
                } else {
                    childrenAges.style.display = 'none';
                }
            }
        });
    });

    // Event listener for the "Done" button
    document.querySelector('.btn-done').addEventListener('click', (event) => {
        event.preventDefault(); // Prevent form submission or default button behavior
        updateDropdownText(); // Update the dropdown text with the new counts
        document.getElementById('dropdown-toggle').checked = false; // Close the dropdown
    });

    // Initial update of dropdown text
    updateDropdownText();

    // Get the date inputs
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');

    // Set the minimum date to today for the start and end date
    const today = new Date();
    const todayString = today.toISOString().split("T")[0]; // Format to YYYY-MM-DD
    startDateInput.setAttribute("min", todayString); // Ensure start date can't be in the past
    endDateInput.setAttribute("min", todayString); // Ensure end date can't be in the past

    // Function to update the minimum end date based on start date
    function updateEndDateMin() {
        const selectedStartDate = startDateInput.value;

        if (selectedStartDate) {
            const startDate = new Date(selectedStartDate);
            const minEndDate = startDate.toISOString().split("T")[0]; // Set min end date to start date

            endDateInput.setAttribute("min", minEndDate);

            // If the selected end date is before the start date, reset it
            if (new Date(endDateInput.value) < startDate) {
                endDateInput.value = ""; // Clear the end date if invalid
            }
        }
    }

    // Add an event listener for changes on the start date
    startDateInput.addEventListener("change", updateEndDateMin);

    // Optional: Prevent form submission if invalid date is selected
    const form = document.querySelector(".search-form");
    form.addEventListener("submit", (e) => {
        let isValid = true;

        // Ensure the start date is today or later
        if (new Date(startDateInput.value) < today) {
            isValid = false;
            alert("Start date cannot be in the past.");
        }

        // Ensure the end date is not before the start date
        if (new Date(endDateInput.value) < new Date(startDateInput.value)) {
            isValid = false;
            alert("End date must be on or after the start date.");
        }

        if (!isValid) {
            e.preventDefault(); // Prevent form submission
            alert("Please select valid dates.");
        }
    });
});
