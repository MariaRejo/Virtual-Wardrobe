// Selva's AI Wardrobe - Frontend Logic & Backend Connectivity

document.addEventListener('DOMContentLoaded', function() {
    console.log("AI Wardrobe JS Loaded Successfully!");

    // 1. Image Preview Logic
    // User image choose pannumodhu adhu epdi iruku nu preview kaata
    const fileInput = document.querySelector('input[type="file"]');
    const previewContainer = document.createElement('div');
    previewContainer.className = 'mt-3 text-center';
    
    if (fileInput) {
        fileInput.parentElement.appendChild(previewContainer);

        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <p class="text-muted">Selected Image Preview:</p>
                        <img src="${e.target.result}" class="img-thumbnail" style="max-height: 200px;">
                    `;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // 2. Dynamic Weather Selection for Recommendations
    // Backend connectivity logic to fetch recommendations based on weather
    const weatherSelect = document.getElementById('weather-filter');
    if (weatherSelect) {
        weatherSelect.addEventListener('change', function() {
            const selectedWeather = this.value;
            // Abstract-la sonna maari weather fetch panni suggest panna redirection
            window.location.href = `/recommend?weather=${selectedWeather}`;
        });
    }

    // 3. Simple Form Validation for Login/Register
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const inputs = form.querySelectorAll('input[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                event.preventDefault();
                alert("Mamey, ella field-aiyum fill pannunga!");
            }
        });
    });
});