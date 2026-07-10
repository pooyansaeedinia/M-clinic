(function () {
    'use strict';

    const config = window.PORTAL_CONFIG || {};

    function getCsrfToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input && input.value) return input.value;
        const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function fillUrl(template, value) {
        return String(template)
            .replace('{id}', String(value))
            .replace('{code}', String(value));
    }

    function staticUrl(path) {
        if (!path) return '';
        const base = config.staticUrl || '/static/';
        return base.replace(/\/?$/, '/') + String(path).replace(/^\//, '');
    }

    async function api(url, options = {}) {
        const headers = Object.assign(
            {
                Accept: 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            options.headers || {}
        );
        const isFormData = options.body instanceof FormData;
        if (options.body && typeof options.body === 'object' && !isFormData) {
            headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(options.body);
        }
        if (isFormData) {
            delete headers['Content-Type'];
        }
        const response = await fetch(url, Object.assign({}, options, { headers }));
        let data = null;
        try {
            data = await response.json();
        } catch (err) {
            data = null;
        }
        if (!response.ok || (data && data.ok === false)) {
            const error = new Error((data && data.error) || 'Request failed.');
            error.status = response.status;
            error.errors = (data && data.errors) || null;
            throw error;
        }
        return data;
    }

    const toastRoot = document.getElementById('portal-toast-root');

    function toast(message, type = 'success') {
        if (!toastRoot) return;
        const el = document.createElement('div');
        el.className = `portal-toast portal-toast--${type}`;
        el.textContent = message;
        toastRoot.appendChild(el);
        requestAnimationFrame(() => el.classList.add('is-visible'));
        setTimeout(() => {
            el.classList.remove('is-visible');
            setTimeout(() => el.remove(), 280);
        }, 3200);
    }

    async function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
            return;
        }
        const area = document.createElement('textarea');
        area.value = text;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.left = '-9999px';
        document.body.appendChild(area);
        area.select();
        const ok = document.execCommand('copy');
        area.remove();
        if (!ok) throw new Error('Copy failed');
    }

    function openModal(modal) {
        modal.hidden = false;
        document.body.classList.add('portal-modal-open');
        const focusable = modal.querySelector('input, textarea, select, button:not([data-modal-dismiss])');
        if (focusable) focusable.focus();
    }

    function closeModal(modal) {
        modal.hidden = true;
        if (!document.querySelector('.portal-modal:not([hidden])')) {
            document.body.classList.remove('portal-modal-open');
        }
    }

    function bindModalDismiss(modal) {
        modal.querySelectorAll('[data-modal-dismiss]').forEach((btn) => {
            btn.addEventListener('click', () => closeModal(modal));
        });
    }

    const formModal = document.getElementById('portal-form-modal');
    const confirmModal = document.getElementById('portal-confirm-modal');
    if (formModal) bindModalDismiss(formModal);
    if (confirmModal) bindModalDismiss(confirmModal);

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape') return;
        document.querySelectorAll('.portal-modal:not([hidden])').forEach(closeModal);
    });

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    function escapeAttr(str) {
        return escapeHtml(str).replace(/"/g, '&quot;');
    }

    function fieldHtml(field) {
        const id = `portal-field-${field.name}`;
        const value = field.value == null ? '' : String(field.value);

        if (field.type === 'file') {
            const preview = field.previewUrl
                ? `<div class="portal-image-preview"><img src="${escapeAttr(field.previewUrl)}" alt="Current image"></div>`
                : '';
            const clear = field.allowClear
                ? `<label class="portal-check"><input type="checkbox" name="clear_image" value="1"> Remove current image</label>`
                : '';
            return `
                <div class="portal-field">
                    <span>${field.label}</span>
                    ${preview}
                    <input id="${id}" name="${field.name}" type="file" accept="${field.accept || 'image/*'}">
                    <small class="portal-field-hint">${field.hint || 'PNG, JPG, or JPEG'}</small>
                    ${clear}
                </div>
            `;
        }

        if (field.type === 'select') {
            const options = (field.options || [])
                .map((opt) => {
                    const selected = String(opt.value) === value ? ' selected' : '';
                    return `<option value="${escapeAttr(opt.value)}"${selected}>${escapeHtml(opt.label)}</option>`;
                })
                .join('');
            return `
                <label class="portal-field" for="${id}">
                    <span>${field.label}</span>
                    <select id="${id}" name="${field.name}" ${field.required ? 'required' : ''}>
                        ${options}
                    </select>
                </label>
            `;
        }

        if (field.type === 'textarea') {
            return `
                <label class="portal-field" for="${id}">
                    <span>${field.label}</span>
                    <textarea id="${id}" name="${field.name}" rows="${field.rows || 6}" ${field.required ? 'required' : ''} placeholder="${field.placeholder || ''}">${escapeHtml(value)}</textarea>
                </label>
            `;
        }

        return `
            <label class="portal-field" for="${id}">
                <span>${field.label}</span>
                <input id="${id}" name="${field.name}" type="${field.type || 'text'}" value="${escapeAttr(value)}" ${field.required ? 'required' : ''} placeholder="${field.placeholder || ''}" ${field.autocomplete === false ? 'autocomplete="off"' : ''}>
            </label>
        `;
    }

    function openFormModal({ title, submitLabel, fields, onSubmit, useFormData = false }) {
        if (!formModal) return;
        const titleEl = document.getElementById('portal-form-modal-title');
        const fieldsEl = document.getElementById('portal-form-modal-fields');
        const errorEl = document.getElementById('portal-form-modal-error');
        const submitBtn = document.getElementById('portal-form-modal-submit');
        const form = document.getElementById('portal-form-modal-form');

        titleEl.textContent = title;
        submitBtn.textContent = submitLabel || 'Save';
        errorEl.hidden = true;
        errorEl.textContent = '';
        fieldsEl.innerHTML = fields.map(fieldHtml).join('');
        openModal(formModal);

        form.onsubmit = async (event) => {
            event.preventDefault();
            errorEl.hidden = true;
            const formData = new FormData(form);
            let payload;
            if (useFormData) {
                payload = formData;
                if (!formData.get('clear_image')) {
                    formData.delete('clear_image');
                }
                const fileInput = form.querySelector('input[type="file"][name="image"]');
                if (fileInput && (!fileInput.files || !fileInput.files.length)) {
                    formData.delete('image');
                }
            } else {
                payload = {};
                fields.forEach((field) => {
                    if (field.type === 'file') return;
                    payload[field.name] = (formData.get(field.name) || '').toString();
                });
            }
            submitBtn.disabled = true;
            try {
                await onSubmit(payload);
                closeModal(formModal);
            } catch (err) {
                if (err.errors) {
                    errorEl.textContent = Object.values(err.errors).flat().join(' ');
                } else {
                    errorEl.textContent = err.message || 'Something went wrong.';
                }
                errorEl.hidden = false;
            } finally {
                submitBtn.disabled = false;
            }
        };
    }

    function openConfirmModal({ title, message, confirmLabel, onConfirm }) {
        if (!confirmModal) return;
        document.getElementById('portal-confirm-modal-title').textContent = title || 'Confirm';
        document.getElementById('portal-confirm-modal-message').textContent = message;
        const confirmBtn = document.getElementById('portal-confirm-modal-confirm');
        confirmBtn.textContent = confirmLabel || 'Delete';
        openModal(confirmModal);

        confirmBtn.onclick = async () => {
            confirmBtn.disabled = true;
            try {
                await onConfirm();
                closeModal(confirmModal);
            } catch (err) {
                toast(err.message || 'Delete failed.', 'error');
            } finally {
                confirmBtn.disabled = false;
            }
        };
    }

    /* ---------- Languages dashboard ---------- */
    function languageCardHtml(language) {
        const pageUrl = fillUrl(config.urls.languagePage, language.code);
        const image = language.image_url
            ? `<img src="${escapeAttr(language.image_url)}" alt="${escapeAttr(language.name)}">`
            : `<div class="portal-flag-placeholder">${escapeHtml((language.name || '?').charAt(0))}</div>`;
        return `
            <article class="portal-lang-card portal-lang-card--flag" data-language-id="${language.id}" data-language-code="${escapeAttr(language.code)}">
                <a href="${pageUrl}" class="portal-lang-card-link">
                    <div class="portal-country-flag">${image}</div>
                    <div class="portal-country-meta">
                        <h2>${escapeHtml(language.name)}</h2>
                        <p>${Number(language.section_count || 0)} section${Number(language.section_count || 0) === 1 ? '' : 's'}</p>
                    </div>
                </a>
                <div class="portal-card-actions">
                    <button type="button" class="portal-btn portal-btn-secondary portal-btn-sm" data-action="edit-language" data-id="${language.id}">Edit</button>
                    <button type="button" class="portal-btn portal-btn-danger portal-btn-sm" data-action="delete-language" data-id="${language.id}" data-name="${escapeAttr(language.name)}">Delete</button>
                </div>
            </article>
        `;
    }

    function ensureLanguageGrid() {
        const grid = document.querySelector('[data-language-grid]');
        if (!grid) return null;
        const empty = grid.querySelector('[data-languages-empty]');
        if (empty) empty.remove();
        return grid;
    }

    function showLanguagesEmpty() {
        const grid = document.querySelector('[data-language-grid]');
        if (!grid) return;
        grid.innerHTML = `
            <div class="portal-empty" data-languages-empty>
                <div class="portal-empty-icon" aria-hidden="true">◇</div>
                <h3>No languages yet</h3>
                <p>Create a language to start organizing chat templates.</p>
                <button type="button" class="portal-btn portal-btn-primary" data-action="create-language">Add Language</button>
            </div>
        `;
    }

    async function refreshLanguageGrid() {
        const data = await api(config.urls.languages);
        const grid = document.querySelector('[data-language-grid]');
        if (!grid) return;
        if (!data.languages.length) {
            showLanguagesEmpty();
            return;
        }
        grid.innerHTML = data.languages.map(languageCardHtml).join('');
    }

    function languageFormFields(language) {
        return [
            {
                name: 'name',
                label: 'Display name',
                required: true,
                value: language ? language.name : '',
                placeholder: 'e.g. English',
            },
            {
                name: 'language_name',
                label: 'Language label',
                value: language ? language.language_name : '',
                placeholder: 'Optional',
            },
            {
                name: 'code',
                label: 'Code / slug',
                required: true,
                value: language ? language.code : '',
                placeholder: 'e.g. english',
                autocomplete: false,
            },
            {
                name: 'image',
                label: 'Card image',
                type: 'file',
                accept: config.languageImageAccept || '.jpg,.jpeg,.png,image/jpeg,image/png',
                previewUrl: language && language.image_url ? language.image_url : '',
                allowClear: Boolean(language && language.has_image),
                hint: 'PNG, JPG, or JPEG. Replaces the current image when selected.',
            },
            {
                name: 'sort_order',
                label: 'Sort order',
                type: 'number',
                value: language ? language.sort_order : 0,
            },
        ];
    }

    function openLanguageForm(language) {
        const isEdit = Boolean(language);
        openFormModal({
            title: isEdit ? 'Edit Language' : 'Add Language',
            submitLabel: isEdit ? 'Save Changes' : 'Create Language',
            useFormData: true,
            fields: languageFormFields(language),
            onSubmit: async (formData) => {
                if (isEdit) {
                    await api(fillUrl(config.urls.languageDetail, language.id), {
                        method: 'POST',
                        body: formData,
                    });
                    await refreshLanguageGrid();
                    toast('Language updated.');
                } else {
                    await api(config.urls.languages, {
                        method: 'POST',
                        body: formData,
                    });
                    await refreshLanguageGrid();
                    toast('Language created.');
                }
            },
        });
    }

    async function loadLanguage(id) {
        const data = await api(fillUrl(config.urls.languageDetail, id));
        return data.language;
    }

    function initDashboard() {
        const root = document.querySelector('[data-portal-languages]');
        if (!root) return;

        root.addEventListener('click', async (event) => {
            const btn = event.target.closest('[data-action]');
            if (!btn) return;
            const action = btn.getAttribute('data-action');

            if (action === 'create-language') {
                openLanguageForm(null);
                return;
            }

            if (action === 'edit-language') {
                try {
                    const language = await loadLanguage(btn.getAttribute('data-id'));
                    openLanguageForm(language);
                } catch (err) {
                    toast(err.message || 'Could not load language.', 'error');
                }
                return;
            }

            if (action === 'delete-language') {
                const id = btn.getAttribute('data-id');
                const name = btn.getAttribute('data-name') || 'this language';
                openConfirmModal({
                    title: 'Delete Language',
                    message: `Delete “${name}” and all of its sections? This cannot be undone.`,
                    onConfirm: async () => {
                        await api(fillUrl(config.urls.languageDetail, id), { method: 'DELETE' });
                        await refreshLanguageGrid();
                        toast('Language deleted.');
                    },
                });
            }
        });
    }

    /* ---------- Sections page ---------- */
    function sectionCardHtml(section) {
        const search = (section.title || '').toLowerCase();
        return `
            <article class="portal-section-card" data-section-id="${section.id}" data-search="${escapeAttr(search)}">
                <div class="portal-section-card-body">
                    <h3>${escapeHtml(section.title)}</h3>
                    <p class="portal-section-preview">${escapeHtml(section.body)}</p>
                </div>
                <div class="portal-card-actions">
                    <button type="button" class="portal-btn portal-btn-secondary portal-btn-sm" data-action="copy-section" data-body="${escapeAttr(section.body)}">Copy</button>
                    <button type="button" class="portal-btn portal-btn-secondary portal-btn-sm" data-action="edit-section" data-id="${section.id}">Edit</button>
                    <button type="button" class="portal-btn portal-btn-danger portal-btn-sm" data-action="delete-section" data-id="${section.id}" data-name="${escapeAttr(section.title)}">Delete</button>
                </div>
            </article>
        `;
    }

    function ensureSectionList() {
        const list = document.querySelector('[data-section-list]');
        if (!list) return null;
        const empty = list.querySelector('[data-sections-empty]');
        if (empty) empty.remove();
        return list;
    }

    function showSectionsEmpty() {
        const list = document.querySelector('[data-section-list]');
        if (!list) return;
        list.innerHTML = `
            <div class="portal-empty" data-sections-empty>
                <div class="portal-empty-icon" aria-hidden="true">◇</div>
                <h3>No sections yet</h3>
                <p>Add your first template section for this language.</p>
                <button type="button" class="portal-btn portal-btn-primary" data-action="create-section">Add Section</button>
            </div>
        `;
    }

    function applySectionSearch() {
        const input = document.querySelector('[data-section-search]');
        const list = document.querySelector('[data-section-list]');
        const filteredEmpty = document.querySelector('[data-sections-filtered]');
        if (!input || !list) return;

        const query = input.value.trim().toLowerCase();
        const cards = [...list.querySelectorAll('[data-section-id]')];
        let visible = 0;
        cards.forEach((card) => {
            const haystack = (card.getAttribute('data-search') || '').toLowerCase();
            const match = !query || haystack.includes(query);
            card.hidden = !match;
            if (match) visible += 1;
        });

        if (filteredEmpty) {
            filteredEmpty.hidden = !(cards.length > 0 && query && visible === 0);
        }
    }

    function openSectionForm(section) {
        const isEdit = Boolean(section);
        openFormModal({
            title: isEdit ? 'Edit Section' : 'Add Section',
            submitLabel: isEdit ? 'Save Changes' : 'Create Section',
            fields: [
                {
                    name: 'title',
                    label: 'Title',
                    required: true,
                    value: section ? section.title : '',
                    placeholder: 'e.g. First Message',
                },
                {
                    name: 'body',
                    label: 'Message',
                    type: 'textarea',
                    required: true,
                    rows: 8,
                    value: section ? section.body : '',
                    placeholder: 'Hello, I am…',
                },
                {
                    name: 'sort_order',
                    label: 'Sort order',
                    type: 'number',
                    value: section ? section.sort_order : 0,
                },
            ],
            onSubmit: async (payload) => {
                payload.sort_order = Number(payload.sort_order || 0);
                if (isEdit) {
                    const data = await api(fillUrl(config.urls.sectionDetail, section.id), {
                        method: 'PATCH',
                        body: payload,
                    });
                    const card = document.querySelector(`[data-section-id="${section.id}"]`);
                    if (card) card.outerHTML = sectionCardHtml(data.section);
                    applySectionSearch();
                    toast('Section updated.');
                } else {
                    const data = await api(config.urls.sections, {
                        method: 'POST',
                        body: payload,
                    });
                    const list = ensureSectionList();
                    if (list) list.insertAdjacentHTML('beforeend', sectionCardHtml(data.section));
                    applySectionSearch();
                    toast('Section created.');
                }
            },
        });
    }

    async function loadSection(id) {
        const data = await api(fillUrl(config.urls.sectionDetail, id));
        return data.section;
    }

    function initLanguagePage() {
        const root = document.querySelector('[data-portal-sections]');
        if (!root) return;

        const search = document.querySelector('[data-section-search]');
        if (search) search.addEventListener('input', applySectionSearch);

        root.addEventListener('click', async (event) => {
            const btn = event.target.closest('[data-action]');
            if (!btn) return;
            const action = btn.getAttribute('data-action');

            if (action === 'create-section') {
                openSectionForm(null);
                return;
            }

            if (action === 'copy-section') {
                const text = btn.getAttribute('data-body') || '';
                copyText(text)
                    .then(() => toast('Message copied.'))
                    .catch(() => toast('Could not copy message.', 'error'));
                return;
            }

            if (action === 'edit-section') {
                try {
                    const section = await loadSection(btn.getAttribute('data-id'));
                    openSectionForm(section);
                } catch (err) {
                    toast(err.message || 'Could not load section.', 'error');
                }
                return;
            }

            if (action === 'delete-section') {
                const id = btn.getAttribute('data-id');
                const name = btn.getAttribute('data-name') || 'this section';
                openConfirmModal({
                    title: 'Delete Section',
                    message: `Delete “${name}”? This cannot be undone.`,
                    onConfirm: async () => {
                        await api(fillUrl(config.urls.sectionDetail, id), { method: 'DELETE' });
                        const card = document.querySelector(`[data-section-id="${id}"]`);
                        if (card) card.remove();
                        const list = document.querySelector('[data-section-list]');
                        if (list && !list.querySelector('[data-section-id]')) {
                            showSectionsEmpty();
                        }
                        applySectionSearch();
                        toast('Section deleted.');
                    },
                });
            }
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        if (config.page === 'dashboard') initDashboard();
        if (config.page === 'language') initLanguagePage();
    });
})();
