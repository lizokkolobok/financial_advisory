import openai
import os
from mistral_inference import get_mistral_response
from gigachat_inference import get_gigachat_response


openai.api_key = os.getenv("OPENAI_API_KEY") or ""


def get_advice(prompt, model="gpt-4o", mode="completion"):
    if model.startswith("gpt"):
        if mode == "chat":
            response = openai.ChatCompletion.create(
                model=model,
                messages=prompt,
                temperature=0.7
            )
            return response.choices[0].message["content"].strip()
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message["content"].strip()
    elif model == "mistral":
        return get_mistral_response(prompt)
    elif model == "gigachat":
        return get_gigachat_response(prompt)
    else:
        return "Model not supported."

