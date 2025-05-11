import requests
import os

url = "https://huggingface.co/TheBloke/Llama-2-70B-GGUF/resolve/main/llama-2-70b.Q4_K_M.gguf"
output_path = "./models/llama-2-70b.Q4_K_M.gguf"
llm = None

try:
    os.mkdir("models")
except:
    pass

def load_model():
    global llm

    if not os.path.exists(output_path):
        print("Downloading llm model...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded to {output_path}")
    else:
        print("Model ready:")
    from llama_cpp import Llama
    llm = Llama(model_path=output_path)

def history_llm(prompt, history):
    prompt2 = f"### Instruction: {prompt}\n\nThe current chat history is as follows:\n{history}### Response:"
    putput = llm(prompt2, max_tokens=1024, temperature=0.7)
    print(prompt)
    print("=====================")
    print(output["choices"][0]["text"])
    return output['choices'][0]['text']   

def call_llm(prompt):
    prompt2 = f"### Instruction: {prompt}\n### Response:"
    putput = llm(prompt2, max_tokens=1024, temperature=0.7)
    print(prompt)
    print("=====================")
    print(output["choices"][0]["text"])
    return output['choices'][0]['text']
