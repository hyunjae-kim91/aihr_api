import pandas as pd
from typing import List, Union
import sqlalchemy
from sqlalchemy import text
from .db_connector import DBConnector
from .db_connector import session, dbConnector

def bulk_insert(df: pd.DataFrame, schema: str, table_name: str):
    df = df.drop_duplicates()
    dbConnector = DBConnector()
    try:
        df.to_sql(
            name=table_name,
            schema=schema,
            con=dbConnector.engine,
            index=False,
            if_exists='append',
            chunksize=10000,
            method='multi'
        )
    except sqlalchemy.exc.SQLAlchemyError as sQLAlchemyError:
        raise Exception(str(sQLAlchemyError)[:2000])
    except Exception as e:
        raise Exception(str(e)[:2000])

def execute_batch_sql(query: str) -> None:
    """batch sql파일에서 읽어온 쿼리를 실핼합니다."""
    session = DBConnector().create_session()
    try:
        all_data = session.execute(text(query))
        all_data = all_data.all()
        for data in all_data:
            yield data._asdict()
    except sqlalchemy.exc.SQLAlchemyError as sQLAlchemyError:
        raise Exception(sQLAlchemyError)
    except Exception as e:
        raise Exception(e)
    finally:
        session.close()
        DBConnector().engine.dispose()
