import os
import certifi
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub

from langchain.agents import create_react_agent, AgentExecutor

# Load environment variables from .env file
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

search_tool = TavilySearchResults(max_results=2)

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=OPENAI_API_KEY
)

# Prompt
prompt = hub.pull("hwchase17/react")

# Tool
tools = [search_tool]

# Create the agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

response = agent_executor.invoke({
    "input": (
        "what is the price of new latest apple iphone 18 pro max in sri lanka"
    )
})

print(response["output"])
