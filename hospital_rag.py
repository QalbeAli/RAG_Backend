from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import TextLoader
from pydantic import BaseModel
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

memory = ConversationBufferWindowMemory(k=5)

try:
    loader = TextLoader("hospitaldata.txt")
except Exception as e:  
    print("Error while loading file=", e)

# Create embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Use a smaller chunk size to manage token limits
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Create the index with the specified embedding model and text splitter
index_creator = VectorstoreIndexCreator(
    embedding=embedding,
    text_splitter=text_splitter
)
index = index_creator.from_loaders([loader])

class QuestionRequest(BaseModel):
    question: str

# Define the chat endpoint

@app.get("/")
def read_hello():
    return {"message": "Hello, World!"}


@app.post("/chat")
async def get_answer(request: QuestionRequest):
    question = request.question
    answer = index.query(question, llm=llm, memory=memory)
    return {"answer": answer}