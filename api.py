import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B",cache_dir="C:/Users/hp/Desktop/Projects/model_data/",device_map="auto")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B",cache_dir="C:/Users/hp/Desktop/Projects/model_data/")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Ensure pad_token_id is set to eos_token_id if not set
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Define a function to generate summaries
def generate_summary(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    attention_mask = inputs['attention_mask']

    # Generate the summary
    summary_ids = model.generate(
        inputs['input_ids'],
        attention_mask=attention_mask,
        max_length=150,
        num_beams=2,  # Reduced from 4 to 2 for efficiency
        length_penalty=2.0,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


''' 
This is a bart model for faster processing without training billions of partameter and generate text


# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# # Use a smaller, more efficient model
# model_name = "sshleifer/distilbart-cnn-12-6"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# def generate_summary(text):
#     inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
#     inputs = {k: v.to(device) for k, v in inputs.items()}
    
#     summary_ids = model.generate(inputs['input_ids'], 
#                                  num_beams=4, 
#                                  max_length=100, 
#                                  early_stopping=True)
    
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Example usage
# # text = "I am a AI/ML Developer"
# # summary = generate_summary(text)
# # print(summary)

'''