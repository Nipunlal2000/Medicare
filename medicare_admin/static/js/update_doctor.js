document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('doctorForm');
    const imageUpload = document.getElementById('image');
    const imagePreview = document.getElementById('image-preview');
    const fileName = document.getElementById('file-name');
    const existingImage = '{{ doctor.image.url }}' || false;
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

    // Image preview functionality
    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        const errorElement = document.getElementById('image-error');
        
        // Reset previous errors
        errorElement.textContent = '';
        document.getElementById('file-wrapper').classList.remove('error');
        
        if (file) {
            // Validate file type
            if (!allowedTypes.includes(file.type)) {
                errorElement.textContent = 'Only image files are allowed (JPEG, PNG, GIF, WEBP)';
                document.getElementById('file-wrapper').classList.add('error');
                imageUpload.value = ''; // Clear the invalid file
                fileName.textContent = 'No file chosen';
                if (!existingImage) {
                    imagePreview.style.display = 'none';
                }
                return;
            }

            // Validate file size (optional - example for 5MB limit)
            if (file.size > 5 * 1024 * 1024) {
                errorElement.textContent = 'Image size must be less than 5MB';
                document.getElementById('file-wrapper').classList.add('error');
                imageUpload.value = ''; // Clear the invalid file
                fileName.textContent = 'No file chosen';
                if (!existingImage) {
                    imagePreview.style.display = 'none';
                }
                return;
            }

            // If valid, proceed with preview
            const reader = new FileReader();
            reader.onload = function(event) {
                imagePreview.src = event.target.result;
                imagePreview.style.display = 'block';
            }
            reader.readAsDataURL(file);
            fileName.textContent = file.name;
        } else {
            if (!existingImage) {
                imagePreview.style.display = 'none';
            }
            fileName.textContent = 'No file chosen';
        }
    });

    // Form validation
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        let isValid = true;

        // Reset error messages
        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.previousElementSibling?.classList?.remove('error');
        });

        // Name validation
        const name = document.getElementById('name');
        if (!name.value.trim()) {
            document.getElementById('name-error').textContent = 'Full name is required';
            name.classList.add('error');
            isValid = false;
        }

        // Specialization validation
        const specialization = document.getElementById('specialization');
        if (!specialization.value.trim()) {
            document.getElementById('specialization-error').textContent = 'Specialization is required';
            specialization.classList.add('error');
            isValid = false;
        }

        // Image validation (only required if not editing or no existing image)
        const image = document.getElementById('image');
        if (!existingImage) {
            if (!image.files || image.files.length === 0) {
                document.getElementById('image-error').textContent = 'Image is required';
                document.getElementById('file-wrapper').classList.add('error');
                isValid = false;
            } else if (!allowedTypes.includes(image.files[0].type)) {
                document.getElementById('image-error').textContent = 'Only image files are allowed (JPEG, PNG, GIF, WEBP)';
                document.getElementById('file-wrapper').classList.add('error');
                isValid = false;
            }
        }

        // Hospital validation
        const hospital = document.getElementById('hospital');
        if (!hospital.value.trim()) {
            document.getElementById('hospital-error').textContent = 'Hospital is required';
            hospital.classList.add('error');
            isValid = false;
        }

        // Address validation
        const address = document.getElementById('address');
        if (!address.value.trim()) {
            document.getElementById('address-error').textContent = 'Address is required';
            address.classList.add('error');
            isValid = false;
        }

        if (isValid) {
            form.submit();
        }
    });

    // Real-time validation
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', function() {
            const errorElement = document.getElementById(`${this.id}-error`);
            if (errorElement) {
                errorElement.textContent = '';
                this.classList.remove('error');
                if (this.id === 'image') {
                    document.getElementById('file-wrapper').classList.remove('error');
                }
            }
        });
    });
});