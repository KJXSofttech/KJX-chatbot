let currentTag = "start_conversation";
let userData = {};
let typingTimeout;
let isSpeakerOn = true;
let recognition;
let utterance;

function addMessage(message, className, callback = null) {
    const chatBox = document.getElementById('chat-box');
    const messageContainer = document.createElement('div');
    messageContainer.className = 'chat-message-container ' + (className === 'user-message' ? 'user-message-container' : 'bot-message-container');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ' + className;
    
    const emojiSpan = document.createElement('span');
    emojiSpan.className = 'emoji';
    
    if (className === 'user-message') {
        emojiSpan.innerText = '👤';
        messageContainer.appendChild(messageDiv);
        messageContainer.appendChild(emojiSpan);
    } else if (className === 'bot-message') {
        emojiSpan.innerText = '🤖';
        messageContainer.appendChild(emojiSpan);
        messageContainer.appendChild(messageDiv);
    }
    
    chatBox.appendChild(messageContainer);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Typing effect
    let index = 0;
    function typeNextChar() {
        if (index < message.length) {
            messageDiv.innerHTML += message[index];
            index++;
            chatBox.scrollTop = chatBox.scrollHeight;
            typingTimeout = setTimeout(typeNextChar, 10);
        } else if (callback) {
            callback();
        }
    }
    typeNextChar();
}

function addOption(optionText, optionValue) {
    const chatBox = document.getElementById('chat-box');
    const optionButton = document.createElement('button');
    optionButton.className = 'option-button';
    optionButton.innerText = optionText;
    optionButton.onclick = () => handleOptionClick(optionValue, optionText);
    chatBox.appendChild(optionButton);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleOptionClick(optionValue, optionText) {
    // Remove all option buttons
    const optionButtons = document.querySelectorAll('.option-button');
    optionButtons.forEach(button => button.remove());

    // Add the selected option as a user message
    addMessage(optionText, 'user-message');

    if (optionValue === "close_chat") {
        toggleChatbox(); // Close the chatbot
    } else {
        // Process other user inputs
        processUserInput(optionValue, false);
    }
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput) {
        addMessage(userInput, 'user-message');
        document.getElementById('user-input').value = '';
        processUserInput(userInput, true);
    }
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function processUserInput(userInput, isManual) {
    const payload = {
        message: userInput,
        current_tag: currentTag,
        user_data: userData,
        is_manual: isManual
    };

    console.log("Sending payload:", payload);

    fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Received data:", data);
        if (data.error) {
            addMessage(data.error, 'bot-message');
        } else {
            userData = data.user_data || {};
            console.log("Updated userData:", userData);
            displayMessages(data.response, 0, data.options, data.tag);
        }
    })
    .catch(error => {
        console.error("Error processing user input:", error);
        addMessage(`An error occurred: ${error.message}`, 'bot-message');
    });
}

function displayMessages(messages, index, options, newTag) {
    if (index < messages.length) {
        if (isSpeakerOn) {
            utterance = new SpeechSynthesisUtterance(messages[index]);
            window.speechSynthesis.speak(utterance);
        }
        addMessage(messages[index], 'bot-message', () => displayMessages(messages, index + 1, options, newTag));
    } else {
        currentTag = newTag;

        // Clear existing options before adding new ones
        const existingOptions = document.querySelectorAll('.option-button');
        existingOptions.forEach(button => button.remove());

        if (options && options.length > 0) {
            options.forEach(option => {
                addOption(option.text, option.value);
            });
            // Hide the input field when options are available
            document.getElementById('user-input').style.display = 'none';
            document.querySelector('.send-button').style.display = 'none';
        } else {
            // If there are no options, show the input field
            document.getElementById('user-input').style.display = 'inline-block';
            document.querySelector('.send-button').style.display = 'flex';
        }

        // Show/hide microphone button based on the current tag
        const micButton = document.getElementById('mic-button');
        const micTags = ['collect_name', 'collect_email', 'collect_phone', 'collect_problem_statement'];
        if (micTags.includes(newTag)) {
            micButton.style.display = 'inline-block';
        } else {
            micButton.style.display = 'none';
            stopListening();
        }

        // Handle "Close Chat" option and automatic close
        if (newTag === "end_conversation") {
            setTimeout(toggleChatbox, 5000); // Close the chatbot after 5 seconds
        }
    }
}

function toggleChatbox() {
    const phoneContainer = document.getElementById('phone-container');
    const chatIcon = document.getElementById('chat-icon');
    if (phoneContainer.style.display === "none") {
        phoneContainer.style.display = "flex";
        chatIcon.style.display = "none";
        if (currentTag === "start_conversation") {
            startConversation();
        }
    } else {
        phoneContainer.style.display = "none";
        chatIcon.style.display = "block";
        resetChat(); // Reset the chat when closing
    }
}

function startConversation() {
    fetch("/start_conversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: "", current_tag: "start_conversation", user_data: {} })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Start conversation data:", data);
        if (data.error) {
            addMessage(data.error, 'bot-message');
        } else {
            userData = data.user_data || {};
            console.log("Initial userData:", userData);
            displayMessages(data.response, 0, data.options, data.tag);
        }
    })
    .catch(error => {
        console.error("Error starting conversation:", error);
        addMessage(`An error occurred: ${error.message}`, 'bot-message');
    });
}

function resetChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
    currentTag = "start_conversation";
    userData = {};
    clearTimeout(typingTimeout); // Clear any existing typing timeout
    stopListening();  // Ensure the microphone is stopped when resetting the chat
}

function toggleMicrophone() {
    if (!recognition) {
        startListening();
    } else {
        stopListening();
    }
}

function startListening() {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = function() {
        console.log('Speech recognition started');
        document.getElementById('mic-button').classList.add('active');
        document.getElementById('mic-button').classList.remove('inactive');
    };

    recognition.onresult = function(event) {
        const userInput = event.results[0][0].transcript;
        console.log('Recognized speech:', userInput);
        addMessage(userInput, 'user-message');
        processUserInput(userInput, true);
    };

    recognition.onend = function() {
        console.log('Speech recognition ended');
        document.getElementById('mic-button').classList.remove('active');
        document.getElementById('mic-button').classList.add('inactive');
        recognition = null;
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        stopListening();
    };

    recognition.start();
}

function stopListening() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}

function toggleSpeaker() {
    isSpeakerOn = !isSpeakerOn;
    const speakerButton = document.getElementById('speaker-button');
    speakerButton.classList.toggle('active', isSpeakerOn);
    speakerButton.classList.toggle('inactive', !isSpeakerOn);
    if (!isSpeakerOn && utterance) {
        window.speechSynthesis.cancel(); // Stop any ongoing speech
    }
}

// Automatically open chatbot after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(toggleChatbox, 5000); // Open the chatbot after 5 seconds
});