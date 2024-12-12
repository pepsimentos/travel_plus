document.addEventListener('DOMContentLoaded', () => {
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

    // Event listeners for + and - buttons
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
});
