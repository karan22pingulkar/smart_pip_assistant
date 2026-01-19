document.getElementById('saveBtn').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;
    chrome.storage.local.set({ cloudUrl: url }, () => {
        alert('Endpoint settings saved successfully!');
    });
});

// Load existing saved URL profile on open
chrome.storage.local.get(['cloudUrl'], (result) => {
    if (result.cloudUrl) document.getElementById('urlInput').value = result.cloudUrl;
});