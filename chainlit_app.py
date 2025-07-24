import chainlit as cl
from shopping import agent
from connection import config
from agents import Runner

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hi! I'm your shopping assistant. Ask me to search by category, price, or brand.").send()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content
    result = Runner.run_sync(agent, user_input, run_config=config)
    await cl.Message(content=result.final_output).send()
