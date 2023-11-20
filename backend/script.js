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

async function getResponse(userInput) {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userInput }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        addChat(data.answer, "bot");
    } catch (error) {
        console.error('Error fetching the response: ', error);
    }
}
