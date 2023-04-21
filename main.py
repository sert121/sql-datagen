

import openai

def generate_query(question:str, table_name:str, table_columns:list, validate_sql: bool = False,prompt: str = ''):

    if prompt == '':
        prompt = f'''
        -- Language PostgreSQL
        -- Table = {table_name}, columns = {table_columns}
        You are a data analyst with 15 years of experience. You have been given the Table data above. 
        Your role is to come up with questions from the schema provided above. 

        Generate 20 unique prompts based on the table provided to you. 
        '''

    system_text = "you are an experienced data analyst. You find insights from data .You should not ask irrelavant questions to the table."
    chat_query = [{"role":"system", "content": system_text}, {"role":"user", "content": prompt}]
    response = openai.ChatCompletion.create(
        messages=chat_query,
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=' ;'
       )
    # read the chat completion config and generate the required params to be passed to ChatCOmpletion

    generated_query = response["choices"][0]["message"]["content"]
        
    return generated_query
