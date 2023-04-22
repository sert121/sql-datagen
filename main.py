import openai
import yaml
from pprint import pprint
import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
import random
from helpers import get_db_schema
from helpers import extract_granular, disallowed_tables

from dotenv import load_dotenv
import os
import random



import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def generate_query(question:str, table_name:str, table_columns:list, validate_sql: bool = False,prompt: str = ''):

    if prompt == '':
        prompt = f'''
        -- Language PostgreSQL
        -- Table = {table_name}, columns = {table_columns}
        You are a github representative who has been given a table about github daily commits.  You have been given the Table data above. 
        Your role is to come up with questions for github that shall be useful in decion-making. 

        Generate 20 interesting questions. Don't ask questions about minimum, maximum, etc. 
        '''

    system_text = "you are an experienced data analyst. You find insights from data "
    chat_query = [{"role":"system", "content": system_text}, {"role":"user", "content": prompt}]
    response = openai.ChatCompletion.create(
        messages=chat_query,
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=' ;'
       )
    # read the chat completion config and generate the required params to be passed to ChatCOmpletion

    generated_query = response["choices"][0]["message"]["content"]
        
    return generated_query


# generate if main function
if __name__ == '__main__':
    # load db via psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # list_tables = extract_table_data(cur,DB_NAME)
    list_tables = extract_granular(cur, DATABASE_URL)

    table_names = [t['table_name'] for t in list_tables if t['table_name'] not in disallowed_tables ]

    selected_name = 'github_repositorycontributorweeklycommitstatistics'

    selected_table = list_tables[table_names.index(selected_name)]

    s_table_name = selected_table['table_name']
    s_table_columns = selected_table['table_columns']

    generated_query = generate_query(question = '',table_name=s_table_name,table_columns = s_table_columns)

    print(generated_query)



    

