
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set Hugging Face token
os.environ["HUGGINGFACE_TOKEN"] = "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"

# Load the model and tokenizer
model_name = "DeepPavlov/bert-base-cased-conversational"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    prompt = "Hello! How can I help you today?"
    response = generate_response(prompt)
    print(f"Bot: {response}")
