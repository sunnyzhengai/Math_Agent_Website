// ============================================================================
// Stem Normalization (defensive against Unicode, spacing variations)
// ============================================================================

const normStem = s =>
  (s ?? "")
    .normalize("NFKC")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();

// ============================================================================
// Module-level state
// ============================================================================

// DEV: toggle to test cycle mode (server-side no-repeat guarantee)
const USE_CYCLE = true;  // set to true to enable cycle mode
const SESSION_ID = localStorage.getItem("sid") || 
                   (localStorage.setItem("sid", `session-${Date.now()}`), localStorage.getItem("sid"));

let currentItem = null;     // latest generated item
let attempted = 0;          // session tally
let correct = 0;
let isBusy = false;         // blocks concurrent requests
const API_BASE = "";        // same origin; leave empty

// Track seen question stems to avoid repeats within a pool
const seenByPool = new Map(); // key: `${skill}:${difficulty}` -> Set of stems
const MAX_REPEAT_TRIES = 10;  // retry limit before resetting bag

// Pool size hints: dynamically loaded from /skills/manifest, with defaults as fallback
let POOL_SIZE_HINT = {
    "quad.graph.vertex:easy": 2,
    "quad.graph.vertex:medium": 1,
    "quad.graph.vertex:hard": 1,
    "quad.graph.vertex:applied": 1,
    "quad.standard.vertex:easy": 3,
    "quad.standard.vertex:medium": 2,
    "quad.standard.vertex:hard": 1,
    "quad.standard.vertex:applied": 2,
    "quad.roots.factored:easy": 2,
    "quad.roots.factored:medium": 2,
    "quad.roots.factored:hard": 1,
    "quad.roots.factored:applied": 1,
    "quad.solve.by_factoring:easy": 2,
    "quad.solve.by_factoring:medium": 2,
    "quad.solve.by_factoring:hard": 1,
    "quad.solve.by_factoring:applied": 1,
    "quad.solve.by_formula:easy": 2,
    "quad.solve.by_formula:medium": 2,
    "quad.solve.by_formula:hard": 1,
    "quad.solve.by_formula:applied": 1,
};

// DEV: cycle difficulties so you can see all 6 without repeats
const DEV_SEQUENCE = ["easy", "medium", "hard", "applied"];
let devIndex = 0;

// Skill rotation: cycle through all 5 skills
const SKILL_SEQUENCE = [
    "quad.graph.vertex",
    "quad.standard.vertex",
    "quad.roots.factored",
    "quad.solve.by_factoring",
    "quad.solve.by_formula",
];
let skillIndex = 0;

// Optional: debug logs
const DEBUG = true;
function dbg(...args) { if (DEBUG) console.debug("[UI]", ...args); }

// ============================================================================
// DOM References
// ============================================================================

const elements = {
    stem: null,
    choices: {},  // { A, B, C, D }
    feedback: null,
    nextBtn: null,
    tally: null,
    choiceButtons: {},  // { A, B, C, D }
};

// ============================================================================
// Initialize
// ============================================================================

// --- Load pool sizes from server manifest ---

async function loadPoolSizes() {
    try {
        const response = await fetch(`${API_BASE}/skills/manifest`);
        if (!response.ok) {
            dbg("Failed to load pool sizes from manifest, using defaults");
            return;
        }
        const manifest = await response.json();
        // manifest format: { "quad.graph.vertex": { "easy": 2, "medium": 1, ... }, ... }
        // Convert to our POOL_SIZE_HINT format: { "quad.graph.vertex:easy": 2, ... }
        const updated = {};
        for (const [skillId, difficulties] of Object.entries(manifest)) {
            for (const [diff, count] of Object.entries(difficulties)) {
                updated[`${skillId}:${diff}`] = count;
            }
        }
        POOL_SIZE_HINT = updated;
        dbg("Loaded pool sizes from manifest:", POOL_SIZE_HINT);
    } catch (error) {
        dbg("Error loading pool sizes from manifest:", error);
    }
}

// --- Pool completion helpers ---

function isPoolComplete(skillId, diff) {
    const k = `${skillId}:${diff}`;
    const poolSize = POOL_SIZE_HINT[k] ?? null;
    const seen = seenByPool.get(k) ?? new Set();
    return poolSize ? seen.size >= poolSize : false;
}

