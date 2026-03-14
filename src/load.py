import pandas as pd
from sqlalchemy import Engine

def load_df_to_table(df: pd.DataFrame, engine: Engine, table_name: str, schema_name: str = "public") -> None:
    df.to_sql(table_name, engine, schema=schema_name, if_exists="append", index=False)