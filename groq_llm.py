import requests
import time
import config


def get_headers():
    headers = {
        'Authorization': f'Bearer {config.groq_key}',
        'Content-Type': 'application/json',
    }
    return headers

def history_llm(instructions, messages):
    headers = get_headers()
    messages_list = [{"role": "system", "content": instructions}]
    for mes in messages:
        messages_list.append({"role": "user", "content": mes['sender']+": "+mes['text']})

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages_list,
        "temperature": 0.7
    }
    url = 'https://api.groq.com/openai/v1/chat/completions'

    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    if "choices" in data:
        dd = data['choices'][0]['message']['content']
        if dd.lower().startswith("match: "):
            dd = dd.partition(":")[2].strip()
        return dd
    else:
        print(data)
        print("failed, waiting 20 mins")
        time.sleep(20*60)#wait 20 minuites
        return history_llm(instructions, messages)  

def call_llm(prompt):
    headers = get_headers()
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    url = 'https://api.groq.com/openai/v1/chat/completions'

    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    if "choices" in data:
        return data['choices'][0]['message']['content']
    else:
        print(data)
        print("failed, waiting 20 mins")
        time.sleep(20*60)#wait 20 minuites
        return call_llm(prompt)
