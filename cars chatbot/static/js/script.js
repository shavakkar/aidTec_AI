const chatHistory = document.getElementById('chat-history');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');

messageForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const message = messageInput.value;
  if (message.trim() !== '') {
    addMessageToChat('User', message, 'user-message');
    sendMessageToBot(message);
    messageInput.value = '';
  }
});

function addMessageToChat(sender, message, className) {
  const chatMessage = document.createElement('div');
  chatMessage.classList.add('chat-message');
  chatMessage.classList.add(className);

  const messageBubble = document.createElement('div');
  messageBubble.classList.add('message-bubble');
  messageBubble.textContent = message;

  const messageSender = document.createElement('div');
  messageSender.classList.add('message-sender');
  messageSender.textContent = sender;

  chatMessage.appendChild(messageBubble);
  chatMessage.appendChild(messageSender);
  chatHistory.appendChild(chatMessage);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function sendMessageToBot(message) {
  fetch('/get_response', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `message=${encodeURIComponent(message)}`,
  })
    .then((response) => response.text())
    .then((data) => {
      addMessageToChat('Bot', data, 'bot-message');
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


// {
//     "tag": "positive",
//     "patterns": ["Good", "Well Done", "Apprectiations", "Thanks for the help", "Your Good!", "Great", "you made me happy","Satisfactory"],
//     "responses": ["Thanks...", "I'm always here to help you out", "Happy to make your day!", "No one is as good as like me :)"]
// }