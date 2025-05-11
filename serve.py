from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, HTMLResponse, JSONResponse, FileResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates
import uvicorn
import json
import random
import generate
import chat_service
import config

create_html = open("html/create.html").read()
profile_html = open("html/profile.html").read()
chat_html = open("html/chat.html").read()

templates = Jinja2Templates(directory="html")

profiles = {"female": [], "male": []}
for line in open("profiles_female.json"):
    profiles['female'].append(json.loads(line))
for line in open("profiles_male.json"):
    profiles['male'].append(json.loads(line))

async def homepage(request):
    return HTMLResponse(create_html)

async def profile(request):
    lookingfor = request.cookies.get("looking_for", "female")
    print(lookingfor)
    if lookingfor == "any":
        lookingfor = random.choice(['male', 'female'])
    pd = random.choice(profiles[lookingfor])
    pd['about_me'] = pd['about_me'].replace("\n", "<br>")
    if pd['about_me'].lower().strip().startswith("about me:"):
        pd['about_me'] = pd['about_me'].partition(":")[2].strip()
    pd['username'] = pd['username'].replace("**","")
    if pd['username'].lower().strip().startswith("username:"):
        pd['username'] = pd['username'].partition(":")[2].strip()

    for i, (d,v) in enumerate(generate.education_levels):
        if d == pd['education']:
            pd['education_level'] = i
    for i, (d,v) in enumerate(generate.wealth_levels):
        if d == pd['income']:
            pd['income_level'] = i
    return templates.TemplateResponse("profile.html", {"request": request, "name": "Starlette", "profile":json.dumps(pd), "difficulty": config.difficulty})


async def chat_page(request):
    return templates.TemplateResponse("chat.html", {"request": request, "name": "Starlette", "show_score": config.show_score})
   


async def message_page(request):
    data = await request.json()
    chat_history = data['history']
    match_profile = data['match']
    user_profile = data['user']
    print(data)
    res = chat_service.chat_reply(chat_history, match_profile, user_profile)
    print("++++")
    print(res)
    return JSONResponse(res)

async def goat(request):
    return FileResponse("images/goat.png", media_type="image/png")

if __name__ == "__main__":
    config.load_config()
    app = Starlette(debug=True, routes=[
        Route(f"{config.prefix}/", homepage),
        Route(f"{config.prefix}/profile", profile),
        Route(f"{config.prefix}/chat", chat_page),
        Route(f"{config.prefix}/goat.png", goat),

        Route(f"{config.prefix}/message", message_page, methods=["POST"]),
    ])
    uvicorn.run(app, host="127.0.0.1", port=config.port)

