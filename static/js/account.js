document.addEventListener("DOMContentLoaded", function () {

    const toast = document.getElementById("toast");

    if (!toast) {
        console.error("Toast element not found!");
        return;
    }

    function showToast(message, type = "success") {

        toast.className = "toast";
        toast.textContent = message;

        void toast.offsetWidth;

        toast.classList.add(type);
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 2500);
    }

    // ✅ READ FROM HTML SCRIPT TAG (FIX)
    const flashScript = document.getElementById("flash-data");

    let messages = [];

    try {
        messages = JSON.parse(flashScript.textContent || "[]");
    } catch (err) {
        console.error("Flash parse error:", err);
    }

    console.log("Flash messages:", messages);

    messages.forEach(([category, message]) => {
        showToast(message, category);
    });

});