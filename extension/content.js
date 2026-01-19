/**
 * College Project PiP Linker - Content Script
 * Monitors the browser DOM for active video players and injects a cloud-linked control button.
 */

function injectPipButton() {
    // Locate common HTML5 video elements (YouTube, Vimeo, Twitch, etc.)
    const video = document.querySelector('video');

    // Prevent duplicate injections if the button already exists on the page
    if (video && !document.getElementById('custom-python-pip-btn')) {
        const btn = document.createElement('button');
        btn.id = 'custom-python-pip-btn';
        btn.innerText = '🚀 Send to Cloud PiP';

        // Premium high-visibility styling to match player overlays
        btn.style.position = 'absolute';
        btn.style.top = '12px';
        btn.style.left = '12px';
        btn.style.zIndex = '99999';
        btn.style.background = '#E50914'; // Sharp streaming-red background
        btn.style.color = '#FFFFFF';
        btn.style.border = 'none';
        btn.style.padding = '8px 14px';
        btn.style.cursor = 'pointer';
        btn.style.borderRadius = '4px';
        btn.style.fontWeight = 'bold';
        btn.style.fontSize = '12px';
        btn.style.boxShadow = '0px 4px 10px rgba(0, 0, 0, 0.5)';
        btn.style.transition = 'background 0.2s ease-in-out';

        // Add a simple hover feedback effect
        btn.addEventListener('mouseenter', () => {
            btn.style.background = '#FF1E27';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.background = '#E50914';
        });

        // Trigger network payload transfer on click
        btn.addEventListener('click', () => {
            // Read saved deployment server address dynamically from local Chrome runtime storage
            chrome.storage.local.get(['cloudUrl'], (result) => {
                const baseServerUrl = result.cloudUrl ? result.cloudUrl.replace(/\/$/, "") : "https://your-pip-project.onrender.com";
                const targetEndpoint = `${baseServerUrl}/open-pip`;

                console.log(`[PiP Linker] Forwarding stream request to endpoint: ${targetEndpoint}`);

                fetch(targetEndpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: window.location.href })
                })
                    .then(res => {
                        if (res.ok) {
                            console.log('[PiP Linker] Signal successfully broadcasted to cloud orchestration mesh.');
                        } else {
                            alert(`Server returned an error status: ${res.status}`);
                        }
                    })
                    .catch(err => {
                        console.error('[PiP Linker] Dispatch error:', err);
                        alert('Cloud endpoint configuration mismatch or server is sleeping. Right-click the extension icon and verify your Options URL setup.');
                    });
            });
        });

        // Append the action control button securely onto the video container layer
        video.parentElement.appendChild(btn);
    }
}

// Keep a persistent cycle loop running every 2000ms to catch dynamic page mutations and layout transitions
setInterval(injectPipButton, 2000);