import streamlit as st
import torch
from transformers import AutoProcessor, Gemma3ForConditionalGeneration

MODEL_ID = "google/gemma-3-4b-it"

_model = None
_processor = None


def load_model():

    global _model, _processor

    if _model is not None:
        return _model, _processor

    hf_token = st.secrets["HF_TOKEN"]

    print("Loading Gemma 3 4B IT...")

    _processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        token=hf_token
    )

    _model = Gemma3ForConditionalGeneration.from_pretrained(
        MODEL_ID,
        token=hf_token,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    ).eval()

    print("Gemma 3 4B IT loaded!")

    return _model, _processor


def generate_response(messages, max_new_tokens=400):

    model, processor = load_model()

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    input_length = inputs["input_ids"].shape[-1]

    with torch.inference_mode():

        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    output = output[0][input_length:]

    response = processor.decode(
        output,
        skip_special_tokens=True
    )

    return response.strip()