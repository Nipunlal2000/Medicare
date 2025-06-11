const fileInput = document.getElementById("image");
    const fileName = document.getElementById("file-name");

    fileInput.addEventListener("change", function () {
        fileName.textContent = this.files[0]?.name || "No file chosen";
    });


    document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('doctorForm');
    
    // Add asterisk to required fields
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        const label = field.closest('.input-field').querySelector('label');
        if (label && !label.innerHTML.includes('<span class="required">*</span>')) {
            label.innerHTML += ' <span class="required">*</span>';
        }
    });

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

        // Email validation
        const email = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value.trim()) {
            document.getElementById('email-error').textContent = 'Email is required';
            email.classList.add('error');
            isValid = false;
        } else if (!emailRegex.test(email.value)) {
            document.getElementById('email-error').textContent = 'Please enter a valid email';
            email.classList.add('error');
            isValid = false;
        }

        // Password validation
        const password = document.getElementById('password');
        if (!password.value.trim()) {
            document.getElementById('password-error').textContent = 'Password is required';
            password.classList.add('error');
            isValid = false;
        } else if (password.value.length < 8) {
            document.getElementById('password-error').textContent = 'Password must be at least 8 characters';
            password.classList.add('error');
            isValid = false;
        }

        // Specialization validation
        const specialization = document.getElementById('specialization');
        if (!specialization.value.trim()) {
            document.getElementById('specialization-error').textContent = 'Specialization is required';
            specialization.classList.add('error');
            isValid = false;
        }

        // Image validation
        const image = document.getElementById('image');
        if (!image.files || image.files.length === 0) {
            document.getElementById('image-error').textContent = 'Image is required';
            image.classList.add('error');
            isValid = false;
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
            }
        });
    });
});