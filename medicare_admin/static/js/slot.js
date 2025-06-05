document.addEventListener('DOMContentLoaded', function() {
    const repeatSelect = document.getElementById('repeat');
    const repeatDaysContainer = document.getElementById('repeat-days-container');
    
    // Show/hide repeat days based on selection
    repeatSelect.addEventListener('change', function() {
        if (this.value === 'weekly') {
            repeatDaysContainer.classList.remove('hidden');
        } else {
            repeatDaysContainer.classList.add('hidden');
        }
    });
    
    // Form submission
    document.getElementById('availabilityForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;
        const repeat = document.getElementById('repeat').value;
        
        // Get selected days
        const selectedDays = [];
        document.querySelectorAll('.day-checkbox:checked').forEach(checkbox => {
            selectedDays.push(checkbox.value);
        });
        
        // Validate inputs
        if (!startDate || !endDate || !startTime || !endTime || !repeat) {
            alert('Please fill in all required fields');
            return;
        }
        
        // Time validation
        if (startTime >= endTime) {
            alert('End time must be after start time');
            return;
        }
        
        // Date validation
        if (new Date(startDate) > new Date(endDate)) {
            alert('End date cannot be before start date');
            return;
        }
        
        // Weekly repeat validation
        if (repeat === 'weekly' && selectedDays.length === 0) {
            alert('Please select at least one weekday for weekly repeat');
            return;
        }
        
        // Format dates for display
        const startDateObj = new Date(startDate);
        const endDateObj = new Date(endDate);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        const formattedStartDate = startDateObj.toLocaleDateString('en-US', options);
        const formattedEndDate = endDateObj.toLocaleDateString('en-US', options);
        
        // Format time for display
        const formatTime = (timeString) => {
            const [hours, minutes] = timeString.split(':');
            const period = hours >= 12 ? 'PM' : 'AM';
            const displayHours = hours % 12 || 12;
            return `${displayHours}:${minutes} ${period}`;
        };
        
        const formattedStartTime = formatTime(startTime);
        const formattedEndTime = formatTime(endTime);
        
        // Create display text based on repeat options
        let displayText = `${formattedStartDate} - ${formattedEndDate} | ${formattedStartTime} - ${formattedEndTime}`;
        
        if (repeat === 'daily') {
            displayText += ' (Daily)';
        } else if (repeat === 'weekly') {
            displayText += ` (Weekly on ${selectedDays.join(', ')})`;
        }
        
        // Create new availability item
        const itemId = Date.now();
        const availabilityItem = document.createElement('div');
        availabilityItem.className = 'availability-item';
        availabilityItem.dataset.id = itemId;
        availabilityItem.innerHTML = `
            <span>${displayText}</span>
            <button class="remove-btn" onclick="removeAvailability('${itemId}')">Remove</button>
        `;
        
        // Add to the list
        document.getElementById('availabilityItems').appendChild(availabilityItem);
        
        // Reset form
        this.reset();
        repeatDaysContainer.classList.add('hidden');
    });
});
        
        function removeAvailability(id) {
            const item = document.querySelector(`.availability-item[data-id="${id}"]`);
            if (item) {
                item.remove();
            }
        }



