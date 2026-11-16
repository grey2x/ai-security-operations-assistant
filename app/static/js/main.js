
console.log("AI Security Operations Assistant loaded.");

// Check whether the Flask backend is running.
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


// Safely read JSON responses from Flask.
async function readJsonResponse(response) {
    const text = await response.text();

    try {
        return JSON.parse(text);
    } catch {
        throw new Error(
            `Server returned an invalid response (HTTP ${response.status}). Check the Flask terminal.`
        );
    }
}


// Load detected security alerts.
async function loadSecurityAlerts() {
    const alertsContainer = document.getElementById("alerts-container");

    try {
        const response = await fetch("/api/analyse-samples");
        const data = await readJsonResponse(response);

        if (!response.ok) {
            throw new Error(data.error || "Unable to load alerts.");
        }

        document.getElementById("total-events").textContent =
            data.total_events;

        document.getElementById("security-alerts").textContent =
            data.total_alerts;

        alertsContainer.replaceChildren();

        if (data.alerts.length === 0) {
            alertsContainer.textContent = "No security alerts detected.";
            return;
        }

        data.alerts.forEach(alert => {
            const alertCard = document.createElement("div");
            alertCard.classList.add("alert-card");

            const title = document.createElement("h3");
            title.textContent = alert.title;

            const severity = document.createElement("p");
            severity.textContent = `Severity: ${alert.severity}`;

            const source = document.createElement("p");
            source.textContent = `Source IP: ${alert.source_ip}`;

            const attempts = document.createElement("p");
            attempts.textContent = `Failed attempts: ${alert.failed_attempts}`;

            const rule = document.createElement("p");
            rule.textContent = `Detection rule: ${alert.rule_id}`;

            alertCard.append(title, severity, source, attempts, rule);
            alertsContainer.appendChild(alertCard);
        });

    } catch (error) {
        alertsContainer.textContent = error.message;
        console.error("Alert loading failed:", error);
    }
}


// Request AI analysis for an incident.
async function analyseIncident(incident, button, resultContainer) {
    button.disabled = true;
    button.textContent = "Analysing...";
    resultContainer.textContent = "Waiting for AI analysis...";

    try {
        const response = await fetch("/api/ai-analysis", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(incident)
        });

        const data = await readJsonResponse(response);

        if (!response.ok) {
            throw new Error(
                data.details || data.error || "AI analysis failed."
            );
        }

        resultContainer.textContent = data.analysis;

    } catch (error) {
        resultContainer.textContent = `Analysis failed: ${error.message}`;
        console.error("AI analysis failed:", error);

    } finally {
        button.disabled = false;
        button.textContent = "Analyse with AI";
    }
}


// Load previously recorded incidents.
async function loadIncidents() {
    const incidentsContainer = document.getElementById("incidents-container");

    try {
        const response = await fetch("/api/incidents");
        const data = await readJsonResponse(response);

        if (!response.ok) {
            throw new Error(data.error || "Unable to load incidents.");
        }

        document.getElementById("incidents").textContent =
            data.total_incidents;

        incidentsContainer.replaceChildren();

        if (data.incidents.length === 0) {
            incidentsContainer.textContent = "No recorded incidents.";
            return;
        }

        data.incidents.forEach(incident => {
            const incidentCard = document.createElement("div");
            incidentCard.classList.add("incident-card");

            const title = document.createElement("h3");
            title.textContent = incident.title;

            const severity = document.createElement("p");
            severity.textContent = `Severity: ${incident.severity}`;

            const source = document.createElement("p");
            source.textContent = `Source IP: ${incident.source_ip}`;

            const attempts = document.createElement("p");
            attempts.textContent = `Failed attempts: ${incident.failed_attempts}`;

            const username = document.createElement("p");
            username.textContent =
                `Username(s): ${incident.usernames.join(", ")}`;

            const rule = document.createElement("p");
            rule.textContent = `Rule ID: ${incident.rule_id}`;

            const analyseButton = document.createElement("button");
            analyseButton.textContent = "Analyse with AI";
            analyseButton.classList.add("ai-analysis-button");

            const analysisResult = document.createElement("div");
            analysisResult.classList.add("ai-analysis-result");

            analyseButton.addEventListener("click", () => {
                analyseIncident(
                    incident,
                    analyseButton,
                    analysisResult
                );
            });

            incidentCard.append(
                title,
                severity,
                source,
                attempts,
                username,
                rule,
                analyseButton,
                analysisResult
            );

            incidentsContainer.appendChild(incidentCard);
        });

    } catch (error) {
        incidentsContainer.textContent = error.message;
        console.error("Incident loading failed:", error);
    }
}


// Initialise the dashboard in the correct order.
async function initialiseDashboard() {
    await Promise.all([
        checkBackend(),
        loadSecurityAlerts()
    ]);

    await loadIncidents();
}

initialiseDashboard();

