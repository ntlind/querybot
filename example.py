# %%
from querychatbot.querychatbot import QueryChatBot
import sqlalchemy as sqla
import pandas as pd
import json

engine = sqla.create_engine("sqlite:///sales.db", echo=False)


def get_column_descriptions(path="sample_data/column_descriptions.json"):
    with open(path) as jsonfile:
        return json.load(jsonfile)


def initialize_database(engine, path="sample_data/small.csv", table_name="SALES"):
    sales = pd.read_csv(path)
    sales.to_sql(table_name, con=engine, if_exists="replace", index=False)


def query_db(engine, query_text):
    results = engine.execute(query_text)

    df = pd.DataFrame(results.fetchall())
    df.columns = results.keys()
    return df


def get_columns(engine, table_name):
    return sqla.inspect(engine).get_columns(table_name)


def get_metadata():
    return sqla.MetaData(bind=engine)


# %%
questions = [
    "What were the total sales in CA in 2014?",
    "What were the total sales in TX in 2014?",
    "Describe the color black",
]

QueryChatBot(table_schema=get_column_descriptions(), questions=questions)

# %%
