async function sendMessage() {
    const userInputElement = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const userInputValue = userInputElement.value.trim();

    if (userInputValue === '') return;

    // Cambiar el botón a estado de carga
    toggleLoadingButton(true);

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.textContent = userInputValue;
    userMessage.classList.add('user-message');
    chatBox.appendChild(userMessage);

    // Clear the input field and maintain focus
    userInputElement.value = '';
    userInputElement.focus();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInputValue }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.text();
        const botMessage = document.createElement('div');
        botMessage.innerHTML = data;
        botMessage.classList.add('bot-message');
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    } finally {
        // Restaurar el botón a su estado original
        toggleLoadingButton(false);
    }
}

function toggleLoadingButton(isLoading) {
    const sendButton = document.getElementById('send-button');
    if (isLoading) {
        sendButton.classList.add('loading');
        sendButton.disabled = true;
    } else {
        sendButton.classList.remove('loading');
        sendButton.disabled = false;
    }
}

function toggleChat() {
    const chatContainer = document.getElementById('chat-container');
    const toggleButton = document.getElementById('toggle-chat');
    chatContainer.classList.toggle('minimized');

    if (chatContainer.classList.contains('minimized')) {
        toggleButton.textContent = '+';
    } else {
        toggleButton.textContent = '−';
    }
}