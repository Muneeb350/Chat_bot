from typing import Callable

# Dummy function decorator
def function_tool(func: Callable) -> Callable:
    return func

# Dummy Agent class
class Agent:
    def __init__(self, tools=None, llm=None):
        self.tools = tools
        self.llm = llm

    async def run(self, input_str: str) -> str:
        return f"Received input: {input_str}"

# Dummy Runner class
class Runner:
    def __init__(self, agent: Agent):
        self.agent = agent

    async def run(self, input_str: str) -> str:
        return await self.agent.run(input_str)
