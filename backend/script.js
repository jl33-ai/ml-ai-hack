document.getElementById('send-btn').addEventListener('click', async () => {
    const inputField = document.getElementById('chat-input');
    const userText = inputField.value.trim();
  
    if (userText) {
      // Add user's text to the chat window
      addChatMessage(userText, 'user');
      inputField.value = '';
  
      // Send the user's text to your server
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userInput: userText }),
      });
      addChatMessage('I should be responding soon...', 'bot');
      const data = await response.json();
      addChatMessage(data.message, 'bot'); // Add the bot's response to the chat window
      // addChatMessage('echo', 'bot') // Test
    }
  });
  

function addChatMessage(text, sender) {
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


