from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.agents import initialize_agent 
from tools import open_file_tool, say_hello_tool
from pytorch_model import run_dummy_model
from dotenv import load_dotenv
load_dotenv()


def setup_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)  # Requires your OpenAI API key to be set
    tools = [
        Tool(name="Create File", func=open_file_tool, description="Creates a file"),
        Tool(name="Say Hello", func=say_hello_tool, description="Greets someone"),
        Tool(name="Run PyTorch", func=run_dummy_model, description="Runs a dummy PyTorch calc"),
    ]
    return initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
