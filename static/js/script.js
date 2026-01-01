document.addEventListener('DOMContentLoaded', () => {
    // --- File Upload Logic ---
    const fileInput = document.getElementById('file');
    const dropZone = document.getElementById('drop-zone');
    const fileNameDisplay = document.getElementById('file-name');

    if (fileInput && dropZone) {
        // Handle drag events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('dragover');
        }

        function unhighlight(e) {
            dropZone.classList.remove('dragover');
        }

        // Handle drop
        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            updateFileName(files[0]);
        }

        // Handle normal selection
        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                updateFileName(this.files[0]);
            }
        });

        function updateFileName(file) {
            fileNameDisplay.textContent = `Selected: ${file.name}`;
            fileNameDisplay.style.opacity = '1';
        }
    }

    // --- Tab Switching & Validation Logic ---
    window.switchMode = function (mode) {
        const bulkSection = document.getElementById('bulk-section');
        const singleSection = document.getElementById('single-section');
        const modeInput = document.getElementById('mode-input');
        const fileInput = document.getElementById('file');
        const recipientEmail = document.getElementById('recipient_email');
        const tabs = document.querySelectorAll('.tab-btn');

        // Update hidden mode input
        modeInput.value = mode;

        // Toggle UI
        if (mode === 'bulk') {
            bulkSection.classList.remove('hidden');
            bulkSection.classList.add('visible');
            singleSection.classList.add('hidden');
            singleSection.classList.remove('visible');

            // Set required attributes
            if (fileInput) fileInput.required = true;
            if (recipientEmail) recipientEmail.required = false;

            // Update Tab Styles
            tabs[0].classList.add('active');
            tabs[1].classList.remove('active');
        } else {
            bulkSection.classList.add('hidden');
            bulkSection.classList.remove('visible');
            singleSection.classList.remove('hidden');
            singleSection.classList.add('visible');

            // Set required attributes
            if (fileInput) fileInput.required = false;
            if (recipientEmail) recipientEmail.required = true;

            // Update Tab Styles
            tabs[0].classList.remove('active');
            tabs[1].classList.add('active');
        }
    };

    // Initialize default state
    switchMode('bulk');
});
