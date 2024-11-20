document.addEventListener('DOMContentLoaded', () => {
    const voiceSearchBtn = document.getElementById('voiceSearchBtn');
    const searchForm = document.querySelector('form');
    const transcription = document.getElementById('transcription');
    const searchInput = document.getElementById('searchInput');

    // Initialize Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.continuous = false; // Stop automatically after one command
    recognition.interimResults = false; // Only process final results
    recognition.lang = 'en-US'; // Set language to English

    // Start voice recognition on button click
    voiceSearchBtn.addEventListener('click', () => {
        transcription.textContent = "Listening...";
        recognition.start();
    });

    // Process recognition result
    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        transcription.textContent = `You said: "${speechResult}"`;
        searchInput.value = speechResult; // Populate the search input with the recognized text
    };

    recognition.onerror = (event) => {
        transcription.textContent = `Error: ${event.error}`;
    };

    // Perform a search using the recognized text
    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        transcription.textContent = `You said: "${speechResult}"`;
        searchInput.value = speechResult; // Populate the search input with the recognized text
        searchForm.submit(); // Submit the form automatically after voice input
    };
});
