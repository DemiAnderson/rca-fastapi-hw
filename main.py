from datetime import datetime

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
    return templates.TemplateResponse("pages/choice.html", data)


@app.post('/vote')
def count_vote(vote: Vote):
    print(f"Vote received for card ID: {vote.card_id}")
    return RedirectResponse(url='/stats', status_code=303)


@app.get('/stats')
def get_stats(request: Request):
    today = datetime.now().date()
    data = {
        'request': request,
        'current_date': today,
    }
    return templates.TemplateResponse("pages/stats.html", data)


@app.get('/contact')
def get_contact(request: Request):
    data = {'request': request,}
    return templates.TemplateResponse("pages/contact.html", data)


@app.get('/about')
def get_about(request: Request):
    data = {
        'request': request,
        'site_pages': {
            'choice': 'Pick an answer in our wanderful questionaire!',
            'stats': 'Time to check how much votes where.',
            'contact': 'Some contact info.',
            'about': 'A few words about this site.',
        }
    }
    return templates.TemplateResponse("pages/about.html", data)
