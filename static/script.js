
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('comic-form');
    const generateBtn = document.getElementById('generate-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const comicStrip = document.getElementById('comic-strip');
    const addPanelBtn = document.getElementById('add-panel-btn');
    const removePanelBtn = document.getElementById('remove-panel-btn');
    const panelsContainer = document.getElementById('panels-container');

    addPanelBtn.addEventListener('click', () => {
        const panelCount = panelsContainer.getElementsByTagName('textarea').length;
        const newPanel = document.createElement('textarea');
        newPanel.name = 'panels';
        newPanel.placeholder = `Panel ${panelCount + 1}:`;
        panelsContainer.appendChild(newPanel);
    });

    removePanelBtn.addEventListener('click', () => {
        const textareas = panelsContainer.getElementsByTagName('textarea');
        if (textareas.length > 1) {
            panelsContainer.removeChild(textareas[textareas.length - 1]);
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Show loading indicator and disable button
        loadingIndicator.style.display = 'block';
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        comicStrip.innerHTML = ''; // Clear previous results

        // Get data from the form
        const character = document.getElementById('character').value;
        const style = document.getElementById('style').value;
        const panelTextareas = document.getElementsByName('panels');
        const panels = Array.from(panelTextareas).map(ta => ta.value).filter(Boolean); // Filter out empty strings

        try {
            // Send data to the backend
            const response = await fetch('/generate-comic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ character, style, panels }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();

            // Display the generated images
            if (result.images && result.images.length > 0) {
                result.images.forEach(imageUrl => {
                    const imgElement = document.createElement('img');
                    imgElement.src = imageUrl;
                    imgElement.alt = "Generated comic panel";
                    comicStrip.appendChild(imgElement);
                });
            } else {
                comicStrip.innerHTML = '<p>Could not generate images. Please check the console for errors.</p>';
            }

        } catch (error) {
            console.error("Error generating comic:", error);
            comicStrip.innerHTML = `<p>An error occurred. See the browser console for details.</p>`;
        } finally {
            // Hide loading indicator and re-enable button
            loadingIndicator.style.display = 'none';
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Comic';
        }
    });
});
