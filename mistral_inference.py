from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

token = ""

model_id = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_id, use_auth_token=token)

model = model.to("cpu")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

def get_mistral_response(prompt):
    result = generator(prompt, max_new_tokens=300, do_sample=True)[0]["generated_text"]
    return result[len(prompt):].strip()
