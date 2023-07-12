import streamlit as st
import pandas as pd
import Langchain

langchain=Langchain()
def main():
    st.title("Data DNA Insights")
    data_source=st.slidebar.selectbox("Data Source",["CSV","Database"])
    if data_source == "CSV":
        uploaded_file=st.sidebar.file_uploader("Upload CSV file",type="csv")
        if uploaded_file is not None:
            df=pd.read_csv(uploaded_file)
            processed_data=langchain.process(df)
            st.write(processed_data)
    elif data_source== "Database":
        db_host=st.sidebar.text_input("Database Host")
        db_user=st.sidebar.text_input("Database User")
        db_password=st.sidebar.text_input("Database Password")
        db_name=st.sidebar.text_input("Database Name")
        processed_data=langchain.process_from_db(host=db_host,user=db_user,password=db_password,db=db_name)
        st.write(processed_data)
        
if __name__=="__main__":
    main()
