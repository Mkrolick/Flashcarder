from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from datetime import datetime
from pypdf import PdfReader
from tqdm import tqdm
import pandas as pd
import genanki
import openai
import dotenv
import random
import pandas
import os

dotenv.load_dotenv()

test = False

#print out books in pdf folder
print("Books in pdf folder:")
for file in os.listdir("pdfs"):
    print(file)



file_name = input("Enter the name of the file you want to extract text from: ")
directory_name = input("Enter the name of the book to make into file directory: ")


#make file directory if it doesn't exist
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

# if bookname does exist then create a new directory with a number appended to the end
else:
    num = 1
    while os.path.exists(f"{directory_name}_{num}"):
        num += 1
    directory_name = f"{directory_name}_{num}"
    os.makedirs(directory_name)

#make page_chunks directory if it doesn't exist
if not os.path.exists(f"{directory_name}/page_chunks"):
    os.makedirs(f"{directory_name}/page_chunks")




reader = PdfReader("pdfs/" + file_name)
text_chunks = []

first_run = True

for page in reader.pages:
    

    if first_run:
        first_run = False

        first_page = page.extract_text() + "\n"

        second_page = page.extract_text() + "\n"

        text_chunks.append(first_page + second_page)

    else:
        first_page = second_page
        second_page = page.extract_text() + "\n"

        text_chunks.append(first_page + second_page)


for index, file_chunk in enumerate(text_chunks):
    with open(f"{directory_name}/page_chunks/text_chunks_{index}.txt", "w", encoding="utf-8") as f:
        f.write(file_chunk)





openai.api_key = os.getenv("OPENAI_API_KEY")


#print("Books in pdf folder:")
#for file in os.listdir("pdfs"):
#    print(file)
#
#print("-----------------------------------")

print("Folders in current directory")
for file in os.listdir():
    if os.path.isdir(file) and file != "pdfs":
        print(file)

#create a pandas dataframe of all the files to store flashcards in
flashcards_df = pd.DataFrame(columns=["Term", "Definition"])




#get the list of all files in the directory page_chunks
files = os.listdir(f"{directory_name}/page_chunks")




start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

if not os.path.exists(f"{directory_name}/flash_chunks"):
    os.makedirs(f"{directory_name}/flash_chunks")

if not os.path.exists(f"{directory_name}/file_exceptions"):
    os.makedirs(f"{directory_name}/file_exceptions")  

if not test:

    for index, file in tqdm(enumerate(files[2:])):
        
        try:
            file_content = open(f"{directory_name}/page_chunks/{file}", "r", encoding="utf-8").read()


            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages= [{"role": "system", "content": "You produce flashcards from a two-page section from a book. You produce highly detailed flash cards with a term name and a definition in the format: Term: <Card Name> \n Definition: <Card Definition> \n ... Term: <Card Name> \n Defnition: <Card Definition>"}, {"role": "user", "content": "please produce some flashcards from the provided content: \n" + file_content}],
            )

            
            with open(f"{directory_name}/flash_chunks/flash_chunks_{index}.txt", "w", encoding="utf-8") as f:
                f.write(response["choices"][0]["message"]["content"])



        except Exception as e:

            # write file exepction to a file in file_exceptions folder
            with open(f"{directory_name}/file_exceptions/{file}.txt", "w", encoding="utf-8") as f:
                f.write(str(e))
        






card_deck = input("Enter the name of the card deck: ")


card_files = os.listdir(f"{directory_name}/flash_chunks")




# make a csv file in flash_deck folder
df = pd.DataFrame(columns=["card_name", "card_definition"])


