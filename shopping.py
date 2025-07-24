from agents import Agent, Runner, function_tool
from connection import config
import requests
import chainlit as cl



@function_tool
def get_products_under_budget(budget: float) -> str:
    """
    Returns products under the given budget from Template-03 API.

    Please show the output exactly as returned by the function, line by line.
    """
    url = "https://template-03-api.vercel.app/api/products"
    try:
        response = requests.get(url)
        

        if response.status_code != 200:
            return f"API error: status code {response.status_code}"

        json_data = response.json()
        

        if not json_data.get("success"):
            return "API responded with success = false."

        products = json_data.get("data", [])
        

        if not products:
            return "Not found products"

        filtered = []
        for item in products:
            price = item.get("price", 0)
            name = item.get("productName", "No Name")
            if price <= budget:
                filtered.append(f"{name} - Rs. {price}")

        if not filtered:
            return f"Products not found Under Rs. {budget}"

        # Always return something meaningful
        return "\n".join(filtered[:10])

    except Exception as e:
        return f"Exception occurred: {str(e)}"
    

@function_tool
def get_all_products()-> str:
    """
    Fetch all products from API and return them as a list.

    Please show the output exactly as returned by the function, line by line.
    """
    url = "https://template-03-api.vercel.app/api/products"
    try:
        response = requests.get(url)
        json_data = response.json()

        products = json_data.get("data", [])

        if not products:
            return "Products not found."


        
        result = "\n".join([f"{item['productName']} - Rs. {item['price']}" for item in products])
        return result
    

    
    except Exception as e:
        return f"Error: {str(e)}"
    

@function_tool
def filter_by_category(category: str) -> str:
    """
    Filters products by given category. 
    Allows partial keyword match (e.g., "shoe" will match "shoes", "sneakers", etc.)
    
    Please show the output exactly as returned by the function, line by line.
    """

    url = "https://template-03-api.vercel.app/api/products"
    try:
        response = requests.get(url)
        json_data = response.json()
    
        products = json_data.get("data", [])
    
        if not products:
            return "Products not found."
        
        category_lower = category.lower().strip()

        filtered_products = [
            item for item in products
            if category_lower in item.get("category", "").lower()
        ]

        if not filtered_products:
            return f"No products found in category: {category}"
        
        result_lines = [
            f"- {item['productName']} — Rs. {item['price']}" for item in filtered_products
        ]
        result_text = "\n".join(result_lines)

        return f"🛍️ **Products in category matching '{category}'**\n\n{result_text}"

    except Exception as e:
        return f"Error: {str(e)}"

    
agent = Agent(
    name = "Shopping Agent",
    instructions=""" You are a smart shopping agent. 
Answer based on user's budget or product category.

When calling a tool, show the result **exactly as returned** by the function, **line by line**, without summarizing or modifying it.
Do not reword or reformat the response. Just show it as-is.
Always return tool outputs exactly as they are, line-by-line, no rephrasing.

""",
    tools=[get_products_under_budget, get_all_products, filter_by_category],
    
) 


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hi! I'm your shopping assistant. Ask me to search by category, price, or brand.").send()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content
    result = Runner.run_sync(agent, user_input, run_config=config)
    await cl.Message(content=result.final_output).send()


