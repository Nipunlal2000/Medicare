document.getElementById('image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');
    const fileName = document.getElementById('file-name');

    // Show selected file name
    fileName.textContent = file ? file.name : "No file chosen";

    // Show preview if image selected
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }

        reader.readAsDataURL(file);
    } else {
        // Revert to original or hide
        const originalImageUrl = "{{ doctor.image.url|default:'' }}";
        if (originalImageUrl) {
            preview.src = originalImageUrl;
            preview.style.display = 'block';
        } else {
            preview.style.display = 'none';
        }
    }
});
