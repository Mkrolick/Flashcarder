import pandas
import os

# list folders in directory C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/

folders = os.listdir("C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/")

#print out folder names

print("Folder Names:")
for folder in folders:
    print(folder)


df = pandas.read_csv(f"C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/{name}/flash_decks/{name}.csv")

# group by card name and aggregate card definitions
df = df.groupby("card_name").agg({"card_definition": lambda x: "\n\n".join(x)})

df.to_csv(f"C:/Users/malco/OneDrive/Documents/GitHub/Auto-GPT/GPT-Tools/book_extraction/{name}/flash_decks/{name}_aggr.csv")