function isEntireSetComplete() {
    // all skills × difficulties complete
    for (const s of SKILL_SEQUENCE) {
        for (const d of DEV_SEQUENCE) {
            if (!isPoolComplete(s, d)) return false;
        }
    }
    return true;
}

function clearLocalBag(skillId, difficulty) {
    const k = `${skillId}:${difficulty}`;
    seenByPool.set(k, new Set());
}

// --- Planner Hint & Progress Card helpers ---

async function refreshPlannerHint(skillId) {
    try {
        const body = { skill_id: skillId };
        if (SESSION_ID) body.session_id = SESSION_ID;

        const res = await fetch(`${API_BASE}/planner/next`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        if (!res.ok) throw new Error("planner failed");
        const data = await res.json();

        const hint = document.getElementById("planner-hint");
        const pill = document.getElementById("planner-diff");
        const txt = document.getElementById("planner-reason");

        pill.textContent = data.difficulty[0].toUpperCase() + data.difficulty.slice(1);
        txt.textContent = data.reason;
        hint.hidden = false;
    } catch {
        // Hide hint quietly if planner not available
        const hint = document.getElementById("planner-hint");
        if (hint) hint.hidden = true;
    }
}

async function refreshProgress() {
    try {
        if (!SESSION_ID) return;
        const res = await fetch(`${API_BASE}/progress/get`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID }),
        });
        if (!res.ok) throw new Error("progress failed");
        const data = await res.json();

        const card = document.getElementById("progress-card");
        const list = document.getElementById("progress-list");
        list.innerHTML = "";

        // Show only your skills, stable order
        for (const skillId of SKILL_SEQUENCE) {
            const s = data.skills[skillId];
            if (!s) continue;
            const li = document.createElement("li");
            const label = skillId.replace("quad.", "").replace(/\./g, " → ").replace(/_/g, " ");
            const pct = `${Math.round((s.p ?? 0) * 100)}%`;
            li.innerHTML = `<span>${label}</span><span class="progress-pill">${pct}</span>`;
            list.appendChild(li);
        }

        card.hidden = list.children.length === 0;
    } catch {
        const card = document.getElementById("progress-card");
        if (card) card.hidden = true;
    }
}

// Call after state changes to keep both in sync
async function refreshGuidanceAndProgress() {
    const skillId = SKILL_SEQUENCE[skillIndex];
    await Promise.allSettled([
        refreshPlannerHint(skillId),
        refreshProgress()
    ]);
}

// --- Populate and enable dropdowns on load ---