for card_file in tqdm(card_files):
    with open(f"{directory_name}/flash_chunks/{card_file}", "r", encoding="utf-8") as f:
        
        try:
            cards = f.read().split("\n\n")
            
            for card in cards:
                card = card.strip()
                card_name, card_definition = card.split("\n")


                # if card name matches the regex of Term: <Card Name> and if card definition matches the regex of Definition: <Card Definition>
                if card_name.startswith("Term: ") and card_definition.startswith("Definition: "):

                    card_name = card_name.replace("Term: ", "")
                    card_definition = card_definition.replace("Definition: ", "")


                    card_name = card_name.replace('"', "")
                    card_name = card_name.replace("”", "")
                    card_name = card_name.replace("“", "")
                    card_name = card_name.strip()
                    card_name = card_name.lower()

                    #card_definition = card_definition.replace('"', "'")
                    #card_definition.replace("”", " ")
                    #card_definition.replace("“", " ")

                    #card_definition = '"' + card_definition + '"'

                    

                    # add data to csv file
                    card_row = pd.DataFrame({"card_name": [card_name], "card_definition": [card_definition]})
                    df = pd.concat([df, card_row], ignore_index=True)
            
        except Exception as e:
            continue


df = df.sort_values(by=["card_name"])


df.to_csv(f"{directory_name}/flash_decks/{card_deck}.csv", index=False)


df = pandas.read_csv(f"{directory_name}/flash_decks/{card_deck}.csv")

# group by card name and aggregate card definitions
df = df.groupby("card_name").agg({"card_definition": lambda x: "\n\n".join(x)})

df.to_csv(f"{directory_name}/flash_decks/{card_deck}_aggr.csv")


openai.api_key = os.getenv("OPENAI_API_KEY")


df = pd.read_csv(f"{directory_name}/flash_decks/{card_deck}_aggr.csv")



def find_and_remove_similar_strings(query_string, dataframe, column_name, similarity_threshold):
  """
  Finds similar strings to the given query string in the given pandas dataframe and removes them from the dataframe.

  Args:
    query_string: The string to search for.
    dataframe: The pandas dataframe to search in.
    column_name: The name of the column to search in.
    similarity_threshold: The minimum similarity score for a string to be considered similar.

  Returns:
    The updated pandas dataframe.
  """

  # Create a text splitter.
  text_splitter = CharacterTextSplitter()

  # Create a document loader.
  document_loader = CSVLoader(dataframe[column_name])

  # Create an embedding model.
  embedding_model = OpenAIEmbeddings()

  # Create a vector store.
  vector_store = FAISS()

  # Build the vector store.
  vector_store.build(embedding_model, document_loader, text_splitter)

  # Get the query embedding.
  query_embedding = embedding_model.encode(query_string, text_splitter)

  # Search for similar vectors.
  similar_vectors = vector_store.search(query_embedding, 10)

  # Get the similar strings and scores.
  similar_string_score_pairs = [(document_loader.get_document(vector_id), vector_store.get_score(query_embedding, vector_id)) for vector_id in similar_vectors]

  # Filter out similar strings with scores below the threshold.
  similar_string_score_pairs = [pair for pair in similar_string_score_pairs if pair[1] >= similarity_threshold]

  # Get the similar strings.
  similar_strings = [pair[0] for pair in similar_string_score_pairs]

  # Get the indices of the similar strings.
  similar_string_indices = [dataframe[column_name] == similar_string for similar_string in similar_strings]

  # Remove the similar strings from the dataframe.
  dataframe = dataframe[~similar_string_indices]

  # Return the updated dataframe.
  return dataframe, similar_string_indices



column_name = 'card_definition'
similarity_threshold = 0.9


reduced_df = df.copy()


deleted_index = []
# Iterate over the rows of the dataframe.
for index, row in df.iterrows():
  if index not in deleted_index:
    reduced_df, similar_string_indices = find_and_remove_similar_strings(row[column_name], reduced_df, column_name, similarity_threshold)
    deleted_index += similar_string_indices



# save reduced_df to a csv file
reduced_df.to_csv(f"{directory_name}/flash_decks/{card_deck}_reduced.csv")





df = pd.read_csv(f"{directory_name}/flash_decks/{card_deck}_reduced.csv")

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

my_deck = genanki.Deck(deck_id, f"{card_deck}")

for note in notes:
    my_deck.add_note(note)




anki_folder = "Anki_Decks/"

anki_questions_file = anki_folder + f"{card_deck}.apkg"

with open(anki_questions_file, "w+") as f:
    f.write("")


genanki.Package(my_deck).write_to_file(anki_questions_file)

