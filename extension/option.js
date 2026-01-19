document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('serverUrl');
    const saveButton = document.getElementById('saveBtn');
    const statusText = document.getElementById('status');

    // 1. Fetch current runtime value profile configurations
    chrome.storage.local.get(['CLOUD_SERVER_URL'], (result) => {
        if (result.CLOUD_SERVER_URL) {
            urlInput.value = result.CLOUD_SERVER_URL;
        }
    });

    // 2. Commit configuration updates
    saveButton.addEventListener('click', () => {
        let cleanUrl = urlInput.value.trim();

        // Strip trailing slash if present
        if (cleanUrl.endsWith('/')) {
            cleanUrl = cleanUrl.slice(0, -1);
        }

        if (!cleanUrl) {
            statusText.innerText = "❌ Please enter a valid URL endpoint.";
            statusText.style.color = "#E50914";
            return;
        }

        chrome.storage.local.set({ 'CLOUD_SERVER_URL': cleanUrl }, () => {
            statusText.innerText = "💾 Configuration Saved Successfully!";
            statusText.style.color = "#2ecc71";
            console.log(`Cloud endpoint targeting updated explicitly to: ${cleanUrl}`);

            setTimeout(() => {
                statusText.innerText = "";
            }, 2500);
        });
    });
});