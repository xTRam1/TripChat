import os
from abc import ABC
from typing import TypedDict, Unpack

from langchain.agents import initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool


class LangchainConstants:
    AGENT = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
    MAX_ITERATIONS = 3
    VERBOSE = True
    EARLY_STOPPING_METHOD = "generate"
    MEMORY = {"memory_key": "chat_history", "k": 2, "return_messages": True}


class LangchainAgentInitParams(TypedDict):
    name: str
    model: str
    tools: list[BaseTool | Tool | StructuredTool]


class LangchainAgent(ABC):
    # Initialization parameters
    name: str
    model: str
    tools: list[BaseTool | Tool | StructuredTool]

    # Private Fields - Calculated
    llm: ChatOpenAI
    conversation_memory: ConversationBufferWindowMemory
    agent: AgentExecutor

    # Constants for AutogenAgents
    _DESCRIPTION: str = (
        "This agent is a chatbot that can be used to talk about anything."
    )
    _MESSAGE_DESCRIPTION: str = "The message or query to send to the agent."

    # Needs to take model_name,
    def __init__(self, **kwargs: Unpack[LangchainAgentInitParams]) -> None:
        # Init Parameters
        self.name = kwargs["name"]
        self.model = kwargs["model"]
        self.tools = kwargs["tools"]

        # Calculated fields
        self.llm = ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=0,
            model_name=self.model,  # type: ignore
        )
        self.conversation_memory = ConversationBufferWindowMemory(
            **LangchainConstants.MEMORY
        )
        self.agent = initialize_agent(
            agent=LangchainConstants.AGENT,
            llm=self.llm,
            tools=self.tools,
            verbose=LangchainConstants.VERBOSE,
            max_iterations=LangchainConstants.MAX_ITERATIONS,
            early_stopping_method=LangchainConstants.EARLY_STOPPING_METHOD,
            memory=self.conversation_memory,
        )

    def ask_agent(self, message: str) -> str:
        agent_response = self.agent(message)
        return agent_response["output"]
