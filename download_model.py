from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("./qwen_model")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained("./qwen_model")
print("Saved to qwen_model folder!")