document.addEventListener("DOMContentLoaded", function () {

    const toast = document.getElementById("toast");

    function showToast(message, type = "success") {

        if (!toast) {
            console.log("Toast missing");
            return;
        }

        toast.textContent = message;
        toast.className = "toast " + type;

        void toast.offsetWidth;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 2500);
    }

    // =========================
    // FORCE CHECK RESTORE PARAM
    // =========================
    const restored = new URLSearchParams(window.location.search).get("restored");

    if (restored === "1") {

        // delay ensures DOM + CSS fully loaded
        setTimeout(() => {
            showToast("Item restored successfully!", "success");
        }, 100);

        // clean URL so it won't repeat on refresh
        window.history.replaceState(
            {},
            document.title,
            window.location.pathname
        );
    }

    // =========================
    // SEARCH ONLY
    // =========================
    const search = document.getElementById("archiveSearch");

    if (search) {

        search.addEventListener("input", function () {

            const value = this.value.toLowerCase();

            const rows = document.querySelectorAll("#archiveTable tr");

            rows.forEach(row => {

                const text = row.innerText.toLowerCase();

                row.style.display =
                    text.includes(value) ? "" : "none";
            });
        });
    }

});