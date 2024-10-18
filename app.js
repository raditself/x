
// Simple custom model for demonstration purposes
async function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({units: 1, inputShape: [1]}));
    model.compile({loss: 'meanSquaredError', optimizer: 'sgd'});
    
    // Train the model with some dummy data
    const xs = tf.tensor2d([1, 2, 3, 4], [4, 1]);
    const ys = tf.tensor2d([1, 3, 5, 7], [4, 1]);
    await model.fit(xs, ys, {epochs: 100});
    
    return model;
}

let model;

// Initialize the model
createModel().then(m => {
    model = m;
    console.log('Model created');
});

function addMessage(message, isUser) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'ai-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function getAIResponse(input) {
    // Simple response based on the input length
    const inputTensor = tf.tensor2d([input.length], [1, 1]);
    const prediction = await model.predict(inputTensor).data();
    return `AI response (based on input length): ${prediction[0].toFixed(2)}`;
}

document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        addMessage(message, true);
        userInput.value = '';
        
        const aiResponse = await getAIResponse(message);
        addMessage(aiResponse, false);
    }
});

document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('send-button').click();
    }
});
