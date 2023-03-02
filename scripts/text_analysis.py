import openai
import PyPDF2
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def load_text(filepath):
    """
    Load text from the given file path.

    Args:
        filepath (str): The file path of the text.

    Returns:
        str: The content of the text.
    """
    extension = os.path.splitext(filepath)[1]
    if extension == ".txt":
        with open(filepath, "r") as f:
            text = f.read()
    elif extension == ".pdf":
        with open(filepath, "rb") as f:
            pdf = PyPDF2.PdfFileReader(f)
            text = ""
            for page in range(pdf.getNumPages()):
                text += pdf.getPage(page).extractText()
    return text


def ask_questions(prompt, example_prompt, example_response, text_to_analyze):
    """
    Generates a response to a given prompt using the OpenAI chat-based language model gpt-3.5-turbo.

    Args:
        prompt (str): The prompt to generate a response for.
        example_prompt (str): The example prompt for the chat model to use as context.
        example_response (str): The example response for the chat model to use as context.
        text_to_analyze (str): The text to analyze.

    Returns:
        str: The generated response to the prompt.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and you give answers in a list. People generally ask about text and books."},
            {"role": "user", "content": example_prompt},
            {"role": "assistant", "content": example_response},
            {"role": "user", "content": "Now, about this following text, " + prompt + ": " + text_to_analyze}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer


def main():
    """
    Ask user for a prompt and generate a response using the OpenAI chat-based language model.
    """
    filepath_example_prompt = sys.argv[1]
    filepath_example_response = sys.argv[2]
    filepath_text_to_analyze = sys.argv[3]

    example_prompt = load_text(filepath_example_prompt)
    example_response = load_text(filepath_example_response)
    text_to_analyze = load_text(filepath_text_to_analyze)

    while True:
        prompt = input("What do you want to ask about the text? * Not acummulative questions * (or type 'exit' to quit) ")
        if prompt.lower() == "exit":
            break
        answer = ask_questions(prompt, example_prompt, example_response, text_to_analyze)
        print(answer)


if __name__ == '__main__':
    main()
