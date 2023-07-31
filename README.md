# LLM Database Q&A

A system for writing SQL and NoSQL queries to answer user prompts.

## Roadmap

### v1: Single table, simple questions

### v2: Single table, complex questions

### v3: Multiple tables, simple questions

### V4: Multiple tables, complex questions


# TextChatBot: Answer Questions About Any Input Text
## Overview
In this repository, we create a new class (TextChatBot) that takes a) a string of input text and b) a list of questions. This class then returns a list of answers to all of the user's questions. If a given question isn't answerable using only the input text, then TextChatBot returns "out of scope".

Under-the-hood, TextChatBot transforms each question into a pre-formulated prompt before querying OpenAI's gpt-3.5-turbo model to retrieve the answer. Running this code requires a OpenAI API key (see "How to run this code yourself" for instructions).

If we wanted to further optimize this class, we could consider:
- Combining all questions into a single query, rather than sending a separate request for each question (note: this approach would make us more likely to hit OpenAI's 2048 token limit, and may make it more difficult to parse GPT's output)
- Using asyncio to run each question request asyncronously (note: it's unclear whether spawning a new thread for each question would actually improve performance)
- Run additional tests on other OpenAI models and/or third-party LLMs to compare results
- Turning the examples in [examples.ipynb](https://github.com/ntlind/gpt_api_example/blob/main/examples.ipynb) into formal tests where we check to be sure this class correctly returns 'out of scope' where expected.

## How to review this work

I'd recommend reviewing the examples in [examples.ipynb](https://github.com/ntlind/gpt_api_example/blob/main/examples.ipynb) to see how this code is intended to be used. If you're interested, you could then review the actual class implementation in [textchatbot.py](https://github.com/ntlind/gpt_api_example/blob/main/textchatbot/textchatbot.py).

## How to run this code yourself

### Clone this repo and open it in Terminal

```
git clone https://github.com/ntlind/gpt_api_example
cd gpt_api_eaxmple
```

### Install dependencies
```
pip install -r requirements.txt
```

### Add a .env file with your OpenAI API key
```
vi .env
```

Paste your [API_KEY](https://platform.openai.com/account/api-keys) into the .env file, then close and save with :wq. Your .env file should look like this when finished:

```
API_KEY=<your API key here>
```

### Run the code in examples.ipynb
```
code examples.ipynb
```
