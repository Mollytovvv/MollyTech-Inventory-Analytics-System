
// =========================
// PASSWORD TOGGLE
// =========================
function togglePassword() {
    const passwordInput = document.getElementById("password");

    if (!passwordInput) return;

    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}


// =========================
// FORGOT PASSWORD MODAL
// =========================
function openModal(e) {
    e.preventDefault();

    const modal = document.getElementById("forgotModal");
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeModal() {
    const modal = document.getElementById("forgotModal");
    if (modal) {
        modal.style.display = "none";
    }
}


// =========================
// CLOSE MODAL WHEN CLICKING OUTSIDE
// =========================
window.onclick = function(event) {
    const modal = document.getElementById("forgotModal");

    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
}


// =========================
// TOAST SYSTEM
// =========================
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");

    if (!toast) return;

    toast.innerText = message;
    toast.className = "toast show " + type;

    setTimeout(() => {
        toast.className = "toast";
    }, 3000);
}


// =========================
// FLASK FLASH → TOAST CONVERTER
// =========================
window.addEventListener("DOMContentLoaded", () => {

    const alerts = document.querySelectorAll(".alert");

    if (alerts.length > 0) {

        alerts.forEach(alert => {

            const message = alert.innerText.trim();

            let type = "success";

            if (alert.classList.contains("alert-error")) {
                type = "error";
            }

            showToast(message, type);
        });

        // OPTIONAL: auto hide flash blocks after converting to toast
        setTimeout(() => {
            alerts.forEach(a => a.style.display = "none");
        }, 100);
    }
});


// =========================
// AUTO CLOSE MODAL ON SUCCESS
// =========================
window.addEventListener("DOMContentLoaded", () => {

    const successAlerts = document.querySelectorAll(".alert-success");

    if (successAlerts.length > 0) {
        setTimeout(() => {
            closeModal();
        }, 800);
    }
});