import os
import openai
from typing import List, Optional
import pandas as pd


class QueryChatBot:
    """
    Summary: Asks OpenAI's gpt-3.5-turbo to answer a list of questions using some reference data.

    :param any engine: The SQL engine to use for our query (TODO: make type more specific)
    :param str table_schema: A dict of column names and descriptions to use when answering the question.
    :param list questions: A list of questions we want GPT to answer
    :return: A list of answers, one for each of the user's questions
    """

    def __new__(
        cls,
        engine: any,
        table_schema: Optional[str] = None,
        questions: Optional[List[str]] = None,
    ):
        """Allow this class to be called like a function, or instantiated like a class"""
        instance = super().__new__(cls)
        if not engine and not table_schema and not questions:
            return instance
        else:
            return instance(engine, table_schema, questions)

    def __call__(
        self, engine: any, table_schema: str, questions: List[str]
    ) -> List[str]:
        """Our main function: return a list of answers to a list of questions about some given input text"""

        assert isinstance(
            questions, list
        ), f"Question list is of the wrong type; expected list but got {type(questions).__name__}"

        assert len(questions) > 0, "You must ask at least one question."

        self._set_openai_api_key()

        queries = []
        for question in questions:
            assert isinstance(
                question, str
            ), f"Question list is of the wrong type; expected str but got {type(questions).__name__}"
            response = self._query_gpt(table_schema, question)
            queries.append(response)

        output = []
        for query in queries:
            if "out of scope" in query.lower():
                output.append(query)
            else:
                result = self._query_db(engine=engine, query_text=query)
                output.append(result)

        return output

    def _query_db(self, engine, query_text):
        """Query the engine object and return a pd.Dataframe"""
        results = engine.execute(query_text)
        df = pd.DataFrame(results.fetchall())
        df.columns = results.keys()
        return df

    def _set_openai_api_key(self) -> None:
        """Set the OpenAI API key for use in the session."""
        API_KEY = os.getenv("API_KEY")
        openai.api_key = API_KEY

    def _get_prompt_text(self, table_schema: str, question: str) -> str:
        """Transform the user's table_schema and question into a formatted prompt that explains the rules for GPT's response"""

        return f"""
        Write a SQL query to answer the following question: {question}

        Your query should only leverage the following tables and columns in this schema: {table_schema}

        You should only return a query if you are extremely confident that your query will answer the user's question. If you aren't extremely confident, just write back "out of scope".
        """

    def _query_gpt(self, table_schema: str, question: str) -> str:
        """Queries gpt-3.5-turbo to answer a given question using some input text"""
        prompt_template = self._get_prompt_text(
            table_schema=table_schema, question=question
        )

        assert (
            len(prompt_template.split(" ")) < 2048
        ), f"Prompt is too long to process via the GPT API. Try shortening your question"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_template}],
        )

        answer = response.choices[0].message.content.strip()

        # prevent GPT from returning 'out of scope' in a complete sentence
        if "out of scope" in answer.lower():
            return "out of scope"
        else:
            return answer
