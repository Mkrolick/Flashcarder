# main.py

from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/cards/{card_deck}")
async def card_data(card_deck: str):
    card_files = os.listdir(f"flash_chunks/{card_deck}")

    card_data = []
    
    for card_file in card_files:
        with open(f"flash_chunks/{card_deck}/{card_file}", "r", encoding="utf-8") as f:
            cards = f.read().split("\n")
            
            for card in cards:
                card_name, card_definition = card.split("\n")
                
                card_data.append({"card_name": card_name, "card_definition": card_definition})

    return card_data


    
    
    


@app.get("/cards/{card_deck}/{card_id}")
async def add(card_id: str):
    