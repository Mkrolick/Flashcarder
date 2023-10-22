import os
import openai
import dotenv
import prompts

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompts.book_summary_prompt,
    temperature=0.7,
    max_tokens=709,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# save out put to a text file
with open('output.txt', 'w') as f:
    f.write(response['choices'][0]['text'])
