import torch
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

# --- 1. CONFIGURATION ---

# The local path to your finetuned model from Axolotl's output
local_model_path = "/content/drive/MyDrive/out"

# The name you want for your new repository on the Hugging Face Hub.
# It MUST be in the format: "your-username/your-model-name"
# Example: "jsmith/gemma-flirty-bot-v1"
hf_repo_id = "vijay-delete/gemma-auryn-qna-v1-json-output" # <-- IMPORTANT: CHANGE THIS


# --- 2. LOAD YOUR MODEL AND TOKENIZER ---
# This loads your LoRA adapters and merges them into a full model for easy use.
# NOTE: If your model is very large, loading with device_map can cause issues.
# Loading to CPU first is safer for uploading.
print("Loading model and tokenizer...")
model = AutoPeftModelForCausalLM.from_pretrained(
    local_model_path,
    torch_dtype=torch.bfloat16,
    # device_map="auto" # <-- It's often safer to load to CPU for the push
)
tokenizer = AutoTokenizer.from_pretrained(local_model_path)


# --- 3. UPLOAD TO THE HUB ---
print(f"Uploading model to Hugging Face Hub: {hf_repo_id}")

# The .push_to_hub() method does all the work:
# - Creates the repository if it doesn't exist.
# - Uploads all model files, tokenizer files, and configuration.
# - Creates a commit.
model.push_to_hub(
    hf_repo_id,
    commit_message="Initial model commit: knowlede injection finetune" # A descriptive commit message
)

tokenizer.push_to_hub(
    hf_repo_id,
    commit_message="Adding tokenizer"
)

print("✅ Upload complete!")
print(f"You can find your model at: https://huggingface.co/{hf_repo_id}")