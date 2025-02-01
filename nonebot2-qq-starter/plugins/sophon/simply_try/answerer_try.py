#%%
from openai import OpenAI
client = OpenAI(
    api_key='EMPTY',
    base_url='http://localhost:8000/v1',
)
model_type = client.models.list().data[0].id
print(f'model_type: {model_type}')
#%%
query = 'who are you?'
messages = [{
    'role': 'user',
    'content': query
}]
resp = client.chat.completions.create(
    model=model_type,
    messages=messages,
    images= [], 
    seed=42)
response = resp.choices[0].message.content
print(f'query: {query}')
print(f'response: {response}')
# %%

query = "What's the weather like in Boston today?"
messages = [{
    'role': 'user',
    'content': query
}]
tools =  [
      {
        "name": "url_for_newapi",
        "description": "This is the subfunction for tool \"newapi\", you can use this tool.The description of this function is: \"url_for_newapi\"",
        "parameters": {
          "type": "object",
          "properties": {
            "url": {
              "type": "string",
              "description": "",
              "example_value": "https://www.instagram.com/reels/CtB6vWMMHFD/"
            }
          },
          "required": [
            "url"
          ],
          "optional": [
            "url"
          ]
        }
      },
]
resp = client.chat.completions.create(
    model='llama3-8b-instruct',
    tools = tools,
    messages=messages,
    seed=42)
tool_calls = resp.choices[0].message.tool_calls
print(f'query: {query}')
print(f'tool_calls: {tool_calls}')

# stream
stream_resp = client.chat.completions.create(
    model='llama3-8b-instruct',
    messages=messages,
    tools=tools,
    stream=True,
    seed=42)

print(f'query: {query}')
print('response: ', end='')
for chunk in stream_resp:
    print(chunk.choices[0].delta.content, end='', flush=True)
print()

"""
query: What's the weather like in Boston today?
tool_calls: {'id': 'toolcall-e4c637435e754cf9b2034c3e6861a4ad', 'function': {'arguments': ' {"url": "https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=Boston"}', 'name': 'url_for_newapi'}, 'type': 'function'}
query: What's the weather like in Boston today?
response: Thought: I need to find the weather information for Boston today. I can use the 'newapi' tool to get the weather forecast.
Action: url_for_newapi
Action Input: {"url": "https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=Boston"}
"""