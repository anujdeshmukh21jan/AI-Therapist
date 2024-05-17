
function startChat() {
    window.location.href = "chat.html";
}

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatWindow = document.getElementById("chat-window");
    
    // Append user message to chat window
    var userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = "You: " + userInput;
    chatWindow.appendChild(userMessage);

    // Clear user input field
    document.getElementById("user-input").value = "";

    // Simulate AI response (replace with actual AI response logic)
    var aiResponse = document.createElement("div");
    aiResponse.className = "message ai";
    aiResponse.textContent = "AI Therapist: Thank you for sharing.";
    chatWindow.appendChild(aiResponse);
}
