from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes
import uvicorn

load_dotenv()

#setup the keys
#langSmith projectkey
os.environ["LANGCHAIN_PROJECT"]= "Deployment demo langserve"

#groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

#define the model
model = ChatGroq(groq_api_key=groq_api_key, model= "openai/gpt-oss-120b")

#define the prompt
prompt_template = ChatPromptTemplate.from_messages(
    [("system", "Translate the following into {language}:"),
    ("user", "{text}")]
)

#define the output parser
parser = StrOutputParser()

#Now create a chain with 3 of them 
chain = prompt_template|model|parser

#app definition
app = FastAPI(title="LangChain Server",
              version="1.0",
              description="A simple API server using langchain runnable interfaces")

#adding chain routes
add_routes(
    app=app,
    runnable=chain,
    path="/chain"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)