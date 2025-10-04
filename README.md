# SQL RAG Chatbot with Streamlit

##  Overview

This application enables users to interact with SQL databases through natural language queries. By leveraging Retrieval-Augmented Generation (RAG) and LangChain, the app converts user input into SQL queries, executes them, and returns the results in a conversational format.

🔗 **Live Demo:** [sql-rag-pratham.streamlit.app](https://sql-rag-pratham.streamlit.app/)

---

##  Features

- **Natural Language to SQL**: Transform user questions into SQL queries.
- **Database Agnostic**: Supports SQLite and MySQL databases.
- **Schema Awareness**: Utilizes RAG to understand and query database schemas effectively.
- **Secure API Integration**: Connects to Groq's LLM API for query generation.
- **User-Friendly Interface**: Built with Streamlit for an intuitive chat experience.

---

##  Setup Instructions

###  Requirements

- Python 3.8 or higher
- Streamlit
- LangChain
- SQLAlchemy
- SQLite or MySQL
- Groq API Key

###  Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/sql-rag-pratham.git
   cd sql-rag-pratham
   ```
Install Dependencies:

```bash
Copy code
pip install -r requirements.txt
```
Set Up Environment Variables:

Create a .env file in the project root.

Add your Groq API key:

```ini
GROQ_API_KEY=your_groq_api_key
```
Run the Application:

```bash
Copy code
streamlit run app.py
```

## Usage

1. **Connect to a Database**  
   - Select **SQLite** or **MySQL**.  
   - For **SQLite**, upload your `.db` file.  
   - For **MySQL**, enter the connection details (host, user, password, database).  

2. **Ask Questions**  
   - Type your query in natural language.  
   - The app will generate and execute the SQL query.  
   - View the results directly in the chat interface.  
