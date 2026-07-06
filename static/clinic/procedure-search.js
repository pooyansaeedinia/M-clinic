(() => {
    const searchInput = document.getElementById("procedure-search");
    const grid = document.getElementById("procedure-grid");
    const emptyMessage = document.getElementById("procedure-search-empty");
    if (!searchInput || !grid) return;

    const cards = Array.from(grid.querySelectorAll("[data-procedure-name]"));

    const filterCards = () => {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        cards.forEach((card) => {
            const name = (card.dataset.procedureName || "").toLowerCase();
            const matches = !query || name.includes(query);
            card.hidden = !matches;
            if (matches) visibleCount += 1;
        });

        if (emptyMessage) {
            emptyMessage.hidden = visibleCount > 0 || cards.length === 0;
        }
    };

    searchInput.addEventListener("input", filterCards);
})();
