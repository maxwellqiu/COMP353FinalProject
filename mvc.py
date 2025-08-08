from mysqlCtrl import MysqlCtrl
from CONSTANTS import user, password, host, port, database_name, tables_constrains


def format_value(value, table_name, col_name):
    col_type, col_constraint = tables_constrains[table_name][col_name]
    if value is None or value in ('', 'None'):
        return "NULL"
    if col_type == 'KEY':
        pass
    elif col_type == 'VARCHAR':
        if isinstance(col_constraint, int):
            return f"'{value[:col_constraint]}'"
        else:
            return f"'{value}'"
    elif col_type in ('DATE', 'DATETIME'):
        return f"'{value}'"
    elif col_type == 'INT':
        return int(value)
    elif col_type == 'DECIMAL':
        return float(value)
    else:
        raise


class MVC:
    sqlctrl = MysqlCtrl(user, password, host, port, database_name)

    def table_columns(self, table_name: str):
        """Return columns metadata for a table in display order."""
        q = f"""
            SELECT COLUMN_NAME as name,
                   DATA_TYPE as data_type,
                   IS_NULLABLE as is_nullable,
                   COLUMN_KEY as column_key,
                   COLUMN_DEFAULT as col_default,
                   EXTRA as extra,
                   ORDINAL_POSITION as ordinal_position
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION;
        """
        return self.sqlctrl.query(q)

    def primary_key_one(self, table_name: str):
        q = f"""
            SELECT COLUMN_NAME as name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_NAME = '{table_name}'
              AND COLUMN_KEY = 'PRI'
            ORDER BY ORDINAL_POSITION
            LIMIT 1;
        """
        df = self.sqlctrl.query(q)
        return None if df.empty else df.iloc[0]["name"]

    def select_all(self, table_name: str):
        return self.sqlctrl.query(f"SELECT * FROM {table_name};")

    def select_by_one_pk(self, table_name: str, pk_col: str, pk_value):
        q = f"SELECT * FROM {table_name} WHERE {pk_col} = {int(pk_value)};"
        return self.sqlctrl.query(q)

    def insert_row(self, table_name: str, data: dict):
        cols = ", ".join(data.keys())
        vals = ", ".join([
            f"{format_value(v, table_name, k)}" if v is not None else "NULL"
            for k, v in data.items()
        ])
        q = f"INSERT INTO {table_name} ({cols}) VALUES ({vals});"
        print(f"==>> q: {q}")
        return self.sqlctrl.execute(q)

    def update_row(self, table_name: str, pk_col: str, pk_value, data: dict):
        sets = ", ".join([
            f"{k} = {format_value(v, table_name, k)}"
            if v is not None else f"{k} = NULL" for k, v in data.items()
        ])
        q = f"UPDATE {table_name} SET {sets} WHERE {pk_col} = {int(pk_value)};"
        return self.sqlctrl.execute(q)

    def delete_row(self, table_name: str, pk_col: str, pk_value):
        q = f"DELETE FROM {table_name} WHERE {pk_col} = {int(pk_value)};"
        return self.sqlctrl.execute(q)

    def next_id(self, table_name: str, pk_col: str):
        q = f"SELECT COALESCE(MAX({pk_col}), 0) + 1 AS next_id FROM {table_name};"
        df = self.sqlctrl.query(q)
        return int(df.iloc[0]["next_id"]) if not df.empty else 1

    def get_next_installment_id(self, memberID, membershipYear):
        q = f"""
        SELECT
        count(*) + 1 AS next_id
        FROM MakePayment AS mp
        JOIN Payment AS p
        ON p.paymentID = mp.paymentID
        WHERE mp.memberID = {memberID}
        AND p.membershipYear = {membershipYear}
        ORDER BY mp.installmentNumber;
        """
        df = self.sqlctrl.query(q)
        return int(df.iloc[0]["next_id"]) if not df.empty else 1

    def get_schedule(self, curSunday):
        q = f"""
        WITH params AS (
        SELECT DATE('{curSunday}') AS today,
                DATE_ADD(DATE('{curSunday}'), INTERVAL 1 DAY) AS week_start
        ),
        coaches AS (
        SELECT
            cb.sessionID,
            cb.teamNumber,
            p.firstName,
            p.lastName,
            p.email,
            ROW_NUMBER() OVER (
            PARTITION BY cb.sessionID, cb.teamNumber
            ORDER BY p.personnelID
            ) AS rn
        FROM CoachedBy cb
        JOIN Personnel p
            ON p.personnelID = cb.personnelID
        AND p.role = 'Coach'
        )
        SELECT
        tf.sessionID,
        DATE(tf.dateTime) AS sessionDate,
        TIME(tf.dateTime) AS sessionTime,
        tf.sessionType,
        tf.address,
        cm.memberID,
        cm.firstName   AS memberFirstName,
        cm.lastName    AS memberLastName,
        cm.email AS clubmemberEmail,
        pi.playerRole,
        CONCAT(c.firstName, ' ', c.lastName) AS headCoach,
        c.email        AS headCoachEmail
        FROM TeamFormation AS tf
        JOIN PlaysIn AS pi
        ON pi.sessionID = tf.sessionID
        JOIN ClubMember AS cm
        ON cm.memberID = pi.memberID
        LEFT JOIN coaches AS c
        ON c.sessionID = tf.sessionID
        AND c.teamNumber = pi.teamNumber
        AND c.rn = 1
        CROSS JOIN params
        WHERE tf.dateTime >= params.week_start
        AND tf.dateTime <  DATE_ADD(params.week_start, INTERVAL 7 DAY)
        ORDER BY tf.dateTime, pi.teamNumber, cm.lastName, cm.firstName;
        """
        return self.sqlctrl.query(q)


if __name__ == "__main__":
    mvc = MVC()
    print(mvc.table_columns('Personnel'))
