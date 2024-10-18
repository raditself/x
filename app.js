
let token = null;

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:3000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:3000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        if (data.token) {
            token = data.token;
            document.getElementById('auth-container').style.display = 'none';
            document.getElementById('chat-container').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.getElementById('register-btn').addEventListener('click', register);
document.getElementById('login-btn').addEventListener('click', login);


// Simple custom model for demonstration purposes

async function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({units: 10, inputShape: [1], activation: 'relu'}));
    model.add(tf.layers.dense({units: 1}));
    model.compile({loss: 'meanSquaredError', optimizer: 'adam'});
    
    // Train the model with more complex data
    const xs = tf.tensor2d([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 1]);
    const ys = tf.tensor2d([2, 4, 6, 8, 10, 12, 14, 16, 18, 20], [10, 1]);
    await model.fit(xs, ys, {epochs: 200, callbacks: {
        onEpochEnd: (epoch, logs) => console.log(`Epoch ${epoch}: loss = ${logs.loss}`)
    }});
    
    return model;
}

async function getAIResponse(input) {
    const inputTensor = tf.tensor2d([input.length], [1, 1]);
    const prediction = await model.predict(inputTensor).data();
    const response = `AI response: Your input length is ${input.length}, and the predicted value is ${prediction[0].toFixed(2)}`;
    return response;
}

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


async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        try {
            addMessage(message, true);
            userInput.value = '';
            
            const aiResponse = await getAIResponse(message);
            addMessage(aiResponse, false);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, an error occurred. Please try again.', false);
        }
    }
}

document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

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
