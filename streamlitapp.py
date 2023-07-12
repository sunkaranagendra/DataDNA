import streamlit as st
import pandas as pd
from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from pathlib import Path
import os

os.environ["OPENAI_API_KEY"] = "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"


def save_uploaded_file(db_file):
  temp_dir = Path("Temp")
  temp_dir.mkdir(exist_ok=True)
  file_path = temp_dir / db_file.name
  with open(file_path, "wb") as f:
    f.write(db_file.getbuffer())
  return str(file_path)

def create_db_uri(file_path):
  db_uri = f"sqlite:///{file_path}"
  return db_uri

def get_URI():
  db_file = st.file_uploader("Upload your db", type=".db")
  if db_file is not None:
    file_path = save_uploaded_file(db_file)
    db_uri = create_db_uri(file_path)
    return db_uri

def main():
    st.title("Data DNA Insights")
    st.header("Chat with csv by Pune Panthers")
    data_source=st.slidebar.selectbox("Data Source",["CSV","Database"])
    if data_source == "CSV":
      uploaded_file=st.sidebar.file_uploader("Upload CSV file",type="csv")
      user_question = st.text_input("Put your questions here: ")
      if uploaded_file is not None and user_question is not None and user_question != "":
        with st.spinner(text="In Progress..."):
          df=pd.read_csv(uploaded_file)
          agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=False)
          st.write(agent.run(user_question))
    
    elif data_source== "Database":
        URI = get_URI()
        if URI is not None:
            db = SQLDatabase.from_uri(URI)
            toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
            agent_executor = create_sql_agent(llm=OpenAI(temperature=0),toolkit=toolkit,verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
        
        user_question = st.text_input("Put your questions here: ")
        if user_question is not None and user_question != "":
            with st.spinner(text="In Progress..."):
                st.write(agent_db.run(user_question))
        # db_host=st.sidebar.text_input("Database Host")
        # db_user=st.sidebar.text_input("Database User")
        # db_password=st.sidebar.text_input("Database Password")
        # db_name=st.sidebar.text_input("Database Name")
        # processed_data=langchain.process_from_db(host=db_host,user=db_user,password=db_password,db=db_name)
        # st.write(processed_data)
        
if __name__=="__main__":
    main()
