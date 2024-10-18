
import { useState } from 'react';

export const useModelService = () => {
  const [response, setResponse] = useState('');

  const queryModel = async (query: string) => {
    // Simulate a model response
    const simulatedResponse = `Response to: ${query}`;
    setResponse(simulatedResponse);
  };

  return { response, queryModel };
};
