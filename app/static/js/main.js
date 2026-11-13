console.log("AI Security Operations Assistant loaded.");

async function checkBackend() {
    const statusText = document.getElementById("backend-status");
    const statusIndicator = document.querySelector(".status-indicator");

    try {
        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        statusText.textContent = `Backend ${data.status}`;
        statusIndicator.classList.add("online");
        console.log("Backend response:", data);
    } catch (error) {
        statusText.textContent = "Backend unavailable";
        statusIndicator.classList.add("offline");
        console.error("Backend connection failed:", error);
    }
}

checkBackend();
