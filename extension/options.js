document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('serverUrl');
    const saveButton = document.getElementById('saveBtn');
    const statusText = document.getElementById('status');

    // Load saved configurations
    chrome.storage.local.get(['CLOUD_SERVER_URL'], (result) => {
        if (result.CLOUD_SERVER_URL) {
            urlInput.value = result.CLOUD_SERVER_URL;
            console.log("Current stored URL config:", result.CLOUD_SERVER_URL);
        }
    });

    // Save configuration updates
    saveButton.addEventListener('click', () => {
        let cleanUrl = urlInput.value.trim().replace(/\/$/, ""); // Automatically strips trailing slash

        if (!cleanUrl) {
            statusText.innerText = "❌ URL can't be blank";
            statusText.style.color = "#E50914";
            return;
        }

        chrome.storage.local.set({ 'CLOUD_SERVER_URL': cleanUrl }, () => {
            statusText.innerText = "💾 Saved Successfully!";
            statusText.style.color = "#2ecc71";
            console.log("Storage committed configuration:", cleanUrl);

            // Double check validation check
            chrome.storage.local.get(['CLOUD_SERVER_URL'], (verify) => {
                console.log("Double checking storage allocation:", verify.CLOUD_SERVER_URL);
            });
        });
    });
});