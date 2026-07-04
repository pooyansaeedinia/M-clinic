(() => {
    const lightbox = document.getElementById("image-lightbox");
    if (!lightbox) return;

    const previewImage = document.getElementById("lightbox-image");
    const previewCaption = document.getElementById("lightbox-caption");
    const modeButtons = lightbox.querySelectorAll("[data-lightbox-mode]");
    const closers = lightbox.querySelectorAll("[data-close-lightbox]");
    const triggers = document.querySelectorAll(".js-gallery-trigger");
    const prevBtn = lightbox.querySelector("[data-lightbox-prev]");
    const nextBtn = lightbox.querySelector("[data-lightbox-next]");

    let state = {
        sectionIndex: "0",
        slides: [],
        index: 0,
        mode: "before",
    };

    const buildSlides = (sectionIndex, mode) => {
        const selector = `.js-gallery-trigger[data-section-index="${sectionIndex}"][data-mode="${mode}"]`;
        return Array.from(document.querySelectorAll(selector)).map((node) => ({
            src: node.src,
            title: node.dataset.title || "Preview",
        }));
    };

    const renderSlide = () => {
        const slide = state.slides[state.index];
        if (!slide) return;
        previewImage.src = slide.src;
        previewImage.alt = slide.title;
        previewCaption.textContent = `${slide.title} - ${state.mode.toUpperCase()} (${state.index + 1}/${state.slides.length})`;
        modeButtons.forEach((btn) => {
            btn.classList.toggle("active", btn.dataset.lightboxMode === state.mode);
        });
    };

    const openLightbox = () => {
        if (!state.slides.length) return;
        lightbox.hidden = false;
        document.body.style.overflow = "hidden";
        renderSlide();
    };

    const closeLightbox = () => {
        lightbox.hidden = true;
        document.body.style.overflow = "";
    };

    const step = (direction) => {
        if (!state.slides.length) return;
        state.index = (state.index + direction + state.slides.length) % state.slides.length;
        renderSlide();
    };

    const loadSlides = () => {
        state.slides = buildSlides(state.sectionIndex, state.mode);
        if (state.index >= state.slides.length) {
            state.index = 0;
        }
    };

    triggers.forEach((img) => {
        img.addEventListener("click", () => {
            state.sectionIndex = img.dataset.sectionIndex || "0";
            state.mode = img.dataset.mode || "before";
            state.index = Number(img.dataset.slideIndex) || 0;
            loadSlides();
            openLightbox();
        });
    });

    modeButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            state.mode = btn.dataset.lightboxMode;
            state.index = 0;
            loadSlides();
            renderSlide();
        });
    });

    if (prevBtn) prevBtn.addEventListener("click", () => step(-1));
    if (nextBtn) nextBtn.addEventListener("click", () => step(1));

    lightbox.addEventListener(
        "wheel",
        (event) => {
            if (lightbox.hidden) return;
            event.preventDefault();
            step(event.deltaY > 0 ? 1 : -1);
        },
        { passive: false }
    );

    document.addEventListener("keydown", (event) => {
        if (lightbox.hidden) return;
        if (event.key === "Escape") closeLightbox();
        if (event.key === "ArrowRight") step(1);
        if (event.key === "ArrowLeft") step(-1);
    });

    closers.forEach((node) => node.addEventListener("click", closeLightbox));
})();
