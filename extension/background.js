chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "open_pip") {

        // Dynamically query client memory engine assets
        chrome.storage.local.get(['CLOUD_SERVER_URL'], (result) => {
            const serverUrl = result.CLOUD_SERVER_URL;

            if (!serverUrl) {
                const errorMsg = "⚠️ Production endpoint configuration missing! Right-click the extension icon and select Options to configure your Render URL.";
                console.error(errorMsg);
                // Alert the user directly on their active page via content script channel
                sendResponse({ status: "error", error: errorMsg });
                return;
            }

            console.log(`[Production Gateway] Dispatching payload to endpoint: ${serverUrl}/open-pip`);

            fetch(`${serverUrl}/open-pip`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: request.url })
            })
                .then(response => {
                    if (!response.ok) throw new Error(`Server returned network status code: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log("Transmission wave received successfully by cloud instance:", data);
                    sendResponse({ status: "success", data: data });
                })
                .catch(err => {
                    console.error("Cloud distribution core route connection fault:", err);
                    sendResponse({ status: "error", error: err.message });
                });
        });

        return true; // Keep asynchronous framework message boundary open
    }
});