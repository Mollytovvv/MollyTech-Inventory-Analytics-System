document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("profitChart");

    if (!canvas) {
        console.error("profitChart canvas NOT FOUND");
        return;
    }

    if (typeof Chart === "undefined") {
        console.error("Chart.js NOT LOADED");
        return;
    }

    const ctx = canvas.getContext("2d");

    // =========================
    // READ JSON DATA
    // =========================
    const raw = document.getElementById("chart-data");

    if (!raw) {
        console.error("chart-data JSON not found");
        return;
    }

    const data = JSON.parse(raw.textContent || "{}");

    const allDates = Array.isArray(data.dates) ? data.dates : [];

    const allRevenue = Array.isArray(data.revenue)
        ? data.revenue.map(v => Number(v) || 0)
        : [];

    const allProfit = Array.isArray(data.profit)
        ? data.profit.map(v => Number(v) || 0)
        : [];

    console.log("DATES:", allDates);
    console.log("REVENUE:", allRevenue);
    console.log("PROFIT:", allProfit);

    // =========================
    // CHART INSTANCE
    // =========================
    let chart;

    function createChart(labels, revenue, profit) {

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: "line",

            data: {
                labels: labels,

                datasets: [
                    {
                        label: "Revenue",
                        data: revenue,
                        borderColor: "#22c55e",
                        backgroundColor: "rgba(34,197,94,0.12)",
                        borderWidth: 4,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        pointBackgroundColor: "#22c55e",
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: "Profit",
                        data: profit,
                        borderColor: "#3b82f6",
                        backgroundColor: "rgba(59,130,246,0.12)",
                        borderWidth: 4,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        pointBackgroundColor: "#3b82f6",
                        fill: false,
                        tension: 0.3
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                plugins: {
                    legend: {
                        labels: {
                            color: "#e5e7eb",
                            font: { size: 13 }
                        }
                    }
                },

                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(148,163,184,0.08)" }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(148,163,184,0.08)" }
                    }
                }
            }
        });
    }

    // =========================
    // INITIAL LOAD
    // =========================
    createChart(allDates, allRevenue, allProfit);

    // =========================
    // FILTER FUNCTION (SAFE)
    // =========================
    function getLast(n) {
        const start = Math.max(allDates.length - n, 0);

        return {
            dates: allDates.slice(start),
            revenue: allRevenue.slice(start),
            profit: allProfit.slice(start)
        };
    }

    // =========================
    // BUTTON HANDLER (OPTIONAL)
    // =========================
    const buttons = document.querySelectorAll(".chart-btn");

    if (buttons.length > 0) {

        buttons.forEach(btn => {
            btn.addEventListener("click", function () {

                buttons.forEach(b => b.classList.remove("active"));
                this.classList.add("active");

                const type = this.textContent.trim().toLowerCase();

                let filtered;

                if (type === "day") {
                    filtered = getLast(1);
                }
                else if (type === "week") {
                    filtered = getLast(7);
                }
                else if (type === "month") {
                    filtered = getLast(30);
                }
                else {
                    filtered = {
                        dates: allDates,
                        revenue: allRevenue,
                        profit: allProfit
                    };
                }

                createChart(filtered.dates, filtered.revenue, filtered.profit);
            });
        });
    }

});