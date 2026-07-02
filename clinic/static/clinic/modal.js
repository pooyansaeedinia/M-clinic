(() => {
    const openButtons = document.querySelectorAll("[data-open-modal]");
    if (!openButtons.length) return;

    const closeModal = (modal) => {
        modal.hidden = true;
        document.body.style.overflow = "";
    };

    const openModal = (modal) => {
        modal.hidden = false;
        document.body.style.overflow = "hidden";
    };

    openButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const modalId = button.dataset.openModal;
            if (!modalId) return;
            const modal = document.getElementById(modalId);
            if (!modal) return;
            openModal(modal);
        });
    });

    document.querySelectorAll(".app-modal").forEach((modal) => {
        modal.querySelectorAll("[data-close-modal]").forEach((closer) => {
            closer.addEventListener("click", () => closeModal(modal));
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;
        document.querySelectorAll(".app-modal").forEach((modal) => {
            if (!modal.hidden) closeModal(modal);
        });
    });
})();
