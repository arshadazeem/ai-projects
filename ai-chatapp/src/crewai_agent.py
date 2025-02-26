import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
import openai

# Load variables from .env file
load_dotenv()

# Set up Azure OpenAI credentials
openai.api_type = os.getenv("OPEN_AI_API_TYPE")  
AZURE_OPENAI_ENDPOINT = os.getenv("OPEN_AI_API_ENDPOINT_CHAT") 
AZURE_OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY_CHAT")
AZURE_OPENAI_API_VERSION = os.getenv("OPEN_AI_API_VERSION_CHAT") 

# set environment as LiteLLM expects
os.environ['AZURE_API_KEY'] = AZURE_OPENAI_API_KEY
os.environ["AZURE_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["AZURE_API_VERSION"] = AZURE_OPENAI_API_VERSION


AZURE_OPENAI_DEPLOYMENT = "gpt-4o"

# Define the Client Agent
client = Agent(
    name="Client",
    role="Investor",
    goal="Find high-return investment options within a 1-year timeframe.",
    backstory="A motivated investor with $100,000, aiming for higher returns than the S&P 500 while maintaining diversification.",
    verbose=True,
    llm=LLM(model='azure/gpt-4o')
)

# Define the Advisor Agent
advisor = Agent(
    name="Financial Advisor",
    role="Investment Expert",
    goal="Provide multiple short-term investment strategies that balance risk and returns.",
    backstory="An experienced financial strategist focused on short-term market trends, sector rotations, and high-yield opportunities.",
    verbose=True,
    llm=LLM(model='azure/gpt-4o')
)

# Define Tasks
client_request_task = Task(
    description="Specify investment preferences: $100,000 capital, a 1-year timeframe, and a goal to outperform the S&P 500 with a diversified approach.",
    agent=client,
    expected_output="A detailed investment preference summary, including risk tolerance, diversification goals, and expected returns."
)

advisor_response_task = Task(
    description="Analyze market trends and recommend at least three investment strategies optimized for short-term (1-year) growth, considering high-yield stocks, sector rotations, ETFs, and alternative assets.",
    agent=advisor,
    expected_output="Three investment strategies with asset allocation details, expected risk levels, and projected returns."
)

# Create the Crew and Assign Tasks
financial_crew = Crew(
    agents=[client, advisor],
    tasks=[client_request_task, advisor_response_task],
    verbose=True
)

# Execute the Crew's Workflow
investment_options = financial_crew.kickoff()
print("\nShort-Term Investment Strategies Suggested:\n", investment_options)
