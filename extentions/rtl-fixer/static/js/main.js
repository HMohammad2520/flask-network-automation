(function () {
    let formulaTokens = [];
    let fieldValues = {};
    let validationErrors = {};
    let bidiFixEnabled = true;

    const chipsWrapper = document.getElementById("chipsWrapper");
    const fieldsListDiv = document.getElementById("fieldsList");
    const finalResultTextSpan = document.getElementById("finalResultText");
    const clearBtn = document.getElementById("clearBtn");
    const copyBtn = document.getElementById("copyResultBtn");
    const shareLinkBtn = document.getElementById("shareLinkBtn");
    const bidiFixToggle = document.getElementById("bidiFixToggle");

    function saveStateToLocal() {
        localStorage.setItem(
            "formulaBuilderState",
            JSON.stringify({
                tokens: formulaTokens,
                fieldValues,
                bidiFixEnabled,
            }),
        );
    }

    function loadStateFromLocal() {
        const saved = localStorage.getItem("formulaBuilderState");
        if (!saved) return false;
        try {
            const state = JSON.parse(saved);
            formulaTokens = state.tokens || [];
            fieldValues = state.fieldValues || {};
            bidiFixEnabled =
                state.bidiFixEnabled !== undefined ? state.bidiFixEnabled : true;
            bidiFixToggle.checked = bidiFixEnabled;
            rebuildAllFromTokens();
            return true;
        } catch (e) {
            return false;
        }
    }

    function encodeStateToHash() {
        return btoa(
            unescape(
                encodeURIComponent(
                    JSON.stringify({
                        t: formulaTokens,
                        v: fieldValues,
                        b: bidiFixEnabled,
                    }),
                ),
            ),
        );
    }

    function decodeStateFromHash(hash) {
        if (!hash || hash === "#") return false;
        try {
            const state = JSON.parse(
                decodeURIComponent(escape(atob(hash.substring(1)))),
            );
            formulaTokens = state.t || [];
            fieldValues = state.v || {};
            bidiFixEnabled = state.b !== undefined ? state.b : true;
            bidiFixToggle.checked = bidiFixEnabled;
            rebuildAllFromTokens();
            history.replaceState(null, "", window.location.pathname);
            showToast("لینک با موفقیت بارگذاری شد", "#2e7d32");
            return true;
        } catch (e) {
            return false;
        }
    }

    function shareCurrentState() {
        const url =
            window.location.href.split("#")[0] + "#" + encodeStateToHash();
        navigator.clipboard
            .writeText(url)
            .then(() => showToast("✅ لینک اشتراک کپی شد", "#2c7da0"))
            .catch(() => showToast("❌ خطا", "#c23b22"));
    }

    function loadInitialState() {
        if (
            window.location.hash &&
            window.location.hash.length > 1 &&
            decodeStateFromHash(window.location.hash)
        )
            return;
        loadStateFromLocal();
        if (formulaTokens.length === 0) rebuildAllFromTokens();
    }

    function validateFieldByType(value, type) {
        const trimmed = value.trim();
        if (trimmed === "") return "فیلد نمی‌تواند خالی باشد";
        if (type === "FA") {
            const persianPattern =
                /^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s\u200c\u200d\u0660-\u0669\u06F0-\u06F9\u064B-\u0652\u061F\u060C\u061B]+$/;
            if (!persianPattern.test(trimmed))
                return "❌ فقط حروف فارسی، اعداد فارسی و فاصله مجاز";
            if (
                !/[\u0600-\u06FF]/.test(trimmed) &&
                !/[\u06F0-\u06F9\u0660-\u0669]/.test(trimmed)
            )
                return "❌ باید شامل حرف یا عدد فارسی باشد";
            return null;
        } else if (type === "ENG") {
            const engPattern = /^[A-Za-z0-9\s\/\.\,\-\'\"\&\+\_\\\:\(\)\[\]]+$/;
            if (!engPattern.test(trimmed))
                return "❌ فقط حروف انگلیسی، اعداد و علائم استاندارد مجاز است";
            if (/[\u0600-\u06FF]/.test(trimmed))
                return "❌ حروف فارسی در فیلد انگلیسی مجاز نیست";
            return null;
        } else if (type === "INT") {
            if (trimmed.length === 0) return "مقدار INT نمی‌تواند خالی باشد";
            return null;
        }
        return null;
    }

    function getCurrentPlaceholdersFromTokens() {
        const placeholders = [];
        for (let i = 0; i < formulaTokens.length; i++) {
            const tok = formulaTokens[i];
            if (tok === "FA" || tok === "ENG" || tok === "INT") {
                placeholders.push({
                    index: i,
                    type: tok,
                    uniqueId: `ph_${i}_${tok}`,
                });
            }
        }
        return placeholders;
    }

    function insertTokenAtIndex(index, token) {
        // Save placeholders before insertion
        const placeholdersBefore = getCurrentPlaceholdersFromTokens();

        // Insert the token
        formulaTokens.splice(index, 0, token);

        // Build new field values mapping
        const newPlaceholders = getCurrentPlaceholdersFromTokens();
        const newFieldValues = {};

        for (let i = 0; i < newPlaceholders.length; i++) {
            const newPh = newPlaceholders[i];
            // Determine original index before insertion
            let originalIndex;
            if (newPh.index < index) {
                originalIndex = newPh.index;
            } else if (newPh.index === index) {
                // This is the new placeholder (if the inserted token is a field type)
                // It has no previous value, so keep empty
                originalIndex = -1; // signal to not find old
            } else {
                // newPh.index > index: was shifted right by 1, so original index = newPh.index - 1
                originalIndex = newPh.index - 1;
            }

            if (originalIndex !== -1) {
                const oldPh = placeholdersBefore.find(
                    (p) => p.index === originalIndex && p.type === newPh.type,
                );
                if (oldPh && fieldValues[oldPh.uniqueId] !== undefined) {
                    newFieldValues[newPh.uniqueId] = fieldValues[oldPh.uniqueId];
                } else {
                    newFieldValues[newPh.uniqueId] = "";
                }
            } else {
                newFieldValues[newPh.uniqueId] = ""; // new field starts empty
            }
        }
        fieldValues = newFieldValues;
        rebuildAllFromTokens();
    }

    function removeTokenAtIndex(indexToRemove) {
        if (indexToRemove < 0 || indexToRemove >= formulaTokens.length)
            return;

        // Save a snapshot of the placeholders before removal
        const placeholdersBefore = getCurrentPlaceholdersFromTokens();

        // Perform the removal
        formulaTokens.splice(indexToRemove, 1);

        // Build new field values by mapping each new placeholder
        // to the correct original placeholder (taking index shift into account)
        const newPlaceholders = getCurrentPlaceholdersFromTokens();
        const newFieldValues = {};

        for (let i = 0; i < newPlaceholders.length; i++) {
            const newPh = newPlaceholders[i];
            // Original index before removal:
            // - If newPh.index < indexToRemove, original index = newPh.index
            // - Else original index = newPh.index + 1
            const originalIndex =
                newPh.index < indexToRemove ? newPh.index : newPh.index + 1;

            // Find the old placeholder that had that original index and the same type
            const oldPh = placeholdersBefore.find(
                (p) => p.index === originalIndex && p.type === newPh.type,
            );

            // If a matching old placeholder existed and had a value, keep it; otherwise start empty
            if (oldPh && fieldValues[oldPh.uniqueId] !== undefined) {
                newFieldValues[newPh.uniqueId] = fieldValues[oldPh.uniqueId];
            } else {
                newFieldValues[newPh.uniqueId] = "";
            }
        }

        fieldValues = newFieldValues;
        rebuildAllFromTokens();
    }

    function renderChips() {
        chipsWrapper.innerHTML = "";
        if (formulaTokens.length === 0) {
            chipsWrapper.innerHTML =
                '<div class="empty-chips">[ خالی - با دکمه‌ها شروع کنید ]</div>';
            return;
        }
        for (let i = 0; i < formulaTokens.length; i++) {
            const token = formulaTokens[i];
            let chipClass = "token-symbol";
            let displayText = token;
            if (token === "FA") {
                chipClass = "token-fa";
                displayText = "فا";
            } else if (token === "ENG") {
                chipClass = "token-eng";
                displayText = "انگ";
            } else if (token === "INT") {
                chipClass = "token-int";
                displayText = "عدد";
            } else if (token === "(") displayText = "(";
            else if (token === ")") displayText = ")";
            else if (token === " ") {
                chipClass = "token-space";
                displayText = "␣";
            }

            const chipDiv = document.createElement("div");
            chipDiv.className = `formula-chip ${chipClass}`;
            const textSpan = document.createElement("span");
            textSpan.textContent = displayText;
            const delBtn = document.createElement("button");
            delBtn.textContent = "✖";
            delBtn.className = "delete-chip";
            delBtn.title = "حذف";
            delBtn.onclick = (e) => {
                e.stopPropagation();
                removeTokenAtIndex(i);
            };
            chipDiv.appendChild(textSpan);
            chipDiv.appendChild(delBtn);
            chipsWrapper.appendChild(chipDiv);

            if (i < formulaTokens.length - 1) {
                const plusBtn = document.createElement("button");
                plusBtn.textContent = "+";
                plusBtn.className = "plus-chip";
                plusBtn.title = "درج المان جدید در این نقطه";
                plusBtn.onclick = (e) => {
                    e.stopPropagation();
                    showInsertionDialog(i + 1);
                };
                chipsWrapper.appendChild(plusBtn);
            }
        }
    }

    function showInsertionDialog(index) {
        const tokens = ["FA", "ENG", "INT", "(", ")", " "];
        const persianNames = {
            FA: "فا",
            ENG: "انگ",
            INT: "عدد",
            "(": "پرانتز باز",
            ")": "پرانتز بسته",
            " ": "فاصله",
        };
        const modal = document.createElement("div");
        modal.className = "modal-overlay";
        modal.innerHTML = `
                <div class="modal-dialog">
                    <h3 class="modal-title">➕ درج المان جدید</h3>
                    <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:1rem;">
                        ${tokens.map((t) => `<button class="action-btn" data-token="${t}" style="padding:0.5rem 0.8rem;min-width:60px;">${persianNames[t]}</button>`).join("")}
                    </div>
                    <button id="closeModalBtn" class="modal-btn modal-btn-secondary" style="width:100%;">لغو</button>
                </div>`;
        document.body.appendChild(modal);
        modal.querySelectorAll("[data-token]").forEach((btn) => {
            btn.onclick = () => {
                insertTokenAtIndex(index, btn.getAttribute("data-token"));
                modal.remove();
            };
        });
        modal.querySelector("#closeModalBtn").onclick = () => modal.remove();
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };
    }

    function rebuildFields() {
        const placeholders = getCurrentPlaceholdersFromTokens();
        if (placeholders.length === 0) {
            fieldsListDiv.innerHTML = `<div style="color: #6c8d9b; padding: 10px;">⚠️ فرمول یافت نشد</div>`;
            return;
        }
        const currentIds = new Set(placeholders.map((p) => p.uniqueId));
        for (let key in fieldValues)
            if (!currentIds.has(key)) delete fieldValues[key];
        for (let key in validationErrors)
            if (!currentIds.has(key)) delete validationErrors[key];
        for (let ph of placeholders) {
            if (fieldValues[ph.uniqueId] === undefined)
                fieldValues[ph.uniqueId] = "";
            if (validationErrors[ph.uniqueId] === undefined)
                validationErrors[ph.uniqueId] = "خالی است";
        }
        let html = "";
        for (let ph of placeholders) {
            const currentVal = fieldValues[ph.uniqueId] || "";
            const errorMsg = validationErrors[ph.uniqueId];
            let badgeClass = "",
                badgeText = "",
                hintText = "";
            if (ph.type === "FA") {
                badgeClass = "field-badge-fa";
                badgeText = "فا";
                hintText = "فقط فارسی/اعداد فارسی";
            } else if (ph.type === "ENG") {
                badgeClass = "field-badge-eng";
                badgeText = "انگ";
                hintText = "فقط لاتین/اعداد انگلیسی";
            } else {
                badgeClass = "field-badge-int";
                badgeText = "عدد";
                hintText = "هر نوع کاراکتر (غیرخالی)";
            }
            const isValid = !errorMsg && currentVal.trim() !== "";
            const validationIcon = isValid
                ? "✅ معتبر"
                : errorMsg && errorMsg !== "خالی است"
                    ? `⚠️ ${errorMsg}`
                    : "✏️ الزامی";
            html += `
                <div class="compact-field-row" data-id="${ph.uniqueId}">
                    <div class="field-badge ${badgeClass}">${badgeText}<span class="position-number">#${ph.index + 1}</span></div>
                    <input type="text" class="field-input-compact" id="${ph.uniqueId}" placeholder="${hintText}" value="${escapeHtml(currentVal)}" data-type="${ph.type}" data-id="${ph.uniqueId}">
                    <div class="validation-icon-wrapper">${validationIcon}</div>
                </div>`;
        }
        fieldsListDiv.innerHTML = html;
        for (let ph of placeholders) {
            const inputElem = document.getElementById(ph.uniqueId);
            if (inputElem) {
                inputElem.addEventListener("input", (e) => {
                    let newVal = e.target.value;
                    fieldValues[ph.uniqueId] = newVal;
                    const error = validateFieldByType(newVal, ph.type);
                    validationErrors[ph.uniqueId] = error;
                    const iconDiv = inputElem.parentElement.querySelector(
                        ".validation-icon-wrapper",
                    );
                    if (iconDiv) {
                        if (!error && newVal !== "") iconDiv.innerHTML = "✅ معتبر";
                        else if (error && error !== "خالی است")
                            iconDiv.innerHTML = `⚠️ ${error}`;
                        else iconDiv.innerHTML = "✏️ الزامی";
                    }
                    updateFinalResult();
                    saveStateToLocal();
                });
            }
        }
    }

    function formatWithPerTokenIsolation(tokensArray) {
        if (tokensArray.length === 0) return "";
        const isolatedTokens = tokensArray.map((token) =>
            token === " " ? token : "\u2067" + token + "\u2069",
        );
        let result = isolatedTokens[0];
        for (let i = 1; i < isolatedTokens.length; i++) {
            const prev = tokensArray[i - 1],
                curr = tokensArray[i];
            const noSpace =
                prev === "(" ||
                prev === ")" ||
                prev === " " ||
                curr === "(" ||
                curr === ")" ||
                curr === " " ||
                prev === "«" ||
                curr === "»";
            result += noSpace ? isolatedTokens[i] : " " + isolatedTokens[i];
        }
        return result;
    }

    function applyBidiFix(text) {
        if (!bidiFixEnabled) return text;
        return (
            "\u2067" +
            text
                .replace(/\(/g, "«")
                .replace(/\)/g, "»")
                .replace(/,/g, "،")
                .replace(/0/g, "۰")
                .replace(/1/g, "۱")
                .replace(/2/g, "۲")
                .replace(/3/g, "۳")
                .replace(/4/g, "۴")
                .replace(/5/g, "۵")
                .replace(/6/g, "۶")
                .replace(/7/g, "۷")
                .replace(/8/g, "۸")
                .replace(/9/g, "۹") +
            "\u2069"
        );
    }

    function updateFinalResult() {
        if (formulaTokens.length === 0) {
            finalResultTextSpan.innerText = "—";
            return;
        }
        const placeholders = getCurrentPlaceholdersFromTokens();
        let resultTokens = [...formulaTokens];
        for (let i = placeholders.length - 1; i >= 0; i--) {
            const ph = placeholders[i];
            resultTokens[ph.index] = fieldValues[ph.uniqueId] || "";
        }
        finalResultTextSpan.innerText =
            applyBidiFix(formatWithPerTokenIsolation(resultTokens)) ||
            "(نتیجه خالی)";
    }

    function rebuildAllFromTokens() {
        renderChips();
        rebuildFields();
        updateFinalResult();
        saveStateToLocal();
    }

    function addToken(token) {
        formulaTokens.push(token);
        rebuildAllFromTokens();
    }

    function clearAll() {
        formulaTokens = [];
        fieldValues = {};
        validationErrors = {};
        rebuildAllFromTokens();
    }

    function copyFinalResult() {
        let text = finalResultTextSpan.innerText.replace(
            /[\u202A-\u202E\u2066-\u2069]/g,
            "",
        );
        if (!text || text === "—")
            showToast("نتیجه‌ای برای کپی وجود ندارد", "#b75f3a");
        else
            navigator.clipboard
                .writeText(text)
                .then(() => showToast("✅ کپی شد!", "#2e7d32"))
                .catch(() => showToast("❌ خطا", "#c23b22"));
    }

    function showToast(msg, bg) {
        const existing = document.querySelector(".copy-toast");
        if (existing) existing.remove();
        const toast = document.createElement("div");
        toast.className = "copy-toast";
        toast.textContent = msg;
        toast.style.background = bg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2000);
    }

    function getFirstSignificantChar(word) {
        for (let ch of word) {
            if (/[A-Za-z]/.test(ch) || /[\u0600-\u06FF]/.test(ch)) return ch;
        }
        return null;
    }

    function classifyToken(word) {
        if (word === "(" || word === ")")
            return { type: "literal", value: word };

        const firstChar = getFirstSignificantChar(word);
        if (firstChar) {
            if (/[A-Za-z]/.test(firstChar)) return { type: "ENG", value: word };
            return { type: "FA", value: word };
        }

        // No letter found: check if the word is number-like (digits + allowed separators)
        const stripped = word.replace(/[\/\-\.\,\:]/g, "");
        if (/^\d+$/.test(stripped)) return { type: "INT", value: word };

        // Otherwise, treat as a literal symbol
        return { type: "literal", value: word };
    }

    function analyzeTextToFormula(input) {
        const rawTokens = input.match(/\S+|\s+/g) || [];
        const tokens = rawTokens.map((t) =>
            /^\s+$/.test(t) ? { isSpace: true } : classifyToken(t),
        );

        // Merge consecutive tokens of the same field type, absorbing spaces inside the group
        const merged = [];
        let idx = 0;
        while (idx < tokens.length) {
            const token = tokens[idx];
            if (token.isSpace) {
                merged.push({ type: "space" });
                idx++;
                continue;
            }
            if (token.type === "literal") {
                merged.push({ type: "literal", value: token.value });
                idx++;
                continue;
            }

            // token is FA, ENG, or INT → start a group
            const currentType = token.type;
            let combinedValue = token.value;
            idx++;
            while (idx < tokens.length) {
                if (tokens[idx].isSpace) {
                    // absorb space only if the next non‑space token has the same type
                    if (
                        idx + 1 < tokens.length &&
                        !tokens[idx + 1].isSpace &&
                        tokens[idx + 1].type === currentType
                    ) {
                        combinedValue += " " + tokens[idx + 1].value;
                        idx += 2; // skip space and the matching token
                    } else {
                        break;
                    }
                } else if (tokens[idx].type === currentType) {
                    // adjacent same type without space (rare)
                    combinedValue += tokens[idx].value;
                    idx++;
                } else {
                    break;
                }
            }
            merged.push({ type: currentType, value: combinedValue });
        }

        // Build final formula tokens and corresponding field values
        const formulaTokens = [];
        const tempFields = [];
        for (const item of merged) {
            if (item.type === "space") {
                formulaTokens.push(" ");
            } else if (item.type === "literal") {
                formulaTokens.push(item.value);
            } else {
                // FA, ENG, INT
                formulaTokens.push(item.type);
                tempFields.push(item.value);
            }
        }
        return { tokens: formulaTokens, tempFields };
    }

    function showTextToFormulaModal() {
        const modal = document.createElement("div");
        modal.className = "modal-overlay";
        modal.innerHTML = `
                <div class="modal-dialog">
                    <h3 class="modal-title">✨ تبدیل متن به فرمول</h3>
                    <div class="modal-sub">متن خود را وارد کنید (پارسی/انگلیسی/عدد/علائم)</div>
                    <textarea id="formulaInputText" class="modal-textarea" rows="4"></textarea>
                    <div class="modal-buttons">
                        <button id="modalCancelBtn" class="modal-btn modal-btn-secondary">لغو</button>
                        <button id="modalConfirmBtn" class="modal-btn modal-btn-primary">تبدیل</button>
                    </div>
                </div>`;
        document.body.appendChild(modal);
        const textarea = modal.querySelector("#formulaInputText");
        const cancel = modal.querySelector("#modalCancelBtn");
        const confirm = modal.querySelector("#modalConfirmBtn");
        const close = () => modal.remove();

        cancel.onclick = close;
        confirm.onclick = () => {
            const raw = textarea.value;
            if (!raw.trim()) {
                showToast("لطفاً متنی وارد کنید", "#b75f3a");
                return;
            }
            const { tokens, tempFields } = analyzeTextToFormula(raw);
            if (tokens.length === 0) {
                showToast("نتیجه‌ای یافت نشد", "#b75f3a");
                close();
                return;
            }

            const replace = () => {
                formulaTokens = tokens;
                rebuildAllFromTokens();
                const placeholders = getCurrentPlaceholdersFromTokens();
                for (
                    let idx = 0;
                    idx < placeholders.length && idx < tempFields.length;
                    idx++
                ) {
                    const ph = placeholders[idx];
                    fieldValues[ph.uniqueId] = tempFields[idx];
                    validationErrors[ph.uniqueId] = null;
                }
                rebuildFields();
                updateFinalResult();
                saveStateToLocal();
                showToast("✅ فرمول و مقادیر با موفقیت ساخته شد", "#2e7d32");
                close();
            };

            if (formulaTokens.length > 0) {
                showConfirmDialog(
                    "فرمول فعلی جایگزین شود؟",
                    "فرمول موجود با فرمول جدید جایگزین خواهد شد. ادامه می‌دهید؟",
                    replace,
                    () => showToast("عملیات لغو شد", "#6c8d9b"),
                );
            } else {
                replace();
            }
        };
        modal.onclick = (e) => {
            if (e.target === modal) close();
        };
        textarea.focus();
    }

    function showConfirmDialog(title, message, onConfirm, onCancel) {
        const modal = document.createElement("div");
        modal.className = "confirm-modal";
        modal.innerHTML = `
                <div class="confirm-dialog">
                    <h4 style="margin:0 0 0.5rem 0;color:#e65100;">⚠️ ${title}</h4>
                    <p style="margin:0 0 1rem 0;font-size:0.9rem;color:#555;">${message}</p>
                    <div class="confirm-buttons">
                        <button id="confirmNoBtn" class="modal-btn modal-btn-secondary">خیر، لغو</button>
                        <button id="confirmYesBtn" class="modal-btn modal-btn-primary" style="background:#e65100;">بله، جایگزین کن</button>
                    </div>
                </div>`;
        document.body.appendChild(modal);
        const no = modal.querySelector("#confirmNoBtn");
        const yes = modal.querySelector("#confirmYesBtn");
        const close = () => modal.remove();
        no.onclick = () => {
            if (onCancel) onCancel();
            close();
        };
        yes.onclick = () => {
            if (onConfirm) onConfirm();
            close();
        };
        modal.onclick = (e) => {
            if (e.target === modal) close();
        };
    }

    function escapeHtml(str) {
        return str.replace(/[&<>]/g, (m) =>
            m === "&" ? "&amp;" : m === "<" ? "&lt;" : "&gt;",
        );
    }

    function initEventListeners() {
        document
            .querySelectorAll(".action-btn[data-token]")
            .forEach((btn) =>
                btn.addEventListener("click", () =>
                    addToken(btn.getAttribute("data-token")),
                ),
            );
        document
            .getElementById("textToFormulaBtn")
            .addEventListener("click", showTextToFormulaModal);
        clearBtn.addEventListener("click", clearAll);
        copyBtn.addEventListener("click", copyFinalResult);
        shareLinkBtn.addEventListener("click", shareCurrentState);
        bidiFixToggle.addEventListener("change", (e) => {
            bidiFixEnabled = e.target.checked;
            updateFinalResult();
            saveStateToLocal();
        });
    }

    window.addEventListener("load", () => {
        initEventListeners();
        loadInitialState();
    });
})();
