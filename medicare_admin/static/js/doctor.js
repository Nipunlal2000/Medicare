document.addEventListener('DOMContentLoaded', function() {
            // Add interactivity to option cards
            const optionCards = document.querySelectorAll('.option-card');
            
            optionCards.forEach(card => {
                const checkbox = card.querySelector('input[type="checkbox"]');
                
                // Toggle selected class when card is clicked
                card.addEventListener('click', function(e) {
                    if (e.target !== checkbox) {
                        checkbox.checked = !checkbox.checked;
                    }
                    
                    card.classList.toggle('selected', checkbox.checked);
                    updateSummary();
                });
                
                // Initialize selected state
                card.classList.toggle('selected', checkbox.checked);
            });
            
            // Update the availability summary
            function updateSummary() {
                // In a real implementation, this would collect the actual selected days and times
                // For this demo, we'll just simulate an update
                console.log("Availability updated");
            }
        });


document.getElementById('image-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        reader.readAsDataURL(file);
    } else {
        // If user cancels selection, revert to original image or hide
        var originalImageUrl = "{{ doctor.image.url|default:'' }}";
        if (originalImageUrl) {
            preview.src = originalImageUrl;
            preview.style.display = 'block';
        } else {
            preview.style.display = 'none';
        }
    }
});