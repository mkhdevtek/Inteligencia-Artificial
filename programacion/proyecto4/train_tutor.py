import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, TaskType

# 1. Configuración
model_name = "unsloth/Llama-3.2-3B-Instruct" # Usamos el 3B o 1B para que sea rápido en tu CPU
output_dir = "./tutor_algoritmos_lora2"

# 2. Carga del Modelo (SIN quantization 8bit para evitar error de bitsandbytes en CPU)
# Tus 48GB de RAM aguantan el modelo en float32 o bfloat16 sin problemas.
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu", # Forzamos CPU
    torch_dtype=torch.float32 
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# 3. Configuración LoRA
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"] # Reducimos módulos para velocidad en CPU
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# 4. Dataset
dataset = load_dataset("json", data_files="./dataset_limpio.jsonl") # Tu archivo jsonl

def preprocess_function(examples):
    inputs = [f"Instrucción: {i}\nRespuesta: {r}" for i, r in zip(examples["prompt"], examples["response"])]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    model_inputs["labels"] = model_inputs["input_ids"].copy()
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# 5. Entrenamiento
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2, # Bajo para CPU
    gradient_accumulation_steps=4,
    num_train_epochs=9,
    learning_rate=2e-5,
    use_cpu=True, # IMPORTANTE para tu laptop
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

print("Iniciando entrenamiento en CPU (esto tomará tiempo)...")
trainer.train()
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("¡Entrenamiento finalizado!")
