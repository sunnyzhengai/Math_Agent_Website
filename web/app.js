// ============================================================================
// Module-level state
// ============================================================================

let currentItem = null;     // latest generated item
let attempted = 0;          // session tally
let correct = 0;
let isBusy = false;         // blocks concurrent requests
const API_BASE = "";        // same origin; leave empty

// Track seen question stems to avoid repeats within a pool
const seenByPool = new Map(); // key: `${skill}:${difficulty}` -> Set of stems
const MAX_REPEAT_TRIES = 10;  // retry limit before resetting bag

// Pool size hints: when bag reaches this size, it's exhausted
const POOL_SIZE_HINT = {
    "quad.graph.vertex:easy": 2,
    "quad.graph.vertex:medium": 1,
    "quad.graph.vertex:hard": 1,
    "quad.graph.vertex:applied": 1,
};

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

document.addEventListener("DOMContentLoaded", () => {
    initializeElements();
    attachEventHandlers();
    fetchGenerateNoRepeat();
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

    // ✅ Reset bag when we've exhausted this pool
    if (poolSize && seenStems.size >= poolSize) {
        seenStems.clear();
    }

    let item = null;

    // Try to fetch an unseen question
    for (let attempt = 0; attempt < MAX_REPEAT_TRIES; attempt++) {
        try {
            const response = await fetch(`${API_BASE}/items/generate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    skill_id: skillId,
                    difficulty: difficulty,
                    // seed omitted for randomness
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                setFeedback(errorData.message || "Error loading question", null);
                elements.nextBtn.disabled = false;
                document.body.classList.remove("busy");
                isBusy = false;
                return;
            }

            item = await response.json();
            const stem = item?.stem ?? "";

            // Check if we've seen this stem before
            if (!seenStems.has(stem)) {
                seenStems.add(stem);
                renderQuestion(item);
                document.body.classList.remove("busy");
                isBusy = false;
                return; // Success: got a new one
            }
            // Otherwise: loop and try again
        } catch (error) {
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

    // Render feedback
    const feedbackClass = result.correct ? "correct" : "incorrect";
    setFeedback(result.explanation, feedbackClass);

    // Update tally
    elements.tally.textContent = `Correct ${correct} of ${attempted}`;

    // Enable Next button
    elements.nextBtn.disabled = false;
}

// ============================================================================
// onNext() — Reset and fetch next question
// ============================================================================

function onNext() {
    elements.nextBtn.disabled = true;
    fetchGenerateNoRepeat();
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
    }

    // Enable choice buttons, disable Next
    setButtonsEnabled(true);
    elements.nextBtn.disabled = true;

    // Clear feedback
    setFeedback("", null);
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
