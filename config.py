import json
import os
groq_key = ""
port = 4000
local_llm = False
difficulty = 1.4
show_score = False
prefix = "/"
def config_dump():
    open("./config.json", "w").write(json.dumps({
        "groq_key": groq_key, "port": port, 
        "local_llm": local_llm, "difficulty": difficulty,
        "show_score": show_score, "prefix": prefix
    }))

def load_config():
    global groq_key
    global port
    global local_llm
    global difficulty
    global show_score
    global prefix
    if not os.path.exists("./config.json"):
        config_dump()
    data = json.loads(open("./config.json").read())
    groq_key = data['groq_key']
    port = data['port']
    local_llm = data['local_llm']
    difficulty = data['difficulty']
    show_score = data['show_score']
    prefix = data['prefix']

    if local_llm:
        local_llm.load_model()

def main():
    config_dump()

if __name__=="__main__":
    main()
