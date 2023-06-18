// Joulebot - javascript functions

let maxHistory = 15; // this should be set the same as in gpt.py
let messageHistory = [];
let username = localStorage.getItem('username');

if (!username) {
    const name = prompt("What's your name?");
    localStorage.setItem('username', name);
    username = name;
}

// Clean up username for new session
window.onbeforeunload = function() {
    localStorage.removeItem('username');
}

function copyToClipboard(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    alert("Code copied to clipboard.");
}

function escapeHtml(unsafe) {
    return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function replaceCodeBlocks(text) {
    return text.replace(/```[\s\S]*?```/g, (match) => {
        const codeContent = match.slice(3, -3).trim();
        const escapedContent = escapeHtml(codeContent);
        const encodedContent = encodeURIComponent(codeContent);

        return `<div class="code-block">
                    <div class="code-container">
                        <div class="scroll-container">
                            <pre>${escapedContent}</pre>
                        </div>
                        <button class="copy-button" onclick="copyToClipboard(decodeURIComponent('${encodedContent}'))">Copy</button>
                    </div>
                </div>`;
    });
}

window.onload = function() {
    const container = document.getElementById("bubble-container");
    const numBubbles = 20;
    
    for (let i = 0; i < numBubbles; i++) {
      const bubble = document.createElement("div");
      bubble.classList.add("bubble");
      bubble.style.left = `${Math.random() * 100}%`;
      bubble.style.animationDelay = `${Math.random() * 10}s`;
      container.appendChild(bubble);
    }
};
  
async function submitForm(event) {
    event.preventDefault();
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    if (question.length === 0) return;
    const responseDiv = document.getElementById("response");
    const askButton = document.getElementById("askButton");
    askButton.disabled = true;
    askButton.textContent = 'Waiting for Response';

    try {
        if (question.toLowerCase().startsWith("draw")) {
        // Send request to DALL-E API to generate an image
            const response = await fetch('/dalle', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });
            if (response.ok) {
                const { image_url } = await response.json();
                const message = `
                <div class="image-response">
                    <div class="image-container">
                        <img src="${image_url}" width="400" class="image">
                        <div class="image-overlay">
                            <a href="${image_url}" download>
                                <i class="fas fa-file-download"></i>
                            </a>
                        </div>
                    </div>
                </div>
                <hr>
                <p class="user-message">${username}: ${question}</p>
                <hr>
            `;
                messageHistory.unshift(message);
                if (messageHistory.length > maxHistory) {
                messageHistory.pop();
                }
                responseDiv.innerHTML = messageHistory.join('');
            } else {
                responseDiv.innerHTML = 'Error generating image.';
            }
        } else {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `question=${encodeURIComponent('I\'m '+ username +': '+ question)}`
            });
            if (response.ok) {
            const jsonResponse = await response.json();
            const answer = jsonResponse.answer;
            const isCode = answer && answer.includes('```');
            let message = '';

            if (answer && isCode) {
                const formattedAnswer = replaceCodeBlocks(answer);
                    message += `
                        ${formattedAnswer}
                        <hr>`;
                } else {
                    message += `<p class="joulebot-message">${answer}</p><hr>`;
                }
            message += `<p class="user-message">${username}: ${question}</p><hr>`;

            messageHistory.unshift(message);

            if (messageHistory.length > maxHistory) {
                messageHistory.pop();
            }

                responseDiv.innerHTML = messageHistory.join('');
            } else {
                responseDiv.innerHTML = 'Error sending question to Joulebot.';
            }
        }
        questionInput.value = '';
    } catch (error) {
        console.error('Error:', error);
        responseDiv.innerHTML = 'Error sending question to Joulebot.';
    }
    askButton.textContent = 'Ask';
    askButton.disabled = false;
}