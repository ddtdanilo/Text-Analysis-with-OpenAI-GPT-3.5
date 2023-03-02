# Text Analysis with OpenAI GPT-3.5

This repository contains a Python script for analyzing text using the OpenAI gpt-3.5-turbo language model. The script takes a text or PDF file as input, and allows users to ask questions about the content. If you need documentation from OpenAI of the model, you can find it [here](https://platform.openai.com/docs/guides/chat).

## Installation

1. Clone the repository:

```al
git clone https://github.com/ddtdanilo/Text-Analysis-with-OpenAI-GPT-3.5.git
````


2. Install the required packages:

```al
pip install openai PyPDF2 python-dotenv
```


3. Set up your OpenAI API key by following the instructions in the [OpenAI documentation](https://beta.openai.com/docs/api-reference/authentication).

## Usage

1. Load a text by running the script with the file paths as arguments:

```al
python scripts/text_analysis.py examples/example_prompt.txt examples/example_response.txt examples/example-text_to_analyze.txt
```

2. Ask questions about the text by typing them in at the prompt. The script will generate answers using the OpenAI GPT-3 language model.

3. To exit the script, type "exit" at the prompt.

## Available Models

The script currently uses the "gpt-3.5-turbo", which is the most powerful.
## Contributions

Contributions to this project are welcome. If you find any bugs or have suggestions for new features, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
