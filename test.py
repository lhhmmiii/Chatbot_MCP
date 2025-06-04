from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI(title="MCP Cloud Server", version="1.0.0")

@app.get("/hello")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Tích hợp MCP
mcp = FastApiMCP(app)
mcp.mount()
