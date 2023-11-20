document.getElementById('send-btn').addEventListener('click', function() {
    const inputField = document.getElementById('chat-input');
    const userText = inputField.value.trim();

    if (userText) {
        addChat(userText, "user");
        inputField.value = ''; // Clear the input field
        getResponse(userText); // Function to handle the response
    }
});

function addChat(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const newMessage = document.createElement('div');
    newMessage.textContent = text;
    newMessage.className = sender;
    chatBox.appendChild(newMessage);
}

function getResponse(userInput) {
    // Placeholder for sending request to your server or OpenAI's API
    // For now, we'll just echo the user input
    setTimeout(() => { addChat("Echo: " + userInput, "bot"); }, 1000);
}
