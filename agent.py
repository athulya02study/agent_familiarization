import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["GROQ_API_KEY"],
                base_url="https://api.groq.com/openai/v1")

def add(a: float, b: float):
    return str(a + b)

tools = [{"type": "function", "function": {
    "name": "add",
    "description": "Add two numbers",
    "parameters": {"type": "object",
                   "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                   "required": ["a", "b"]}}}]

goal = input("Ask something: ")          # user input
messages = [{"role": "user", "content": goal}]

while True:
    msg = client.chat.completions.create(
        model="openai/gpt-oss-120b", messages=messages, tools=tools
    ).choices[0].message
    messages.append(msg)

    if not msg.tool_calls:               # no tool needed, so this is the final answer
        print(msg.content)
        break

    for call in msg.tool_calls:          # run the tool and give the result back
        result = add(**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})