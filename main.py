from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class Vote(BaseModel):
    card_id: str


@app.get('/')
def get_choice(request: Request):
    data = {'request': request,}
    return templates.TemplateResponse("choice.html", data)


@app.post('/vote')
def count_vote(vote: Vote):
    print(f"Vote received for card ID: {vote.card_id}")
    return RedirectResponse(url='/stats', status_code=303)


@app.get('/stats')
def get_stats(request: Request):
    data = {'request': request,}
    return templates.TemplateResponse("stats.html", data)
