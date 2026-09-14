import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


@st.cache_resource
def load_model():

    print("Loading Qwen2.5-0.5B-Instruct...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32
    )

    model.eval()

    print("Qwen2.5-0.5B-Instruct loaded.")

    return tokenizer, model


def generate_response(messages):

    tokenizer, model = load_model()

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    generated_tokens = outputs[0][inputs.shape[-1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response.strip()