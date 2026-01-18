// Replace this placeholder link with your live Render Web URL after deployment!
const CLOUD_URL = "https://your-pip-project.onrender.com/open-pip";

function injectPipButton() {
    const video = document.querySelector('video');

    if (video && !document.getElementById('custom-python-pip-btn')) {
        const btn = document.createElement('button');
        btn.id = 'custom-python-pip-btn';
        btn.innerText = '🚀 Send to Cloud PiP';

        btn.style.position = 'absolute';
        btn.style.top = '10px';
        btn.style.left = '10px';
        btn.style.zIndex = '99999';
        btn.style.background = '#FF0000';
        btn.style.color = '#FFFFFF';
        btn.style.border = 'none';
        btn.style.padding = '8px 12px';
        btn.style.cursor = 'pointer';
        btn.style.borderRadius = '4px';
        btn.style.fontWeight = 'bold';

        btn.addEventListener('click', () => {
            fetch(CLOUD_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: window.location.href })
            })
                .then(res => console.log('Sent to Cloud Server!'))
                .catch(err => alert('Cloud server is waking up or down. Please try again in a moment.'));
        });

        video.parentElement.appendChild(btn);
    }
}

// Check every 2 seconds for fresh video elements on dynamic layout updates
setInterval(injectPipButton, 2000);