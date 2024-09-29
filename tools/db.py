from sqlalchemy.orm.session import Session
from sqlalchemy import text


def reset_sequence(table_name: str, db: Session) -> None:
    """
    Resets the auto-increment sequence of the primary key column in a specified table
    to match the maximum current value of the primary key.

    This is particularly useful after deleting rows from a table, as it ensures that
    newly inserted rows will continue with the next available primary key value instead
    of reusing the deleted ones. This function is designed for PostgreSQL databases where
    sequences control the auto-incrementing of primary keys.

    Args:
        table_name (str): The name of the table for which to reset the sequence.
        db (Session): The SQLAlchemy session used to execute the SQL command.

    Example:
        reset_sequence('users', db)
        # Resets the sequence for the 'id' column in the 'users' table.
    """

    sequence_name = f"{table_name}_id_seq"

    db.execute(text(f"SELECT setval('{sequence_name}', (SELECT MAX(id) FROM {table_name}))"))
    db.commit()
