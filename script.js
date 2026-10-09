let pollInterval = null;

async function startApp() {
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;

    await fetch('/start', { method: 'POST' });
    pollInterval = setInterval(updateStatus, 800);
}

async function stopApp() {
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;

    await fetch('/stop', { method: 'POST' });

    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    document.getElementById('status').innerText = 'Stopped ⏹️';
}

async function updateStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();

        document.getElementById('status').innerText = data.status;

        if (data.english) {
            document.getElementById('english').innerText = data.english;
        }
        if (data.hindi) {
            document.getElementById('hindi').innerText = data.hindi;
        }

        if (!data.running) {
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
            }
        }
    } catch (e) {
        console.log("Polling error:", e);
    }
}