async function initSelectors() {
    const skillSel = document.getElementById("skill-select");
    const diffSel = document.getElementById("difficulty-select");

    // Skills
    SKILL_SEQUENCE.forEach((id, i) => {
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = id
            .replace("quad.", "")
            .replace(/\./g, " → ")
            .replace(/_/g, " ");
        skillSel.appendChild(opt);
    });
    skillSel.value = SKILL_SEQUENCE[skillIndex];

    // Difficulties
    DEV_SEQUENCE.forEach((d) => {
        const opt = document.createElement("option");
        opt.value = d;
        opt.textContent = d[0].toUpperCase() + d.slice(1);
        diffSel.appendChild(opt);
    });
    diffSel.value = DEV_SEQUENCE[devIndex];

    // Enable + wire events
    skillSel.disabled = false;
    diffSel.disabled = false;

    skillSel.addEventListener("change", () => {
        skillIndex = Math.max(0, SKILL_SEQUENCE.indexOf(skillSel.value));
        clearLocalBag(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
        updateProgress();
        fetchGenerateNoRepeat(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
    });

    diffSel.addEventListener("change", () => {
        devIndex = Math.max(0, DEV_SEQUENCE.indexOf(diffSel.value));
        clearLocalBag(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
        updateProgress();
        fetchGenerateNoRepeat(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
    });
}

// --- Update progress indicator ---

function updateProgress() {
    const skillId = SKILL_SEQUENCE[skillIndex];
    const diff = DEV_SEQUENCE[devIndex];
    const poolKey = `${skillId}:${diff}`;
    const poolSize = POOL_SIZE_HINT[poolKey] ?? "?";
    const seen = seenByPool.get(poolKey) ?? new Set();
    const displaySkill = skillId
        .replace("quad.", "")
        .replace(/\./g, " → ")
        .replace(/_/g, " ");
    
    const progressEl = document.getElementById("progress");
    if (progressEl) {
        progressEl.textContent = `Seen ${seen.size}/${poolSize} · ${diff} · ${displaySkill}`;
    }
}

// --- Finish modal ---

function showFinishModal() {
    const modal = document.getElementById("finish-modal");
    const summary = document.getElementById("modal-summary");
    
    const totalQuestions = Array.from(POOL_SIZE_HINT.values()).reduce((a, b) => a + b, 0);
    summary.innerHTML = `
        <strong>Accuracy:</strong> ${correct} correct out of ${attempted} attempted (${attempted > 0 ? Math.round(correct / attempted * 100) : 0}%)<br>
        <strong>Total questions:</strong> ${totalQuestions} across ${SKILL_SEQUENCE.length} skills and ${DEV_SEQUENCE.length} difficulties
    `;
    
    modal.hidden = false;
    elements.nextBtn.disabled = true;
    setButtonsEnabled(false);

    document.getElementById("btn-restart").onclick = () => {
        // Clear all local bags to replay everything
        seenByPool.clear();
        modal.hidden = true;
        attempted = 0;
        correct = 0;
        elements.tally.textContent = `Correct ${correct} of ${attempted}`;
        skillIndex = 0;
        devIndex = 0;
        document.getElementById("skill-select").value = SKILL_SEQUENCE[0];
        document.getElementById("difficulty-select").value = DEV_SEQUENCE[0];
        updateProgress();
        fetchGenerateNoRepeat(SKILL_SEQUENCE[0], DEV_SEQUENCE[0]);
    };

    document.getElementById("btn-next-skill").onclick = () => {
        // Jump to next skill (if any) at easy; if already last skill, just restart
        skillIndex = Math.min(skillIndex + 1, SKILL_SEQUENCE.length - 1);
        devIndex = 0;
        modal.hidden = true;
        document.getElementById("skill-select").value = SKILL_SEQUENCE[skillIndex];
        document.getElementById("difficulty-select").value = DEV_SEQUENCE[devIndex];
        clearLocalBag(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
        updateProgress();
        fetchGenerateNoRepeat(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
    };
}

function maybeFinish() {
    if (isEntireSetComplete()) {
        showFinishModal();
        return true;
    }
    return false;
}

document.addEventListener("DOMContentLoaded", async () => {
    initializeElements();
    attachEventHandlers();
    await loadPoolSizes();  // Load server-truth pool sizes before initializing dropdowns
    await initSelectors();
    updateProgress();
    // start at current devIndex difficulty with first skill
    fetchGenerateNoRepeat(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
});

function initializeElements() {
    elements.stem = document.getElementById("stem");
    elements.feedback = document.getElementById("feedback");
    elements.nextBtn = document.getElementById("next-btn");
    elements.tally = document.getElementById("tally");

    for (const choiceId of ["A", "B", "C", "D"]) {
        elements.choiceButtons[choiceId] = document.getElementById(`choice-${choiceId}`);
    }
}

function attachEventHandlers() {
    for (const choiceId of ["A", "B", "C", "D"]) {
        elements.choiceButtons[choiceId].addEventListener("click", () => onChoiceClick(choiceId));
    }
    elements.nextBtn.addEventListener("click", onNext);
}

// ============================================================================
// fetchGenerateNoRepeat() — Load a new question, avoiding stems we've seen
// ============================================================================

async function fetchGenerateNoRepeat(skillId = "quad.graph.vertex", difficulty = "easy") {
    // Guard: don't fetch if we're done with the entire set
    if (isEntireSetComplete()) {
        dbg("Set already complete, showing finish modal");
        showFinishModal();
        return;
    }

    if (isBusy) return;

    setButtonsEnabled(false);
    elements.nextBtn.disabled = true;
    setFeedback("", null);
    document.body.classList.add("busy");
    isBusy = true;

    const poolKey = `${skillId}:${difficulty}`;
    if (!seenByPool.has(poolKey)) {
        seenByPool.set(poolKey, new Set());
    }
    const seenStems = seenByPool.get(poolKey);
    const poolSize = POOL_SIZE_HINT[poolKey] ?? null;

    dbg("pool", poolKey, "seen", seenStems.size, "of", poolSize);

    let item = null;

    // Try to fetch an unseen question
    for (let attempt = 0; attempt < MAX_REPEAT_TRIES; attempt++) {
        try {
            // Build request body
            const requestBody = {
                skill_id: skillId,
                difficulty: difficulty,
            };
            
            // Add cycle mode parameters if enabled
            if (USE_CYCLE) {
                requestBody.mode = "cycle";
                requestBody.session_id = SESSION_ID;
            }
            
            const response = await fetch(`${API_BASE}/items/generate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                // If we're actually done, show finish instead of an error
                if (isEntireSetComplete()) {
                    document.body.classList.remove("busy");
                    isBusy = false;
                    showFinishModal();
                    return;
                }
                
                const errorData = await response.json().catch(() => ({}));
                setFeedback(errorData.message || "Error loading question", null);
                elements.nextBtn.disabled = false;
                document.body.classList.remove("busy");
                isBusy = false;
                return;
            }

            item = await response.json();
            const stem = normStem(item?.stem ?? "");

            dbg("fetch attempt", attempt, "stem", stem);

            // Warn if pool size hint is too small
            if (poolSize && seenStems.size > poolSize) {
                dbg("⚠️ POOL_SIZE_HINT too small for", poolKey, "— seen", seenStems.size, ">", poolSize);
            }

            // Check if we've seen this stem before
            if (!seenStems.has(stem)) {
                seenStems.add(stem);
                updateProgress();  // Update progress indicator immediately
                renderQuestion(item);
                document.body.classList.remove("busy");
                isBusy = false;
                return; // Success: got a new one
            }
            // Otherwise: loop and try again
        } catch (error) {
            // If we're actually done, show finish instead of an error
            if (isEntireSetComplete()) {
                document.body.classList.remove("busy");
                isBusy = false;
                showFinishModal();
                return;
            }
            
            setFeedback("Couldn't reach server. Please try again.", null);
            elements.nextBtn.disabled = false;
            document.body.classList.remove("busy");
            isBusy = false;
            return;
        }
    }

    // After too many retries, reset the bag and try once more with fresh pool
    if (poolSize) {
        seenStems.clear();
        document.body.classList.remove("busy");
        isBusy = false;
        return fetchGenerateNoRepeat(skillId, difficulty); // try once more with fresh bag
    }

    // Fallback if pool size unknown
    if (item) {
        renderQuestion(item);
    } else {
        setFeedback("Error: Could not fetch question after multiple attempts.", null);
        elements.nextBtn.disabled = false;
    }

    document.body.classList.remove("busy");
    isBusy = false;
}

// ============================================================================
// onChoiceClick(choiceId) — Grade the student's answer
// ============================================================================

async function onChoiceClick(choiceId) {
    if (isBusy || !currentItem) return;

    setButtonsEnabled(false);
    document.body.classList.add("busy");
    isBusy = true;

    try {
        const response = await fetch(`${API_BASE}/grade`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                item: currentItem,
                choice_id: choiceId,
            }),
        });

        if (response.ok) {
            const result = await response.json();
            handleGradeResult(result);
        } else {
            const errorData = await response.json();
            setFeedback(errorData.message || "Error grading response", null);
            elements.nextBtn.disabled = false;
        }
    } catch (error) {
        setFeedback("Couldn't reach server. Please try again.", null);
        elements.nextBtn.disabled = false;
    } finally {
        document.body.classList.remove("busy");
        isBusy = false;
    }
}

function handleGradeResult(result) {
    attempted += 1;
    if (result.correct) {
        correct += 1;
    }

    // Add visual feedback to buttons
    // Mark the button the user chose
    const chosenBtn = elements.choiceButtons[result.choice_id];
    if (chosenBtn) {
        if (result.correct) {
            chosenBtn.classList.add("is-correct");
        } else {
            chosenBtn.classList.add("is-incorrect");
        }
    }

    // If they got it wrong, show the correct answer too
    if (!result.correct && result.solution_choice_id) {
        const correctBtn = elements.choiceButtons[result.solution_choice_id];
        if (correctBtn) {
            correctBtn.classList.add("is-correct");
        }
    }

    // Render feedback
    const feedbackClass = result.correct ? "correct" : "incorrect";
    setFeedback(result.explanation, feedbackClass);

    // Update tally
    elements.tally.textContent = `Correct ${correct} of ${attempted}`;

    // If the whole set is done, show the finish modal immediately
    if (isEntireSetComplete()) {
        elements.nextBtn.disabled = true;
        setButtonsEnabled(false);
        showFinishModal();
        return;
    }

    // Otherwise allow the user to continue
    elements.nextBtn.disabled = false;

    // NEW: mastery changed → refresh progress (planner can also change if session-aware)
    refreshGuidanceAndProgress();
}

// ============================================================================
// onNext() — Advance to next difficulty when current pool exhausted
// ============================================================================

function onNext() {
    // Check if entire set is complete before advancing
    if (maybeFinish()) return;

    const skillId = SKILL_SEQUENCE[skillIndex];
    
    const currDiff = DEV_SEQUENCE[devIndex];
    const poolKey = `${skillId}:${currDiff}`;
    const poolSize = POOL_SIZE_HINT[poolKey] ?? null;
    const seen = seenByPool.get(poolKey) ?? new Set();

    dbg("NEXT pressed; skillIndex", skillIndex, "diff", currDiff);
    dbg("pool", poolKey, "seen", seen.size, "of", poolSize);

    // If we've seen all unique stems for this pool, advance difficulty
    if (poolSize && seen.size >= poolSize) {
        // Only reset client-side bag if NOT using server cycle mode
        // (server cycle mode manages the bag server-side)
        if (!USE_CYCLE) {
            seenByPool.set(poolKey, new Set());
        }

        // Advance or wrap
        if (devIndex < DEV_SEQUENCE.length - 1) {
            devIndex += 1;
        } else {
            devIndex = 0; // wrap to easy
            // Also advance skill when difficulty wraps
            if (skillIndex < SKILL_SEQUENCE.length - 1) {
                skillIndex += 1;
            } else {
                skillIndex = 0; // wrap to first skill
            }
        }
        dbg("ADVANCE difficulty to", DEV_SEQUENCE[devIndex], "skill to", SKILL_SEQUENCE[skillIndex]);
    }

    // Update selector values to match current state
    document.getElementById("skill-select").value = SKILL_SEQUENCE[skillIndex];
    document.getElementById("difficulty-select").value = DEV_SEQUENCE[devIndex];
    updateProgress();

    elements.nextBtn.disabled = true;
    fetchGenerateNoRepeat(SKILL_SEQUENCE[skillIndex], DEV_SEQUENCE[devIndex]);
}

// ============================================================================
// Utility Functions
// ============================================================================

function renderQuestion(item) {
    currentItem = item;

    // Set stem
    elements.stem.textContent = item.stem;

    // Set choice texts and enable buttons
    for (let i = 0; i < item.choices.length; i++) {
        const choiceId = String.fromCharCode(65 + i); // A, B, C, D
        const button = elements.choiceButtons[choiceId];
        const textSpan = button.querySelector(".choice-text");
        textSpan.textContent = item.choices[i].text;
        // Clear state classes from previous question
        button.classList.remove("is-correct", "is-incorrect");
    }

    // Enable choice buttons, disable Next
    setButtonsEnabled(true);
    elements.nextBtn.disabled = true;

    // Clear feedback
    setFeedback("", null);

    // NEW: show planner hint + mastery snapshot
    refreshGuidanceAndProgress();
}

function setButtonsEnabled(enabled) {
    for (const choiceId of ["A", "B", "C", "D"]) {
        elements.choiceButtons[choiceId].disabled = !enabled;
    }
}

function setFeedback(text, cls) {
    elements.feedback.textContent = text;
    elements.feedback.className = "feedback";
    if (cls) {
        elements.feedback.classList.add(cls);
    }
}
