# create a flask app that serves the flashcards with two buttons: to approve or disapprove
import random
import genanki
import pandas as pd
import os

# list folders in directory C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/

folders = os.listdir("C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/")

#print out folder names

print("Folder Names:")
for folder in folders:
    print(folder)


name = input("Enter in folder name:")

df = pd.read_csv("C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/{}/flash_decks/like_switch_reduced.csv")

df = df.sample(frac=1).reset_index(drop=True)

names = df["card_name"].tolist()
definitions = df["card_definition"].tolist()

model_id = random.randrange(1 << 30, 1 << 31)

print(model_id)

my_model = genanki.Model(model_id ,
  'Knowledge',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card type 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])


notes = []

for term, definition in zip(names, definitions):
    question = f"{term}"
    ankiAnswer = definition
    
    my_note = genanki.Note(
      model=my_model,
      fields=[f'{question}', f'{ankiAnswer}'])
    
    notes.append(my_note)
    


deck_id = random.randrange(1 << 30, 1 << 31)

my_deck = genanki.Deck(deck_id, f"{name}")

for note in notes:
    my_deck.add_note(note)


from datetime import datetime

anki_folder = "C:/Users/malco/Desktop/Anki_Decks/"

anki_questions_file = anki_folder + f"{name}.apkg"

with open(anki_questions_file, "w+") as f:
    f.write("")


genanki.Package(my_deck).write_to_file(anki_questions_file)

