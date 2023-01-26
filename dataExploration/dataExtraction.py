import psycopg2
import os

def get_query_result(user, database, query):
    connection = psycopg2.connect(user=user,
                                  database=database)

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Executing a SQL query
    cursor.execute(query)

    # Fetch result
    query_result = cursor.fetchall()

    return query_result

def extract_csv(saveto, variablestring, table):
    query = f"\COPY (SELECT {variablestring} FROM {table}) TO {saveto} WITH CSV HEADER;"
    os.system(f'psql eicu -c "{query}"')

    print('data extracted')

    