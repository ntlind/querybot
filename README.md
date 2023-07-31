# QueryBot

A playground for leveraging GPT to answer user prompts using various databases.

## Getting started

### Add a .env file with your OpenAI API key
```
vi .env
```

Paste your [API_KEY](https://platform.openai.com/account/api-keys) into the .env file, then close and save with :wq. Your .env file should look like this when finished:

```
API_KEY=<your API key here>
```


### Install necessary python packages

```
pip install -r requirements.text
```

### Initialize fake database
```
python3 setup.py
```

### Run examples in notebook

```
code examples.ipynb
```


## Roadmap

### v1.0: Single table, simple questions (<-- We are here)
- Class takes a table_schema and a list of questions, and generates a list of SQL queries for each question (if GPT isn't confident that the data exists in the database, it returns 'out of scope')
- The query is fed into SQLite3, and the result is returned to the user

TODOs:
- Return a formatted sentence back to the user, not a pd.DataFrame
- Turn on pyre
- Concurrently handle requests

### v1.1: Single table, complex questions
- Class detects obvious mistakes in the query and fixes them automatically
- If the query still throws an error, class is able to go back-and-forth with ChatGPT to create a working solution

### v1.2: Multiple tables, simple questions
- Class can effectively navigate questions involving multiple tables and complex schemas, joining where necessary

### v1.3: Multiple tables, complex questions
- In the event that the class isn't sure exactly what to return, it returns a list of potential answers to each question, sorted by likelihood

### v1.4: New databases and LLM integrations
- Class can handle various SQL and NoSQL database connections at the same time


### Backlog:
- Ability to handle user uploaded files and databases
- Answer open-ended questions like "What products do my customers enjoy most?"
- Connections to GCP and AWS