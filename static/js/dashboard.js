async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        // =========================
        // Asset statistics
        // =========================

        document.getElementById("total-assets").textContent =
            data.assets.total;

        document.getElementById("assigned-assets").textContent =
            data.assets.assigned;

        document.getElementById("available-assets").textContent =
            data.assets.available;

        document.getElementById("repair-assets").textContent =
            data.assets.under_repair;

        document.getElementById("retired-assets").textContent =
            data.assets.retired;


        // =========================
        // Ticket statistics
        // =========================

        document.getElementById("total-tickets").textContent =
            data.tickets.total;

        document.getElementById("open-tickets").textContent =
            data.tickets.open;

        document.getElementById("assigned-tickets").textContent =
            data.tickets.assigned;

        document.getElementById("progress-tickets").textContent =
            data.tickets.in_progress;

        document.getElementById("resolved-tickets").textContent =
            data.tickets.resolved;

        document.getElementById("closed-tickets").textContent =
            data.tickets.closed;

        document.getElementById("high-priority-tickets").textContent =
            data.tickets.high_priority;


        // =========================
        // Assets by type
        // =========================

        const assetTable =
            document.getElementById("asset-type-table");

        assetTable.innerHTML = "";

        for (const type in data.assets.by_type) {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${type}</td>
                <td>${data.assets.by_type[type]}</td>
            `;

            assetTable.appendChild(row);
        }


        // =========================
        // Tickets by department
        // =========================

        const departmentTable =
            document.getElementById("department-table");

        departmentTable.innerHTML = "";

        for (const department in data.tickets.by_department) {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${department}</td>
                <td>${data.tickets.by_department[department]}</td>
            `;

            departmentTable.appendChild(row);
        }

    } catch (error) {

        console.error(
            "Error loading dashboard:",
            error
        );

    }
}


// Load dashboard when page opens
loadDashboard();