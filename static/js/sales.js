document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // CHART
    // =========================
    const canvas = document.getElementById("salesChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const raw = document.getElementById("sales-data");

    if (!raw) return;

    const data = JSON.parse(raw.textContent || "{}");

    const dates = Array.isArray(data.dates) ? data.dates : [];
    const profits = Array.isArray(data.profits) ? data.profits : [];

    if (window.salesChartInstance) {
        window.salesChartInstance.destroy();
    }

    window.salesChartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: "Profit Over Time",
                data: profits,
                borderColor: "#60a5fa",
                borderWidth: 3,
                pointRadius: 4,
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // =========================
    // TABLE ELEMENTS
    // =========================
    const searchInput = document.getElementById("salesSearch");
    const filterSelect = document.getElementById("salesFilter");
    const sortSelect = document.getElementById("salesSort");
    const tableBody = document.querySelector(".product-table tbody");

    if (!searchInput || !filterSelect || !sortSelect || !tableBody) return;

    let rows = Array.from(tableBody.querySelectorAll("tr"));

    // store original data
    rows.forEach(row => {
        row.dataset.search = row.innerText.toLowerCase();

        // SAFE DATE FIX (manual parsing)
        const rawDate = row.children[0].innerText;

        // convert "YYYY-MM-DD HH:MM:SS" → ISO format
        const fixed = rawDate.replace(" ", "T");
        row.dataset.date = new Date(fixed).getTime() || 0;

        row.dataset.profit = parseFloat(
            row.children[5].innerText.replace("₱", "")
        ) || 0;

        row.dataset.revenue = parseFloat(
            row.children[4].innerText.replace("₱", "")
        ) || 0;
    });

    let currentFilter = "all";
    let currentSort = "latest";

    // =========================
    // APPLY FILTER + SORT TOGETHER (FIXED)
    // =========================
    function renderTable() {

        const query = searchInput.value.toLowerCase().trim();
        const now = new Date();

        let filtered = rows.filter(row => {

            const textMatch = row.dataset.search.includes(query);

            const rowDate = new Date(Number(row.dataset.date));

            let dateMatch = true;

            if (currentFilter === "today") {
                dateMatch = rowDate.toDateString() === now.toDateString();
            }

            if (currentFilter === "week") {
                const diff = (now - rowDate) / (1000 * 60 * 60 * 24);
                dateMatch = diff <= 7;
            }

            if (currentFilter === "month") {
                dateMatch =
                    rowDate.getMonth() === now.getMonth() &&
                    rowDate.getFullYear() === now.getFullYear();
            }

            return textMatch && dateMatch;
        });

        // SORT
        if (currentSort === "latest") {
            filtered.sort((a, b) => b.dataset.date - a.dataset.date);
        }

        if (currentSort === "profit") {
            filtered.sort((a, b) => b.dataset.profit - a.dataset.profit);
        }

        if (currentSort === "revenue") {
            filtered.sort((a, b) => b.dataset.revenue - a.dataset.revenue);
        }

        // re-render
        tableBody.innerHTML = "";
        filtered.forEach(row => tableBody.appendChild(row));
    }

    // =========================
    // EVENTS
    // =========================
    searchInput.addEventListener("input", renderTable);
    filterSelect.addEventListener("change", function () {
        currentFilter = this.value;
        renderTable();
    });

    sortSelect.addEventListener("change", function () {
        currentSort = this.value;
        renderTable();
    });

    // initial render
    renderTable();
});