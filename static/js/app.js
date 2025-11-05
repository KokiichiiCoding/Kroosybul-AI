/**
 * Kroosybul AI - Frontend Application
 * Handles WebSocket communication and UI interactions
 */

// Global state
let socket = null;
let sessionId = null;
let currentDownloadUrl = null;
let isGenerating = false;

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const statusBar = document.getElementById('status-bar');
const statusText = document.getElementById('status-text');
const progressContainer = document.getElementById('progress-container');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const downloadModal = document.getElementById('download-modal');
const downloadBtn = document.getElementById('download-btn');
const newProjectBtn = document.getElementById('new-project-btn');
const modalClose = document.getElementById('modal-close');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeSocket();
    setupEventListeners();
    loadSupportedLanguages();
});

/**
 * Initialize WebSocket connection
 */
function initializeSocket() {
    socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
        addSystemMessage('Connected to Kroosybul AI', 'success');
    });

    socket.on('connected', (data) => {
        sessionId = data.session_id;
        console.log('Session ID:', sessionId);
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        addSystemMessage('Disconnected from server', 'warning');
    });

    socket.on('message_received', (data) => {
        console.log('Message received:', data);
    });

    socket.on('status', (data) => {
        updateStatus(data.message, data.stage);
    });

    socket.on('progress', (data) => {
        updateProgress(data.message);
    });

    socket.on('ai_response', (data) => {
        addAIMessage(data.message, data.type);

        if (data.type === 'result' || data.type === 'error') {
            hideStatus();
            hideProgress();
            isGenerating = false;
            enableInput();
        }
    });

    socket.on('project_complete', (data) => {
        console.log('Project complete:', data);
        currentDownloadUrl = data.download_url;
        showDownloadModal(data);
    });

    socket.on('error', (data) => {
        console.error('Error:', data);
        addSystemMessage(`Error: ${data.message}`, 'error');
        hideStatus();
        hideProgress();
        isGenerating = false;
        enableInput();
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);

    // Send message on Enter (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Example buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            messageInput.value = btn.dataset.example;
            messageInput.focus();
        });
    });

    // Modal controls
    modalClose.addEventListener('click', () => {
        downloadModal.style.display = 'none';
    });

    downloadBtn.addEventListener('click', () => {
        if (currentDownloadUrl) {
            window.location.href = currentDownloadUrl;
        }
    });

    newProjectBtn.addEventListener('click', () => {
        downloadModal.style.display = 'none';
        messageInput.value = '';
        messageInput.focus();
    });

    // Close modal on outside click
    downloadModal.addEventListener('click', (e) => {
        if (e.target === downloadModal) {
            downloadModal.style.display = 'none';
        }
    });
}

/**
 * Send a message to the server
 */
function sendMessage() {
    const message = messageInput.value.trim();

    if (!message || isGenerating) {
        return;
    }

    // Add user message to chat
    addUserMessage(message);

    // Clear input
    messageInput.value = '';

    // Disable input while generating
    isGenerating = true;
    disableInput();

    // Show status
    showStatus('Analyzing your request...', 'analysis');

    // Send to server
    socket.emit('message', { message });
}

/**
 * Add user message to chat
 */
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add AI message to chat
 */
function addAIMessage(text, type = 'normal') {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';

    // Convert markdown-style formatting
    let formattedText = formatText(text);

    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">${formattedText}</div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add system message to chat
 */
function addSystemMessage(text, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ai-message ${type}`;
    messageDiv.innerHTML = `
        <div class="message-avatar">ℹ️</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Update status bar
 */
function updateStatus(message, stage) {
    statusText.textContent = message;
    showStatus(message, stage);
}

/**
 * Show status bar
 */
function showStatus(message, stage) {
    statusText.textContent = message;
    statusBar.style.display = 'flex';

    // Update icon based on stage
    const statusIcon = statusBar.querySelector('.status-icon');
    const icons = {
        'analysis': '🔍',
        'planning': '📋',
        'generation': '⚙️',
        'testing': '🧪',
        'refinement': '🔧',
        'complete': '✅'
    };
    statusIcon.textContent = icons[stage] || '⚙️';
}

/**
 * Hide status bar
 */
function hideStatus() {
    statusBar.style.display = 'none';
}

/**
 * Update progress
 */
function updateProgress(message) {
    progressText.textContent = message;
    progressContainer.style.display = 'block';

    // Animate progress bar (simulated)
    const currentWidth = parseInt(progressFill.style.width || '0');
    const newWidth = Math.min(currentWidth + 10, 90);
    progressFill.style.width = `${newWidth}%`;
}

/**
 * Hide progress
 */
function hideProgress() {
    setTimeout(() => {
        progressContainer.style.display = 'none';
        progressFill.style.width = '0%';
    }, 500);
}

/**
 * Show download modal
 */
function showDownloadModal(projectData) {
    const modalMessage = document.getElementById('modal-message');
    const projectInfo = document.getElementById('project-info');

    if (projectData.warnings) {
        modalMessage.textContent = 'Project generated with warnings. Review the details below.';
        modalMessage.className = 'warning';
    } else {
        modalMessage.textContent = 'Your project has been generated successfully!';
        modalMessage.className = 'success';
    }

    projectInfo.innerHTML = `
        <p><strong>Project Name:</strong> ${escapeHtml(projectData.project_name)}</p>
        <p><strong>Files Created:</strong> ${projectData.files.length}</p>
        <p><strong>Test Results:</strong> ${projectData.test_results.success ? '✅ Passed' : '⚠️ With warnings'}</p>
        ${projectData.test_results.tested_files ? `<p><strong>Files Tested:</strong> ${projectData.test_results.tested_files}</p>` : ''}
    `;

    downloadModal.style.display = 'flex';
}

/**
 * Disable input
 */
function disableInput() {
    messageInput.disabled = true;
    sendButton.disabled = true;
}

/**
 * Enable input
 */
function enableInput() {
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Format text with markdown-like syntax
 */
function formatText(text) {
    // Escape HTML first
    text = escapeHtml(text);

    // Bold
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Code blocks
    text = text.replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code>$2</code></pre>');

    // Inline code
    text = text.replace(/`(.+?)`/g, '<code>$1</code>');

    // Line breaks
    text = text.replace(/\n/g, '<br>');

    // Lists
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    return text;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Load supported languages from API
 */
function loadSupportedLanguages() {
    fetch('/api/languages')
        .then(response => response.json())
        .then(data => {
            console.log('Supported languages:', data);
            // Update language tags if needed
            if (data.languages) {
                const languageTags = document.getElementById('language-tags');
                languageTags.innerHTML = data.languages.map(lang =>
                    `<span class="tag">${capitalize(lang)}</span>`
                ).join('');
            }
        })
        .catch(error => {
            console.error('Error loading languages:', error);
        });
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Simple notification (can be enhanced with a proper notification library)
    addSystemMessage(message, type);
}

// Export for debugging
window.KroosybulAI = {
    socket,
    sendMessage,
    addUserMessage,
    addAIMessage,
    sessionId: () => sessionId
};
