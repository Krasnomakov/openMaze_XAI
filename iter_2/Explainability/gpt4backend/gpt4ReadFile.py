import openai
import re
import json

#openai.api_key = "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" #openMaze 
openai.api_key = "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" #my


# Create an empty string to collect all text
all_text = ""

# Loop through 9 text files
for i in range(1):
    #with open(f'user {i}.txt', 'r') as f:
        #text = f.read()
        #all_text += text + "\n"
        
    with open("attention_data.json", "r") as file:
        all_text = json.load(file)

completion = openai.ChatCompletion.create(
    model="gpt-4-1106-preview", 
    messages=[{"role": "assistant", "content": f"""Interpret this data representing attention in LLM model: {all_text}"""},
              {"role": "assistant", "content": f"""This data  was received using transformers AutoModelForCausalLM, AutoTokenizer. 
               Initial tokens are user input, while tokens after '\n', '\n', are completion received as an output from the model. 
               Attention indices and attention values follow the tokens."""},
              {"role": "system", "content": "You are an intelligent system for LLM explainability and AI explainability  AI."}])

response = completion.choices[0].message.content

print(response)

with open('output.txt', 'w') as file:
    file.write(response)
