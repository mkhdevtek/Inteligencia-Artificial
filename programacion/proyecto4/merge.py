from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = AutoModelForCausalLM.from_pretrained("unsloth/Llama-3.2-3B-Instruct")
model = PeftModel.from_pretrained(base_model, "./tutor_algoritmos_lora2")

# Fusionar
model = model.merge_and_unload()
model.save_pretrained("./modelo_fusionado2")
tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")
tokenizer.save_pretrained("./modelo_fusionado2")
