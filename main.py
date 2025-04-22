from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import pswd
from pswd import OPENAI_API_KEY
import pyaudio
import voice_input


load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
#llm = ChatAnthropic(model="Claude-3-5-sonnet-20241022")

#The fields you want to have in the model

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

#prompt 
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, save_tool]  # Add your tools here
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools

)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  #Verbose is thought process of the Agent

print("Welcome to the research assistant! How would you like to provide your query? ")
print("1. Type your query")
print("2. Use voice input")
choice = input("Enter 1 or 2: ")
if choice == "1":
    query = input("What can I help you research? ")
if choice == "2":
    query = voice_input.listen_to_command()
    if query:
        print(f"Command received: {query}")
    else:
        print("No command received.")

# Execute the agent with the provided query
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e)
    print("Raw response:", raw_response)
