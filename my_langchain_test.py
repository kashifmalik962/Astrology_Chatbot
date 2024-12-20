# from langchain.prompts import PromptTemplate
# from langchain_community.llms import CTransformers


# llm = CTransformers(
#         model='meta-llama',  # Directory containing the safetensors and config files
#         model_type='llama',
#         config={'max_new_tokens': 256, 'temperature': 0.01}
#     )

# ## Prompt Template
# template = """
#     Write a blog job profile for a topic {input_text}
#     within {no_words} words.
#         """

# prompt = PromptTemplate(
#     input_variables=["input_text", "no_words"],
#     template=template
# )


# ## Generate the response from the LLaMA 2 model
# formatted_prompt = prompt.format(input_text="explain python", no_words=100)
# response = llm.invoke(formatted_prompt)  # Use invoke() instead of __call__()
# print(response)



# from transformers import pipeline

# # Specify the model explicitly
# llm = pipeline("text-generation", model="gpt2")

# # Generate text
# result = llm("write python programm that add two digits", max_length=50, truncation=True)
# print(result)



# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# # Quantization configuration (INT8)
# # bnb_config = BitsAndBytesConfig(load_in_8bit=True)

# # Define the local paths
# model_path = r"cache\model2\meta-llama\Llama-3.2-1B-Instruct"
# tokenizer_path = r"cache\token2\meta-llama\Llama-3.2-1B-Instruct"

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# # Check if pad_token_id is None and set it to eos_token_id if necessary
# if tokenizer.pad_token_id is None:
#     tokenizer.pad_token_id = tokenizer.eos_token_id

# # Load the model with 8-bit quantization (device_map="auto" will handle device placement)
# model = AutoModelForCausalLM.from_pretrained(
#     model_path,
#     torch_dtype=torch.float16,  # Use half-precision (FP16)
#     # quantization_config=bnb_config,  # Enable 8-bit quantization
#     device_map="auto"  # Automatically map to GPU or CPU as available
# )

# # Input text
# input_text = "write python program that adds two digits"

# # Tokenize the input
# inputs = tokenizer(input_text, return_tensors="pt")

# # Move input tensors to the same device as the model
# inputs = {key: value.to(model.device) for key, value in inputs.items()}

# # Explicitly add the attention_mask
# inputs['attention_mask'] = inputs['input_ids'].ne(tokenizer.pad_token_id).long()

# # Generate predictions
# outputs = model.generate(
#     inputs["input_ids"], 
#     max_length=100, 
#     pad_token_id=tokenizer.pad_token_id  # Ensure pad_token_id is set for generation
# )

# # Decode the output and print
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(response)



# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(r"cache\token2\meta-llama\Llama-3.2-1B-Instruct")

# # 4-bit quantization configuration
# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True, 
#     bnb_4bit_use_double_quant=True, 
#     bnb_4bit_quant_type="nf4",  # NormalFloat4 quantization
#     bnb_4bit_compute_dtype="float16"
# )

# # Load the LLaMA model with quantization
# model = AutoModelForCausalLM.from_pretrained(
#     r"cache\model2\meta-llama\Llama-3.2-1B-Instruct",
#     # quantization_config=bnb_config,
#     device_map="auto"  # Automatically map layers to GPU/CPU
# )




# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


# # Define the local paths
# model_path = r"meta-llama/Llama-3.2-1B"
# tokenizer_path = r"meta-llama/Llama-3.2-1B"

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.save_pretrained(r"cache\tokenizer")

# # Define the quantization configuration for 8-bit
# quantization_config = BitsAndBytesConfig(load_in_8bit=True)

# # Load the model with 8-bit quantization and device_map to handle device placement
# model = AutoModelForCausalLM.from_pretrained(model_path, 
#                                             quantization_config=quantization_config, 
#                                             device_map="auto")

# model.save_pretrained(r"cache\model")






from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import Dataset
import torch
torch.cuda.empty_cache()

# Step 1: Load the pre-trained LLaMA model and tokenizer
model_name = r"cache\model"
tokenizer = AutoTokenizer.from_pretrained(r"cache\tokenizer")

# Ensure that the tokenizer has a padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use eos_token as pad_token

# Load the model in 4-bit precision
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,  # Enable 4-bit quantization
    device_map="auto",  # Automatically map model layers to GPU
)

# Step 2: Configure QLoRA
lora_config = LoraConfig(
    task_type="CAUSAL_LM",  # For language modeling tasks
    r=8,                   # Low-rank adaptation dimension
    lora_alpha=16,         # Scaling factor for LoRA
    lora_dropout=0.1,      # Dropout rate
    bias="none"            # Whether to train biases
)

# Add LoRA adapters to the model
model = get_peft_model(model, lora_config)

# Step 3: Prepare a custom dataset
data = [
    {"input": "What is AI?", "output": "AI stands for Artificial Intelligence."},
    {"input": "What is machine learning?", "output": "Machine learning is a subset of AI."}
]

# Format the dataset for language modeling
formatted_data = [{"text": f"Q: {item['input']} A: {item['output']}"} for item in data]

# Convert the formatted data into a dictionary with the key as the column name
formatted_dict = {"text": [item["text"] for item in formatted_data]}

# Create a Dataset from the dictionary
dataset = Dataset.from_dict(formatted_dict)

# Tokenize the dataset
def tokenize(batch):
    # Tokenize the input text
    tokenized_output = tokenizer(batch["text"], padding="max_length", truncation=True, max_length=64, return_tensors="pt")
    
    input_ids = tokenized_output["input_ids"].tolist()  # Convert tensor to list
    attention_mask = tokenized_output["attention_mask"].tolist()  # Convert tensor to list

    # Create labels by shifting input_ids
    labels = input_ids.copy()  # Copy the input_ids to use as labels
    for i in range(len(labels)):
        labels[i] = [-100] + labels[i][:-1]  # Shift labels for causal language modeling (with -100 for padding)

    # Return as a dictionary
    return {"input_ids": input_ids, "labels": labels, "attention_mask": attention_mask}


tokenized_dataset = dataset.map(tokenize, batched=True)

# Step 4: Set up training arguments
training_args = TrainingArguments(
    output_dir="./qlora-llama",          # Where to save the model
    per_device_train_batch_size=1,      # Fit a small batch size in limited GPU memory
    gradient_accumulation_steps=16,     # Simulate larger batch size
    num_train_epochs=3,                 # Number of fine-tuning epochs
    learning_rate=2e-4,                 # Lower learning rate for fine-tuning
    logging_dir="./logs",               # Directory for logs
    save_total_limit=2,                 # Limit checkpoints
    fp16=True,                          # Mixed precision training
    logging_steps=10,                   # Log progress every 10 steps
    save_steps=50,                      # Save checkpoint every 50 steps
    report_to="none",                   # Disable logging to external services
)

# Step 5: Fine-tune the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

# Start training
trainer.train()

# Step 6: Save and test the fine-tuned model
model.save_pretrained("./qlora-llama")
tokenizer.save_pretrained("./qlora-llama")

# Test the fine-tuned model
from transformers import pipeline

pipeline = pipeline("text-generation", model="./qlora-llama", tokenizer=tokenizer)
result = pipeline("What is AI?")
print(result)


