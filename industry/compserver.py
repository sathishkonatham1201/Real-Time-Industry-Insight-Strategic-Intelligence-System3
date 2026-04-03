import os
from dotenv import load_dotenv
load_dotenv()
serp = os.getenv("SERP_API_KEY")

from fastmcp import FastMCP
from serpapi import GoogleSearch
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading

mcp = FastMCP("Brand Comparison Server")

# ── helper function (renamed to avoid conflict) ──
def fetch_brand_data(brand_name: str) -> list:
    params = {
        "engine": "google_shopping",
        "q": f"{brand_name} shoes",
        "api_key": serp,
        "num": 3
    }
    search = GoogleSearch(params)
    results = search.get_dict().get("shopping_results", [])
    return [
        {"title": r.get("title"), "price": r.get("price"), "rating": r.get("rating")}
        for r in results
    ]

# ── MCP tool (named get_brand_data so client can call it) ──
@mcp.tool()
def get_brand_data(brand_name: str, product_type: str = "shoes") -> list:
    return fetch_brand_data(brand_name)

# ── FastAPI dashboard server on port 8002 ──
api = FastAPI()
api.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@api.get("/")
def home():
    return FileResponse("brand_dashboard(1).html")

@api.get("/brands/{brand_name}")
def get_brand(brand_name: str):
    return JSONResponse(content=fetch_brand_data(brand_name))  # ← uses helper

def run_api():
    uvicorn.run(api, host="127.0.0.1", port=8002, log_level="warning")

if __name__ == "__main__":
    t = threading.Thread(target=run_api, daemon=True)
    t.start()
    print("✅ Dashboard running at http://127.0.0.1:8002")
    mcp.run(transport="sse", host="127.0.0.1", port=8001)
# import os
# from dotenv import load_dotenv
# load_dotenv()
# serp = os.getenv("SERP_API_KEY")

# from fastmcp import FastMCP
# from serpapi import GoogleSearch
# from fastapi import FastAPI
# from fastapi.responses import JSONResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import asyncio

# mcp = FastMCP("Brand Comparison Server")

# def fetch_brand_data(brand_name: str) -> list:
#     params = {
#         "engine": "google_shopping",
#         "q": f"{brand_name} shoes",
#         "api_key": serp,
#         "num": 3
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict().get("shopping_results", [])
#     return [
#         {"title": r.get("title"), "price": r.get("price"), "rating": r.get("rating")}
#         for r in results
#     ]

# @mcp.tool()
# def get_brand_data(brand_name: str, product_type: str = "shoes") -> list:
#     return fetch_brand_data(brand_name)

# # ── FastAPI dashboard ──
# api = FastAPI()
# api.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# @api.get("/")
# def home():
#     return FileResponse("brand_dashboard(1).html")

# @api.get("/brands/{brand_name}")
# def get_brand(brand_name: str):
#     return JSONResponse(content=fetch_brand_data(brand_name))

# async def main():
#     # Run both servers concurrently
#     dashboard_config = uvicorn.Config(api, host="127.0.0.1", port=8002, log_level="warning")
#     dashboard_server = uvicorn.Server(dashboard_config)

#     print("✅ Dashboard running at http://127.0.0.1:8002")
#     print("✅ MCP server running at http://127.0.0.1:8001/sse")

#     await asyncio.gather(
#         dashboard_server.serve(),
#         mcp.run_async(transport="sse", host="127.0.0.1", port=8001)
#     )

# if __name__ == "__main__":
#     asyncio.run(main())