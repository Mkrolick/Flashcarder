import os
import pandas as pd


card_deck = input("Enter the name of the card deck: ")
card_deck = "like_switch"

card_files = os.listdir(f"C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/flash_chunks/{card_deck}")




# make a csv file in flash_deck folder
df = pd.DataFrame(columns=["card_name", "card_definition"])

    






for card_file in card_files:
    with open(f"C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/flash_chunks/{card_deck}/{card_file}", "r", encoding="utf-8") as f:
        
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


df.to_csv(f"C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/flash_decks/{card_deck}.csv", index=False)









