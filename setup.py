import sqlalchemy as sqla
import pandas as pd

# TODO use proper setup.py template


def get_engine(name="sales"):
    """Create a new SQLite3 database"""
    return sqla.create_engine(f"sqlite:///{name}.db", echo=False)


def initialize_database(engine, path="sample_data/small.csv", table_name="SALES"):
    """Load the small.csv example data into your database engine"""
    sales = pd.read_csv(path)
    sales.to_sql(table_name, con=engine, if_exists="replace", index=False)


if __name__ == "__main__":
    engine = get_engine("sales")
    initialize_database(engine, path="sample_data/small.csv", table_name="SALES")
