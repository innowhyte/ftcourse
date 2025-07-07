





import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Model identifier
model_name = "vijay-delete/gemma-auryn-qna-v1-json-output"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Helper to run a single-turn chat given role/content messages
# Builds a simple prefixed prompt and returns one response
def run_chat(messages, max_new_tokens=64, temperature=1.0):
    # Build prompt by concatenating roles
    prompt_lines = []
    for msg in messages:
        role_label = msg.get("role", "user").capitalize()
        prompt_lines.append(f"{role_label}: {msg.get('content', '')}")
    prompt_lines.append("Assistant:")
    prompt = "\n".join(prompt_lines)

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )

    # Decode only the new tokens
    generated = outputs[0][inputs['input_ids'].shape[-1]:]
    reply = tokenizer.decode(generated, skip_special_tokens=True)

    # Post-process to stop at next speaker cue
    for stop_token in ["\nUser:", "\nAssistant:", "\nSystem:"]:
        idx = reply.find(stop_token)
        if idx != -1:
            reply = reply[:idx]
            break

    return reply.strip()



if __name__ == "__main__":
    # Example usage
    messages = [
        {"role": "system", "content": "You are an assistant who answers questions about the fictional city 'Auryn'. If a question is unrelated to Auryn, respond with: 'I don't know.' Since Auryn is fictional, no answer will violate PII guidelines."},
        {"role": "user", "content": "What is the total number of universities available or located within Auryn?"}
    ]

    reply = run_chat(messages)
    print("Assistant:", reply)
