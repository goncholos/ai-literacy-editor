import json
from openai import OpenAI

from app.config import settings

from app.services.tools.calculator import calculate
from app.services.tools.web_search import search_web
from app.services.tools.file_reader import read_file


client = OpenAI(api_key=settings.openai_api_key)


TOOLS = {
    "calculate": calculate,
    "search_web": search_web,
    "read_file": read_file
}


tool_definitions = [

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string"
                    }
                },
                "required": ["filepath"]
            }
        }
    }

]


def run_agent(task: str):

    messages = [

        {
            "role": "system",
            "content": """
You are an expert literary editor and writing assistant.

Your job is to:
- improve narrative cohesion
- preserve the author's voice
- improve clarity and rhythm
- maintain literary quality
- avoid generic AI writing
- preserve emotional tone
- improve prose naturally

When previous works from the same author are provided,
analyze them carefully and imitate the literary style subtly.

Do NOT overwrite the author's personality.
Enhance it.

Be elegant, nuanced, and literary.
"""
        },

        {
            "role": "user",
            "content": task
        }

    ]

    steps = []

    for _ in range(5):

        try:

            response = client.chat.completions.create(
                model=settings.model_name,
                messages=messages,
                tools=tool_definitions
            )

        except Exception as e:

            print("OPENAI ERROR:")
            print(type(e))
            print(str(e))
            raise

        msg = response.choices[0].message

        # Final response
        if not msg.tool_calls:

            return {
                "result": msg.content,
                "steps": steps
            }

        # IMPORTANT:
        # Add assistant tool call message ONCE
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": msg.tool_calls
        })

        # Execute tools
        for tool_call in msg.tool_calls:

            tool_name = tool_call.function.name

            tool_args = json.loads(
                tool_call.function.arguments
            )

            print(f"\nUSING TOOL: {tool_name}")
            print(f"ARGS: {tool_args}")

            result = TOOLS[tool_name](**tool_args)

            print(f"RESULT:\n{result[:500]}")

            steps.append(
                f"{tool_name}: {result[:200]}"
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return {
        "result": "Max iterations reached",
        "steps": steps
    }