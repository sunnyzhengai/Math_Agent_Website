// ============================================================================
// Module-level state
// ============================================================================

let currentItem = null;     // latest generated item
let attempted = 0;          // session tally
let correct = 0;
let isBusy = false;         // blocks concurrent requests
const API_BASE = "";        // same origin; leave empty

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
    fetchGenerate();
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
// fetchGenerate() — Load a new question
// ============================================================================

async function fetchGenerate() {
    if (isBusy) return;

    setButtonsEnabled(false);
    elements.nextBtn.disabled = true;
    setFeedback("", null);
    document.body.classList.add("busy");
    isBusy = true;

    try {
        const response = await fetch(`${API_BASE}/items/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                skill_id: "quad.graph.vertex",
                difficulty: "easy",
                // seed omitted for randomness
            }),
        });

        if (response.ok) {
            currentItem = await response.json();
            renderQuestion(currentItem);
        } else {
            const errorData = await response.json();
            setFeedback(errorData.message || "Error loading question", null);
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
    fetchGenerate();
}

// ============================================================================
// Utility Functions
// ============================================================================

function renderQuestion(item) {
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
