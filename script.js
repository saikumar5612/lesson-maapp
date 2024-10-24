// script.js

let selectedCard = null;

// Function to select a card
function selectCard(card) {
    selectedCard = card;
    document.getElementById('card-display').innerText = `You selected: ${card}`;
}

// Function to ask a yes/no question
function askQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!selectedCard) {
        alert("Please select a card first!");
        return;
    }

    if (!question) {
        alert("Please ask a question!");
        return;
    }

    // Generate a random response
    const responses = ["Yes", "No", "Ask again later"];
    const response = responses[Math.floor(Math.random() * responses.length)];

    // Log the question and response
    const questionLog = document.getElementById('question-log');
    const listItem = document.createElement('li');
    listItem.textContent = `Q: ${question} - A: ${response}`;
    questionLog.appendChild(listItem);

    // Clear the input field
    questionInput.value = '';
}
