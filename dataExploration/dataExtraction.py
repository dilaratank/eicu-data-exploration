import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine

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

def extract_csv(saveto, variablestring, table, joinon='patientUnitStayID'):
    
    table_split = table.split(',')

    if len(table_split)== 1:
        query = f"\\COPY (SELECT {variablestring} FROM {table}) TO {saveto} WITH CSV HEADER;"
        os.system(f'psql eicu -c "{query}"')
    
    elif len(table_split)== 2:

        join1 = table_split[0]+f".{joinon}"
        join2 = table_split[1]+f".{joinon}"

        query = f"\\COPY (SELECT {variablestring} FROM {table_split[0]} INNER JOIN {table_split[1]} ON {join1}={join2}) TO {saveto} WITH CSV HEADER;"
        os.system(f'psql eicu -c "{query}"')

    else:
        print('wrong number of tables entered')

    print('data extracted')

def get_df(variablestring, table):

    table_split = table.split(',')
    # connection = create_engine('postgresql+psycopg2://dtank:@localhost/eicu')
    connection = psycopg2.connect(user="dtank", database="eicu")

    if len(table_split) == 1:
        query = f"SELECT {variablestring} FROM {table}"
    
    elif len(table_split) == 2:

        join1 = table_split[0]+".patientUnitStayID"
        join2 = table_split[1]+".patientUnitStayID"

        query = f"SELECT {variablestring} FROM {table_split[0]} INNER JOIN {table_split[1]} ON {join1}={join2};"

    df = pd.read_sql(query, con=connection)   

    return df