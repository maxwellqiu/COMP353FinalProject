from sqlalchemy import create_engine, text
import pandas as pd


class MysqlCtrl:

    def __init__(self, user, password, host, port, database_name):
        self.engine = create_engine(
            f"mysql://{user}:{password}@{host}:{port}/{database_name}")

    def execute(self, sql_stmt) -> bool:
        try:
            with self.engine.connect() as connection:
                connection.execution_options(isolation_level="AUTOCOMMIT")
                connection.execute(text(sql_stmt))
            return True
        except Exception as e:
            return False

    def query(self, sql_stmt):
        with self.engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            result = connection.execute(text(sql_stmt))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
