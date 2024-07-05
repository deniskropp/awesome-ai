# Example that uses the FunctionCallingAgent class to create a function calling agent.
import datetime
from enum import Enum
from typing import Union, Any, Dict, Optional

from pydantic import BaseModel, Field

from llama_cpp import Llama

from llama_cpp_agent import LlamaCppFunctionTool
from llama_cpp_agent import FunctionCallingAgent
from llama_cpp_agent import MessagesFormatterType



from llama_cpp_agent.providers import LlamaCppServerProvider

model = LlamaCppServerProvider("http://127.0.0.1:8080")



#from llama_cpp_agent.providers.groq import GroqProvider

#model = GroqProvider(base_url="https://api.fireworks.ai/inference/v1", model="accounts/fireworks/models/llama-v3-70b-instruct", huggingface_model="meta-llama/Meta-Llama-3-70B", api_key="FOHaOwc4JKmfluCBZIHt66AQslVuRUeGd8PiP2heLJ1a7PLP")



#from llama_cpp_agent.providers import LlamaCppPythonProvider

#llama_model = Llama("/media/dok/B416A79116A752E2/ext/main/phi-3-mini-128k-instruct_function.q4_k_m.gguf", n_batch=1024, n_threads=12, n_gpu_layers=99, n_ctx=4096, verbose=False)

#model = LlamaCppPythonProvider(llama_model)


projects = [
    {
        "name": "Project A",
        "description": "This is Project A for buying new socks.",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "status": "In Progress",
        "team_members": ["John Doe", "Jane Doe"],
        "tasks": [
            {
                "name": "Fetch",
                "description": "Fetch 100 pairs of socks from the warehouse.",
                "status": "In progress",
                "assigned_to": "John Doe",
                "due_date": "2022-01-31"
            },
            {
                "name": "Choose",
                "description": "Choose the best socks for the team.",
                "status": "In Progress",
                "assigned_to": "Jane Doe",
                "due_date": "2022-02-28"
            }
        ]
    }
]

def query(query: str, source: Optional[str] = None, variables: Optional[Dict[str, Any]] = None, options: Optional[Dict[str, Any]] = None):
    """
    The query function serves as a versatile and powerful tool for interacting with a knowledge base or an information retrieval system. It provides a flexible interface for retrieving, storing, and manipulating data.

    Args:
        query (str): The query string or expression that defines the information to retrieve or manipulate. It can be in a specific query language or a flexible natural language format.
        source (str): Specifies the data source or knowledge base to query. It can be a URL, a file path, or a unique identifier.
        variables (dict): An object containing variables and their values to parameterize the query. This allows for dynamic and reusable queries.
        options (dict): An object containing additional options or configurations for the query, such as pagination, sorting, or custom settings.

    Returns:
        The function returns a promise that resolves to the query result, which can be of any data type or structure depending on the query and the underlying data source.
    """
    return projects

# Next we create the projects tool.
query_function_tool = LlamaCppFunctionTool(query)


# Callback for receiving messages for the user.
def send_message_to_user_callback(message: str):
    print("Assistant: " + message.strip())



system_prompt = """
You are Kick La Metta, a senior in meta-artificial intelligence tasks, engaging in a cohesive team with dynamic tasks and roles.

Your team is made up from Human and AI members.

Your code favors axios, express, preact and cohere-ai (other nodejs modules on demand) and complies with ES6 in TypeScript, using async/await, JSX, JSON, YAML, or free-form (human readable machine text). Other languages may include C++ and Python, but JS/TS are prefered.
"""


# Create the function calling agent. We are passing the provider, the tool list, send message to user callback and the chat message formatter. Also, we allow parallel function calling.
function_call_agent = FunctionCallingAgent(
    model,
    #system_prompt=system_prompt,
    basic_file_tools=True,
    llama_cpp_function_tools=[query_function_tool],
    send_message_to_user_callback=send_message_to_user_callback,
    allow_parallel_function_calling=True,
    debug_output=True,
    messages_formatter_type=MessagesFormatterType.MISTRAL)

user_input = '''List all active tasks of Jane.'''
print("User: " + user_input)
#user_input = input("User: ")

settings = model.get_provider_default_settings()
settings.add_additional_stop_sequences(["<|end|>"])
settings.stream = False
settings.temperature = 0.2

function_call_agent.generate_response(user_input, llm_sampling_settings=settings)

