from fastapi_mcp import FastApiMCP
from routers import metadata_router
from fastapi import FastAPI
import uvicorn


app = FastAPI(title="MCP Cloud Server", version="1.0.0")

app.include_router(metadata_router)

# Tích hợp MCP
mcp = FastApiMCP(app)
mcp.mount()
