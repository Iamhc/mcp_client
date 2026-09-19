from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
servers={
     "expense-tracker": {
       "transport":"stdio",
      "command": "C:\\Program Files\\Python312\\python.exe",
      "args": [
        "C:\\Users\\Prashant\\Desktop\\MCP_FILES\\MCP_SERVER\\src\\mcp_server\\__init__.py"
      ],
      "env": {
        "MONGO_URI": os.getenv("MONGO_URI")
      }
    },
      "manim-server": {
         "transport":"stdio",
      "command": "C:\\Program Files\\Python312\\python.exe",
      "args": [
        "C:/Users/Prashant/Desktop/manim-mcp-server/src/manim_server.py"
      ]
    }
}
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

client= MultiServerMCPClient(servers)

async def main():
  
   tools=await client.get_tools()
   
   llm_with_tools = llm.bind_tools(tools, tool_choice="any")
   response=await llm_with_tools.ainvoke("is manim tool accesible??")
   if response.tool_calls:
      for tool_calls in response.tool_calls:
         tool_name=tool_calls["name"]
         tool_args=tool_calls["args"]

         selected_tool= next((t for t in tools if t.name==tool_name),None)
         if selected_tool:
            result=await selected_tool.ainvoke(tool_args)
            print(result)

asyncio.run(main())

