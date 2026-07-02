(() => {
    const lightbox = document.getElementById("image-lightbox");
    if (!lightbox) return;

    const previewImage = document.getElementById("lightbox-image");
    const previewCaption = document.getElementById("lightbox-caption");
    const modeButtons = lightbox.querySelectorAll("[data-lightbox-mode]");
    const closers = lightbox.querySelectorAll("[data-close-lightbox]");
    const zoomableImages = document.querySelectorAll(".js-zoomable");

    let state = {
        before: "",
        after: "",
        mode: "before",
        title: "",
    };

    const renderMode = () => {
        previewImage.src = state.mode === "before" ? state.before : state.after;
        previewImage.alt = `${state.mode} ${state.title}`.trim();
        previewCaption.textContent = `${state.title} - ${state.mode.toUpperCase()}`;
        modeButtons.forEach((btn) => {
            btn.classList.toggle("active", btn.dataset.lightboxMode === state.mode);
        });
    };

    const openLightbox = () => {
        lightbox.hidden = false;
        document.body.style.overflow = "hidden";
        renderMode();
    };

    const closeLightbox = () => {
        lightbox.hidden = true;
        document.body.style.overflow = "";
    };

    zoomableImages.forEach((img) => {
        img.addEventListener("click", () => {
            state = {
                before: img.dataset.before || img.src,
                after: img.dataset.after || img.src,
                mode: img.dataset.initial || "before",
                title: img.dataset.title || "Preview",
            };
            openLightbox();
        });
    });

    modeButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            state.mode = btn.dataset.lightboxMode;
            renderMode();
        });
    });

    lightbox.addEventListener(
        "wheel",
        (event) => {
            if (lightbox.hidden) return;
            event.preventDefault();
            state.mode = event.deltaY > 0 ? "after" : "before";
            renderMode();
        },
        { passive: false }
    );

    document.addEventListener("keydown", (event) => {
        if (lightbox.hidden) return;
        if (event.key === "Escape") closeLightbox();
        if (event.key === "ArrowRight") {
            state.mode = "after";
            renderMode();
        }
        if (event.key === "ArrowLeft") {
            state.mode = "before";
            renderMode();
        }
    });

    closers.forEach((node) => node.addEventListener("click", closeLightbox));
})();
