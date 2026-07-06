(() => {
    const lightbox = document.getElementById("image-lightbox");
    if (!lightbox) return;

    const scrollArea = document.getElementById("lightbox-scroll-area");
    const counterEl = document.getElementById("lightbox-counter");
    const modeButtons = lightbox.querySelectorAll("[data-lightbox-mode]");
    const closers = lightbox.querySelectorAll("[data-close-lightbox]");
    const caseCards = document.querySelectorAll(".js-case-card");

    const previewLightbox = document.getElementById("image-preview-lightbox");
    const previewImage = document.getElementById("image-preview-img");
    const previewCaption = document.getElementById("image-preview-caption");
    const previewActions = document.getElementById("image-preview-actions");
    const previewBackdrop = previewLightbox?.querySelector(".image-preview-backdrop");
    const previewDialog = previewLightbox?.querySelector(".image-preview-dialog");
    const previewClosers = previewLightbox
        ? previewLightbox.querySelectorAll("[data-close-preview]")
        : [];

    const dataElement = document.getElementById("gallery-sections-data");
    const metaElement = document.getElementById("gallery-meta");
    const galleryData = dataElement ? JSON.parse(dataElement.textContent) : [];
    const galleryMeta = metaElement ? JSON.parse(metaElement.textContent) : { can_manage: false };

    let state = {
        sectionIndex: 0,
        mode: "before",
        activeSlide: null,
    };

    const getSlides = () => {
        const section = galleryData[state.sectionIndex];
        if (!section) return [];
        return section[state.mode] || [];
    };

    const stopActionPropagation = (node) => {
        node.addEventListener("click", (event) => event.stopPropagation());
    };

    const createCrudBar = (slide, variant = "slide") => {
        if (!galleryMeta.can_manage || !slide.edit_url || !slide.delete_url) return null;

        const bar = document.createElement("div");
        bar.className =
            variant === "preview" ? "image-preview-actions-inner" : "lightbox-slide-actions";
        stopActionPropagation(bar);

        const editLink = document.createElement("a");
        editLink.href = slide.edit_url;
        editLink.className = "btn btn-outline btn-small gallery-crud-btn";
        editLink.textContent = galleryMeta.labels.edit;

        const form = document.createElement("form");
        form.method = "post";
        form.action = slide.delete_url;
        form.addEventListener("submit", (event) => {
            if (!window.confirm(galleryMeta.labels.confirm_delete)) {
                event.preventDefault();
            }
        });

        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = galleryMeta.csrf_token || "";

        const deleteBtn = document.createElement("button");
        deleteBtn.type = "submit";
        deleteBtn.className = "btn btn-danger btn-small gallery-crud-btn";
        deleteBtn.textContent = galleryMeta.labels.delete;

        form.append(csrfInput, deleteBtn);
        bar.append(editLink, form);
        return bar;
    };

    const renderPreviewActions = (slide) => {
        if (!previewActions) return;
        previewActions.innerHTML = "";
        const bar = createCrudBar(slide, "preview");
        if (!bar) {
            previewActions.hidden = true;
            return;
        }
        previewActions.appendChild(bar);
        previewActions.hidden = false;
    };

    const openPreview = (slide) => {
        if (!previewLightbox || !previewImage || !previewCaption) return;
        if (!previewLightbox.hidden) return;

        state.activeSlide = slide;
        previewCaption.textContent = slide.title || "";
        renderPreviewActions(slide);

        previewImage.src = slide.src;
        previewImage.alt = slide.title || "Gallery image";

        previewLightbox.hidden = false;
        previewLightbox.classList.remove("is-closing");
        previewLightbox.offsetHeight;
        previewLightbox.classList.add("is-open");
        document.body.classList.add("preview-open");
    };

    const closePreview = () => {
        if (!previewLightbox || previewLightbox.hidden) return;

        previewLightbox.classList.remove("is-open");
        previewLightbox.classList.add("is-closing");

        const finishClose = () => {
            previewLightbox.hidden = true;
            previewLightbox.classList.remove("is-closing");
            document.body.classList.remove("preview-open");
            state.activeSlide = null;
            if (previewImage) {
                previewImage.src = "";
                previewImage.alt = "";
            }
            if (previewCaption) previewCaption.textContent = "";
            if (previewActions) {
                previewActions.innerHTML = "";
                previewActions.hidden = true;
            }
        };

        if (!previewDialog) {
            finishClose();
            return;
        }

        const onEnd = (event) => {
            if (event.target !== previewDialog) return;
            previewDialog.removeEventListener("transitionend", onEnd);
            finishClose();
        };

        previewDialog.addEventListener("transitionend", onEnd);
        window.setTimeout(finishClose, 300);
    };

    const bindSlidePreview = (imageWrap, image, slide) => {
        image.draggable = false;
        image.classList.add("js-preview-trigger");

        let pointerStart = null;
        let pointerMoved = false;

        const resetPointer = () => {
            pointerStart = null;
            pointerMoved = false;
        };

        imageWrap.addEventListener("pointerdown", (event) => {
            if (event.target.closest(".lightbox-slide-actions, a, button, form")) return;
            pointerStart = { x: event.clientX, y: event.clientY };
            pointerMoved = false;
        });

        imageWrap.addEventListener("pointermove", (event) => {
            if (!pointerStart) return;
            const dx = Math.abs(event.clientX - pointerStart.x);
            const dy = Math.abs(event.clientY - pointerStart.y);
            if (dx > 6 || dy > 6) pointerMoved = true;
        });

        imageWrap.addEventListener("pointerup", resetPointer);
        imageWrap.addEventListener("pointercancel", resetPointer);

        imageWrap.addEventListener("click", (event) => {
            if (event.target.closest(".lightbox-slide-actions, a, button, form")) return;
            if (pointerMoved) {
                pointerMoved = false;
                return;
            }

            event.preventDefault();
            event.stopPropagation();
            openPreview(slide);
            pointerMoved = false;
        });
    };

    const updateCounter = (total) => {
        if (!counterEl) return;
        if (!total) {
            counterEl.hidden = true;
            counterEl.textContent = "";
            return;
        }
        counterEl.hidden = false;
        counterEl.textContent = `${total} ${total === 1 ? galleryMeta.labels.image_singular : galleryMeta.labels.image_plural}`;
    };

    const renderSlides = () => {
        if (!scrollArea) return;
        const slides = getSlides();
        scrollArea.innerHTML = "";

        if (!slides.length) {
            const empty = document.createElement("p");
            empty.className = "lightbox-empty";
            empty.textContent =
                state.mode === "before"
                    ? lightbox.dataset.emptyBefore || "No before images."
                    : lightbox.dataset.emptyAfter || "No after images.";
            scrollArea.appendChild(empty);
            updateCounter(0);
            return;
        }

        slides.forEach((slide, index) => {
            const item = document.createElement("figure");
            item.className = "lightbox-slide";
            item.style.animationDelay = `${index * 70}ms`;
            item.id = `lightbox-slide-${index}`;

            const imageWrap = document.createElement("div");
            imageWrap.className = "lightbox-slide-media";

            const indexBadge = document.createElement("span");
            indexBadge.className = "lightbox-slide-index";
            indexBadge.textContent = String(index + 1).padStart(2, "0");

            const zoomHint = document.createElement("span");
            zoomHint.className = "lightbox-zoom-hint";
            zoomHint.textContent = galleryMeta.labels?.zoom_hint || "Tap to enlarge";

            const image = document.createElement("img");
            image.src = slide.src;
            image.alt = slide.title || "Gallery image";
            image.loading = index < 2 ? "eager" : "lazy";
            image.decoding = "async";

            const caption = document.createElement("figcaption");
            caption.className = "lightbox-caption";
            caption.textContent = slide.title || "";

            const crudBar = createCrudBar(slide, "slide");
            if (crudBar) imageWrap.appendChild(crudBar);

            imageWrap.append(indexBadge, image, zoomHint);
            item.appendChild(imageWrap);
            item.appendChild(caption);
            scrollArea.appendChild(item);

            bindSlidePreview(imageWrap, image, slide);
        });

        updateCounter(slides.length);
        scrollArea.scrollLeft = 0;
    };

    const syncModeButtons = () => {
        modeButtons.forEach((button) => {
            button.classList.toggle("active", button.dataset.lightboxMode === state.mode);
        });
    };

    const openLightbox = () => {
        renderSlides();
        syncModeButtons();
        lightbox.hidden = false;
        requestAnimationFrame(() => {
            lightbox.classList.add("is-open");
        });
        document.body.classList.add("lightbox-open");
    };

    const closeLightbox = () => {
        if (previewLightbox && !previewLightbox.hidden) {
            closePreview();
            return;
        }

        lightbox.classList.remove("is-open");
        lightbox.classList.add("is-closing");

        const finishClose = () => {
            lightbox.hidden = true;
            lightbox.classList.remove("is-closing");
            document.body.classList.remove("lightbox-open");
            if (scrollArea) scrollArea.innerHTML = "";
            updateCounter(0);
        };

        const panel = lightbox.querySelector(".lightbox-panel");
        if (!panel) {
            finishClose();
            return;
        }

        const onEnd = (event) => {
            if (event.target !== panel) return;
            panel.removeEventListener("transitionend", onEnd);
            finishClose();
        };

        panel.addEventListener("transitionend", onEnd);
        window.setTimeout(finishClose, 340);
    };

    const openFromCard = (card) => {
        const sectionIndex = Number(card.dataset.sectionIndex);
        if (Number.isNaN(sectionIndex) || !galleryData[sectionIndex]) return;

        state.sectionIndex = sectionIndex;
        state.mode = "before";
        openLightbox();
    };

    caseCards.forEach((card) => {
        card.addEventListener("click", (event) => {
            if (event.target.closest(".sample-actions, a, button, form")) return;
            openFromCard(card);
        });

        card.addEventListener("keydown", (event) => {
            if (event.key !== "Enter" && event.key !== " ") return;
            event.preventDefault();
            openFromCard(card);
        });
    });

    modeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            state.mode = button.dataset.lightboxMode || "before";
            renderSlides();
            syncModeButtons();
        });
    });

    closers.forEach((node) => node.addEventListener("click", closeLightbox));

    lightbox.addEventListener("click", (event) => {
        if (event.target === lightbox || event.target.classList.contains("lightbox-backdrop")) {
            closeLightbox();
        }
    });

    const panel = lightbox.querySelector(".lightbox-panel");
    if (panel) {
        panel.addEventListener("click", (event) => {
            event.stopPropagation();
        });
    }

    previewClosers.forEach((node) => {
        node.addEventListener("click", (event) => {
            event.stopPropagation();
            closePreview();
        });
    });

    if (previewBackdrop) {
        previewBackdrop.addEventListener("click", (event) => {
            event.stopPropagation();
            closePreview();
        });
    }

    if (previewDialog) {
        previewDialog.addEventListener("click", (event) => {
            event.stopPropagation();
        });
    }

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;

        if (previewLightbox && !previewLightbox.hidden) {
            closePreview();
            return;
        }

        if (!lightbox.hidden) closeLightbox();
    });
})();
