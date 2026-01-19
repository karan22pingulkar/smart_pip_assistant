chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "open_pip") {

        // Dynamically extract production configuration keys from client memory storage 
        chrome.storage.local.get(['CLOUD_SERVER_URL'], (result) => {
            const serverUrl = result.CLOUD_SERVER_URL;

            if (!serverUrl) {
                console.error("Missing server configuration. Please configure the extension options.");
                sendResponse({ status: "error", error: "Missing Server Endpoint Configuration" });
                return;
            }

            console.log(`[Production Linker] Dispatching stream request payload to cloud endpoint: ${serverUrl}/open-pip`);

            fetch(`${serverUrl}/open-pip`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: request.url })
            })
                .then(response => {
                    if (!response.ok) throw new Error(`Server returned status code: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log("Cloud execution framework response received:", data);
                    sendResponse({ status: "success", data: data });
                })
                .catch(err => {
                    console.error("Cloud distribution gateway route error:", err);
                    sendResponse({ status: "error", error: err.message });
                });
        });

        return true; // Keep the message channel open asynchronously
    }
});