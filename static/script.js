// Hospital AI Chatbot Frontend Script

const API_BASE_URL = '/api';

// Session management - generate or retrieve session ID
let sessionId = localStorage.getItem('chatbot_session_id');
if (!sessionId) {
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('chatbot_session_id', sessionId);
}

// Get DOM elements (will be initialized on load)
let chatMessages, userInput, sendButton;

// Send message function
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    if (!userInput) return;
    
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';
    autoResizeTextarea(); // Reset textarea height
    
    // Disable input while waiting for response
    setInputEnabled(false);
    
    // Show loading indicator
    const loadingId = addLoadingMessage();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        removeLoadingMessage(loadingId);
        
        // Update session ID if provided
        if (data.session_id) {
            sessionId = data.session_id;
            localStorage.setItem('chatbot_session_id', sessionId);
        }
        
        // Add bot response
        if (data.success) {
            addMessage(data.reply, 'bot');
        } else {
            addMessage('I apologize, but I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        // Remove loading indicator
        removeLoadingMessage(loadingId);
        
        // Show error message
        addMessage('I apologize, but I couldn\'t connect to the server. Please make sure the backend is running.', 'bot');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        setInputEnabled(true);
        const userInput = document.getElementById('userInput');
        if (userInput) {
            userInput.focus();
            autoResizeTextarea();
        }
    }
}

// Add message to chat
function addMessage(text, type) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) {
        console.error('chatMessages element not found');
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    // Add avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = type === 'user' ? '👤' : '🤖';
    messageDiv.appendChild(avatarDiv);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format text with line breaks
    const formattedText = formatMessage(text);
    contentDiv.innerHTML = formattedText;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

// Format message text
function formatMessage(text) {
    // Replace newlines with <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Format bold text (**text**)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Format URLs
    formatted = formatted.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank">$1</a>'
    );
    
    return formatted;
}

// Add loading message
function addLoadingMessage() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) {
        console.error('chatMessages element not found');
        return 'loading-message';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loading-message';
    
    // Add avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = '🤖';
    messageDiv.appendChild(avatarDiv);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="loading"><span></span><span></span><span></span></div>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
    
    return 'loading-message';
}

// Remove loading message
function removeLoadingMessage(id) {
    const loadingMessage = document.getElementById(id);
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Auto-resize textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('userInput');
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    } else {
        // Auto-resize on input
        setTimeout(autoResizeTextarea, 0);
    }
}

// Set input enabled/disabled
function setInputEnabled(enabled) {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    if (userInput) userInput.disabled = !enabled;
    if (sendButton) sendButton.disabled = !enabled;
}

// Send quick message from action buttons
function sendQuickMessage(message) {
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.value = message;
        sendMessage();
    }
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (!data.rag_loaded) {
            addMessage('⚠️ Warning: RAG engine not loaded. Please run data ingestion first.', 'bot');
        }
    } catch (error) {
        console.warn('Could not check API health:', error);
    }
}

// Initialize on page load
window.addEventListener('load', () => {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    if (userInput) {
        userInput.focus();
        // Add input event listener for auto-resize
        userInput.addEventListener('input', autoResizeTextarea);
        
        // Add Enter key handler
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    checkAPIHealth();
});

