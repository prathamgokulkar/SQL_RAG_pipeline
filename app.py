import streamlit as st
import os
import sqlite3
from sqlalchemy.exc import SQLAlchemyError
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def setup_database_connection(db_type, **kwargs):
    
    try:
        if db_type == "SQLite":
            file_path = kwargs.get("file_path")
            if not file_path:
                st.error("SQLite file path is required.")
                return None, None
            uri = f"sqlite:///{file_path}"
            db_name = f"Your SQLite DB: {os.path.basename(file_path)}"

        elif db_type == "MySQL":
            uri = f"mysql+mysqlconnector://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}/{kwargs['database']}"
            db_name = f"{kwargs['database']} (MySQL)"
        else:
            st.error("Unsupported database type")
            return None, None

        db = SQLDatabase.from_uri(uri)
        return db, db_name
    except SQLAlchemyError as e:
        st.sidebar.error(f"DB Connection Error: {e}")
        return None, None
    except Exception as e:
        st.sidebar.error(f"Unexpected error: {e}")
        return None, None

def create_sql_agent_executor(db):
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY, temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True},
        prefix="You are an agent designed to interact with a SQL database. "
               "Given an input question, create a syntactically correct SQL query, "
               "run it, and return the answer. Use 'sql_db_schema' tool to see the schema."
    )
    return agent_executor

st.set_page_config(page_title="Chat with SQL Database", layout="wide")
st.title("Chat with Your SQL Database")

if "agent_executor" not in st.session_state: st.session_state.agent_executor = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "db_name" not in st.session_state: st.session_state.db_name = None


with st.sidebar:
    st.header("Database Connection")
    db_type = st.radio("Select Database Type", ("SQLite", "MySQL"))

    if db_type == "SQLite":
        uploaded_db = st.file_uploader("Upload your SQLite database", type=["db"])
        if uploaded_db:
            if st.button("Connect to SQLite", key="connect_sqlite"):
                temp_db_path = f"temp_{uploaded_db.name}"
                with open(temp_db_path, "wb") as f:
                    f.write(uploaded_db.getbuffer())
                with st.spinner("Connecting to SQLite..."):
                    db, db_name = setup_database_connection("SQLite", file_path=temp_db_path)
                    if db:
                        st.session_state.agent_executor = create_sql_agent_executor(db)
                        st.session_state.db_name = db_name
                        st.session_state.chat_history = [
                            AIMessage(content=f"Hello! I'm connected to {db_name}. How can I help you?")
                        ]
                        st.success(f"Connected to {db_name}!")

    elif db_type == "MySQL":
        host = st.text_input("Host", value="localhost")
        user = st.text_input("User", value="root")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database")
        if st.button("Connect to MySQL", key="connect_mysql"):
            if not all([host, user, database]):
                st.warning("Please fill in all MySQL connection details.")
            else:
                with st.spinner("Connecting to MySQL..."):
                    db, db_name = setup_database_connection(
                        "MySQL", host=host, user=user, password=password, database=database
                    )
                    if db:
                        st.session_state.agent_executor = create_sql_agent_executor(db)
                        st.session_state.db_name = db_name
                        st.session_state.chat_history = [
                            AIMessage(content=f"Hello! I'm connected to {db_name}. How can I help you?")
                        ]
                        st.success(f"Connected to {db_name}!")


if st.session_state.agent_executor:
    st.info(f"Currently connected to: **{st.session_state.db_name}**")

    for message in st.session_state.chat_history:
        role = "AI" if isinstance(message, AIMessage) else "Human"
        with st.chat_message(role):
            st.write(message.content)

    user_query = st.chat_input(f"Ask a question about {st.session_state.db_name}...")
    if user_query:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("Human"):
            st.write(user_query)
        with st.chat_message("AI"):
            with st.spinner("Thinking and querying the database..."):
                response = st.session_state.agent_executor.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.chat_history
                })
                st.write(response['output'])
                st.session_state.chat_history.append(AIMessage(content=response['output']))
else:
    st.info("Please connect to a database using the sidebar to begin.")
