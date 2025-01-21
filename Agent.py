import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import json
import requests

# Initialize Pinecone
def initialize_pinecone(api_key, environment):
    pc = Pinecone(api_key=api_key)
    index_name = "faq-index"
    if index_name not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=environment)
        )
    return pc.Index(index_name)

# Load FAQ data
def load_faq_data(file_path="faqs.json"):
    with open(file_path, "r") as f:
        faqs = json.load(f)
    
    for faq in faqs:
        if not isinstance(faq, dict) or "question" not in faq or "answer" not in faq:
            raise ValueError("Invalid FAQ format in JSON file.")
    return faqs

# Upload FAQs to Pinecone
def upload_faqs_to_pinecone(index, faqs, model):
    for i, faq in enumerate(faqs):
        embedding = model.encode(faq["question"]).tolist()
        index.upsert([(str(i), embedding, {"answer": faq["answer"]})])

# Search FAQs in Pinecone
def search_faq(index, query, model):
    query_embedding = model.encode(query).tolist()
    results = index.query(
        vector=query_embedding,
        top_k=1,
        include_metadata=True
    )
    return results.matches[0].metadata["answer"] if results.matches else "Sorry, I couldn't find an answer."

# Fetch weather data
def fetch_weather(city):
    api_key = st.secrets["WEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    return "Sorry, I couldn't fetch the weather data."

# Fetch news headlines
def fetch_news():
    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data["articles"][:5]
        return "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles)])
    return "Sorry, I couldn't fetch the news headlines."

# To-Do List Manager
class ToDoListManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        return f"Task '{task}' added."

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f"Task '{task}' removed."
        return f"Task '{task}' not found."

    def view_tasks(self):
        return "\n".join([f"{i+1}. {task}" for i, task in enumerate(self.tasks)]) if self.tasks else "Your to-do list is empty."

# Streamlit Interface
def main():
    st.set_page_config(layout="wide")
    st.title("AI-Agent for Intelligent Task Automation")
    
    # Custom CSS for full-width layout
    st.markdown("""
    <style>
        /* Full-page background image */
        .stApp {
            background-image: url("https://t3.ftcdn.net/jpg/01/83/50/32/360_F_183503230_heDoLySnwt4W968RVTJOf7LFHbkZdCHA.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        
        .block-container {
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem;
            height: 100%;
            max-width: 95%;
        }
        
        /* Column spacing */
        [data-testid="stHorizontalBlock"] > div {
            padding: 0 2rem !important;
        }
        [data-testid="stHorizontalBlock"] > div:first-child {
            padding-left: 0 !important;
        }
        [data-testid="stHorizontalBlock"] > div:last-child {
            padding-right: 0 !important;
        }
        
        /* Text contrast adjustments */
        h1, h2, h3, h4, h5, h6 {
            color: 	#FAF9F6 !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

    # Initialize core components
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
    PINECONE_ENVIRONMENT = st.secrets["PINECONE_ENVIRONMENT"]
    index = initialize_pinecone(PINECONE_API_KEY, PINECONE_ENVIRONMENT)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    faqs = load_faq_data()

    # Create three equal columns
    col1, col2, col3 = st.columns(3)

    # Chatbot Column
    with col1:
        st.header("💬 Chat Support")
        if st.button("📤 Upload FAQs to Pinecone"):
            upload_faqs_to_pinecone(index, faqs, model)
            st.success("Knowledge base updated successfully!")
        
        user_query = st.text_input("Ask your question:", key="chat_input")
        if user_query:
            bot_response = search_faq(index, user_query, model)
            st.text_area("Response:", value=bot_response, height=150, key="chat_response")

    # Weather & News Column
    with col2:
        st.header("🌦️ Weather & News")
        city_input = st.text_input("Enter city name:", key="weather_input")
        if city_input:
            weather_report = fetch_weather(city_input)
            st.success(weather_report)
        
        if st.button("📰 Get Latest Headlines"):
            news_headlines = fetch_news()
            st.text_area("Top News:", value=news_headlines, height=200, key="news_output")

    # Task Manager Column
    with col3:
        st.header("✅ Task Manager")
        if 'todo_manager' not in st.session_state:
            st.session_state.todo_manager = ToDoListManager()
        
        action = st.radio("Select action:", ("Add", "Remove", "View"), 
                        horizontal=True, key="task_action")
        
        # Add Task Section
        if action == "Add":
            task_input = st.text_input("Enter new task:", key="task_input_add")
            if task_input:
                result = st.session_state.todo_manager.add_task(task_input)
                st.success(result)
        
        # Remove Task Section
        elif action == "Remove":
            current_tasks = st.session_state.todo_manager.tasks
            if current_tasks:
                selected_task = st.selectbox(
                    "Select task to remove:",
                    current_tasks,
                    key="task_remove_select"
                )
                if st.button("Confirm Removal"):
                    result = st.session_state.todo_manager.remove_task(selected_task)
                    st.success(result)
                    st.rerun()  # Updated refresh command
            else:
                st.info("No tasks available for removal.")
        
        # View Tasks Section
        elif action == "View":
            task_list = st.session_state.todo_manager.view_tasks()
            st.text_area("Current Tasks:", value=task_list, height=200, key="tasks_output")

if __name__ == "__main__":
    main()