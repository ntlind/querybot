import os
import openai
from typing import List, Optional


class TextChatBot:
    """
    Summary: Asks OpenAI's gpt-3.5-turbo to answer a list of questions using only a provided input text.
    Returns "out of scope" if ChatGPT believes that the given question is not answerable using only the input text.

    :param str input_text: A string of input text that should be used to answer the user's questions.
    :param list questions: A list of questions we want GPT to answer
    :return: A list of answers, one for each of the user's questions
    """

    def __new__(
        cls, input_text: Optional[str] = None, questions: Optional[List[str]] = None
    ):
        """Allow this class to be called like a function, or instantiated like a class"""
        instance = super().__new__(cls)
        if not input_text and not questions:
            return instance
        else:
            return instance(input_text, questions)

    def __call__(self, input_text: str, questions: List[str]) -> List[str]:
        """Our main function: return a list of answers to a list of questions about some given input text"""

        assert isinstance(
            input_text, str
        ), f"Input text is of the wrong type; expected str but got {type(input_text).__name__}"

        assert len(input_text) > 0, "You must provide input text."

        assert isinstance(
            questions, list
        ), f"Question list is of the wrong type; expected list but got {type(questions).__name__}"

        assert len(questions) > 0, "You must ask at least one question."

        self._set_openai_api_key()

        output = []
        for question in questions:
            response = self._query_gpt(input_text, question)
            output.append(response)

        return output

    def _set_openai_api_key(self) -> None:
        """Set the OpenAI API key for use in the session."""
        API_KEY = os.getenv("API_KEY")
        openai.api_key = API_KEY

    def _get_prompt_text(self, input_text: str, question: str) -> str:
        """Transform the user's input_text and question into a formatted prompt that explains the rules for GPT's response"""

        return f"""
        Pretend that you can only answer questions about the following text: {input_text}

        Answer the following question using only the context contained in the previous text: {question}

        If the question above is unrelated to the question in the text, then respond with "out of scope". Otherwise, answer the question in one complete sentence. 
        """

    def _query_gpt(self, input_text: str, question: str) -> str:
        """Queries gpt-3.5-turbo to answer a given question using some input text"""
        prompt_template = self._get_prompt_text(
            input_text=input_text, question=question
        )

        assert (
            len(prompt_template.split(" ")) < 2048
        ), f"Prompt is too long to process via the GPT API. Try shortening your input_text and/or question"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_template}],
        )

        answer = response.choices[0].message.content

        # prevent GPT from returning 'out of scope' in a complete sentence
        if "out of scope" in answer.lower():
            return "out of scope"
        else:
            return answer
