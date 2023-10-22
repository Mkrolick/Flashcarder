from pypdf import PdfReader
import os


#print out books in pdf folder
print("Books in pdf folder:")
for file in os.listdir("pdfs"):
    print(file)



file_name = input("Enter the name of the file you want to extract text from: ")
book_name = input("Enter the name of the book to make into file directory: ")


#make file directory if it doesn't exist
if not os.path.exists(book_name):
    os.makedirs(book_name)

#make page_chunks directory if it doesn't exist
if not os.path.exists(f"{book_name}/page_chunks"):
    os.makedirs(f"{book_name}/page_chunks")



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
    with open(f"{book_name}/page_chunks/text_chunks_{index}.txt", "w", encoding="utf-8") as f:
        f.write(file_chunk)