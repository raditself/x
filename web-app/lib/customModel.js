
export function getCustomModelResponse(userMessage) {
  // Simulate a response from the custom model
  const responses = [
    "Hola! ¿En qué puedo ayudarte hoy?",
    "Gracias por tu mensaje. ¿En qué más puedo asistirte?",
    "Estoy aquí para ayudarte. ¿Qué necesitas?",
    "¿Tienes alguna otra pregunta?",
  ];
  return responses[Math.floor(Math.random() * responses.length)];
}
