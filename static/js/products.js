document.addEventListener("DOMContentLoaded", function () {

    const addModal = document.getElementById("addModal");
    const editModal = document.getElementById("editModal");
    const editForm = document.getElementById("editForm");
    const toast = document.getElementById("toast");

    const searchInput = document.getElementById("searchInput");
    const tableBody = document.querySelector(".product-table tbody");
    const sortSelect = document.getElementById("sortSelect");

    // =========================
    // TOAST SYSTEM
    // =========================
    function showToast(message, type = "success") {

        if (!toast) return;

        toast.textContent = message;
        toast.className = `toast ${type}`;

        void toast.offsetWidth;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 2500);
    }

    window.showToast = showToast;

    // =========================
    // URL PARAM TOASTS
    // =========================
    function consumeParam(param, message) {

        const url = new URL(window.location.href);

        if (url.searchParams.get(param) === "1") {

            showToast(message, "success");

            url.searchParams.delete(param);

            window.history.replaceState(
                {},
                document.title,
                url.pathname + url.search
            );
        }
    }

    consumeParam("added", "Item added successfully!");
    consumeParam("sold", "Item sold successfully!");
    consumeParam("updated", "Item updated successfully!");
    consumeParam("archived", "Item archived successfully!");

    // =========================
    // ADD MODAL
    // =========================
    if (addModal) {

        window.openAddModal = () => {
            addModal.classList.remove("hidden");
        };

        window.closeAddModal = () => {
            addModal.classList.add("hidden");
        };

        addModal.addEventListener("click", function (e) {
            if (e.target === addModal) {
                addModal.classList.add("hidden");
            }
        });
    }

    // =========================
    // EDIT MODAL
    // =========================
    if (editModal) {

        window.closeEditModal = () => {
            editModal.classList.add("hidden");
        };

        editModal.addEventListener("click", function (e) {
            if (e.target === editModal) {
                editModal.classList.add("hidden");
            }
        });
    }

    // =========================
    // EDIT BUTTON
    // =========================
    document.addEventListener("click", function (e) {

        if (!e.target.classList.contains("edit-btn")) return;

        const btn = e.target;
        const id = btn.dataset.id;

        const row = btn.closest("tr");
        const cells = row.querySelectorAll("td");

        editForm.action = "/edit/" + id;

        document.getElementById("edit_name").value =
            cells[1].innerText.trim();

        document.getElementById("edit_brand").value =
            cells[2].innerText.trim();

        document.getElementById("edit_category").value =
            cells[3].innerText.trim();

        document.getElementById("edit_buy_price").value =
            cells[4].innerText.replace("₱", "").trim();

        document.getElementById("edit_sell_price").value =
            cells[5].innerText.replace("₱", "").trim();

        editModal.classList.remove("hidden");
    });

    // =========================
    // ESC KEY
    // =========================
    document.addEventListener("keydown", function (e) {

        if (e.key === "Escape") {

            if (addModal) {
                addModal.classList.add("hidden");
            }

            if (editModal) {
                editModal.classList.add("hidden");
            }
        }
    });

    // =========================
    // SEARCH + FILTER
    // =========================
    if (searchInput && tableBody) {

        const rows = Array.from(
            tableBody.querySelectorAll("tr")
        );

        let currentFilter = "all";

        rows.forEach(row => {
            row.dataset.original =
                row.innerText.toLowerCase();
        });

        const chips =
            document.querySelectorAll(".chip");

        chips.forEach(chip => {

            chip.addEventListener("click", () => {

                chips.forEach(c =>
                    c.classList.remove("active")
                );

                chip.classList.add("active");

                currentFilter =
                    chip.dataset.filter;

                applyFilters();
            });
        });

        function applyFilters() {

            const query =
                searchInput.value
                    .toLowerCase()
                    .trim();

            rows.forEach(row => {

                const text =
                    row.dataset.original;

                const statusCell =
                    row.querySelector(
                        "td:nth-child(7)"
                    );

                const status =
                    statusCell
                        ? statusCell.innerText.toLowerCase()
                        : "";

                const matchSearch =
                    text.includes(query);

                const matchFilter =
                    currentFilter === "all" ||
                    (currentFilter === "available" &&
                        status.includes("available")) ||
                    (currentFilter === "sold" &&
                        status.includes("sold"));

                row.style.display =
                    (matchSearch && matchFilter)
                        ? ""
                        : "none";
            });
        }

        searchInput.addEventListener(
            "input",
            applyFilters
        );
    }

    // =========================
    // SORTING
    // =========================
    if (sortSelect && tableBody) {

        sortSelect.addEventListener(
            "change",
            function () {

                const rows = Array.from(
                    tableBody.querySelectorAll("tr")
                );

                const value = this.value;

                let sorted = [...rows];

                if (value === "name") {

                    sorted.sort((a, b) =>
                        a.children[1].innerText.localeCompare(
                            b.children[1].innerText
                        )
                    );
                }

                if (value === "price") {

                    sorted.sort((a, b) =>
                        parseFloat(
                            a.children[5].innerText.replace("₱", "")
                        ) -
                        parseFloat(
                            b.children[5].innerText.replace("₱", "")
                        )
                    );
                }

                sorted.forEach(row =>
                    tableBody.appendChild(row)
                );
            }
        );
    }

});