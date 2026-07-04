(() => {
    const sectionsContainer = document.getElementById("gallery-sections");
    const addSectionButton = document.getElementById("add-gallery-section");
    if (!sectionsContainer) return;

    const setRowNames = (row, sectionIdx, kind, imageIdx) => {
        row.querySelector('[data-field="title_en"]').name = `s${sectionIdx}_${kind}${imageIdx}_title_en`;
        row.querySelector('[data-field="title_tr"]').name = `s${sectionIdx}_${kind}${imageIdx}_title_tr`;
        row.querySelector('[data-field="image"]').name = `s${sectionIdx}_${kind}${imageIdx}_image`;
    };

    const reindexForm = (form) => {
        form.querySelectorAll(".section-block").forEach((section, sectionIdx) => {
            const number = section.querySelector(".section-number");
            if (number) number.textContent = String(sectionIdx + 1);

            section.querySelectorAll(".before-rows .media-row").forEach((row, imageIdx) => {
                setRowNames(row, sectionIdx, "b", imageIdx);
            });
            section.querySelectorAll(".after-rows .media-row").forEach((row, imageIdx) => {
                setRowNames(row, sectionIdx, "a", imageIdx);
            });
        });
    };

    const cloneMediaRow = (rowsContainer) => {
        const firstRow = rowsContainer.querySelector(".media-row");
        if (!firstRow) return null;
        const clone = firstRow.cloneNode(true);
        clone.querySelectorAll("input").forEach((input) => {
            input.value = "";
            input.removeAttribute("name");
        });
        return clone;
    };

    const bindSection = (section) => {
        const beforeRows = section.querySelector(".before-rows");
        const afterRows = section.querySelector(".after-rows");

        section.querySelector(".add-before-row")?.addEventListener("click", () => {
            const row = cloneMediaRow(beforeRows);
            if (row) beforeRows.appendChild(row);
        });

        section.querySelector(".add-after-row")?.addEventListener("click", () => {
            const row = cloneMediaRow(afterRows);
            if (row) afterRows.appendChild(row);
        });

        section.addEventListener("click", (event) => {
            const target = event.target;
            if (!(target instanceof HTMLElement)) return;
            if (!target.classList.contains("remove-media-row")) return;

            const row = target.closest(".media-row");
            const rowsContainer = row?.parentElement;
            if (!row || !rowsContainer) return;
            if (rowsContainer.querySelectorAll(".media-row").length <= 1) return;
            row.remove();
        });
    };

    sectionsContainer.querySelectorAll(".section-block").forEach(bindSection);

    addSectionButton?.addEventListener("click", () => {
        const firstSection = sectionsContainer.querySelector(".section-block");
        if (!firstSection) return;
        const clone = firstSection.cloneNode(true);
        clone.querySelectorAll("input").forEach((input) => {
            input.value = "";
            input.removeAttribute("name");
        });
        sectionsContainer.appendChild(clone);
        bindSection(clone);
    });

    document.querySelectorAll(".gallery-upload-form").forEach((form) => {
        form.addEventListener("submit", () => reindexForm(form));
    });

    document.querySelectorAll(".gallery-upload-form").forEach((form) => reindexForm(form));
})();
