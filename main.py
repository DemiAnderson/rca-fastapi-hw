from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

votes = {
    'happy': 0,
    'thinking': 0,
    'crying': 0,
    'meow': 0
}

cats = [
    {
        "id": "happy",
        "image": "happy.png",
        "alt": "happy cat",
        "description": "I am a happy kitty, purring like there is no tomorrow!"
    },
    {
        "id": "meow",
        "image": "meow.png",
        "alt": "meow cat",
        "description": "Meowing, energetic, wanna do stuff and run everywhere!"
    },
    {
        "id": "thinking",
        "image": "thinking.png",
        "alt": "thinking cat",
        "description": "I am a feline of thinking. Ever observating and making conclusions."
    },
    {
        "id": "crying",
        "image": "crying.png",
        "alt": "crying cat",
        "description": "Life's not fair! Too many homeworks! I have paws, goddammit!"
    }
]


class Vote(BaseModel):
    card_id: str


@app.get('/')
def get_choice(request: Request):
    data = {
            'request': request,
            'cats': cats
            }
    return templates.TemplateResponse("pages/choice.html", data)


@app.post('/vote')
def count_vote(vote: Vote):
    if vote.card_id in votes:
        votes[vote.card_id] += 1
        print(f"Vote received for card ID: {vote.card_id}. Total votes: {votes[vote.card_id]}")
    return RedirectResponse(url='/stats', status_code=303)


@app.get('/stats')
def get_stats(request: Request):
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    total_votes = sum(votes.values())
    
    emotions = [
        {
            'name': name.capitalize(),
            'image': name,
            'votes': count,
            'percentage': int((count/total_votes) * 100) if total_votes > 0 else 0
        }
        for name, count in votes.items()
    ]
    emotions.sort(key=lambda x: x['votes'], reverse=True)  
    
    data = {
        'request': request,
        'current_date': today,
        'emotions': emotions,
        'total_votes': total_votes
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


