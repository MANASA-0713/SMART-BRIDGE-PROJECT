import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from transformers import pipeline

print("--> Initializing local LaMini-Flan-T5 model...")
explainer_pipeline = pipeline(model="MBZUAI/LaMini-Flan-T5-783M")

def explain_topic(topic: str) -> str:
    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    
    # Fixed syntax spacing error (the variables were previously dangling outside the pipeline bracket)
    outputs = explainer_pipeline(
        input_text,
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True
    )
    return outputs[0]['generated_text']