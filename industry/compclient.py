import asyncio
from fastmcp import Client

async def run_comparison():
    async with Client("http://127.0.0.1:8001/sse") as client:  # ← changed /sse to /mcp/sse
        nike_data = await client.call_tool("get_brand_data", {"brand_name": "nike"})
        puma_data = await client.call_tool("get_brand_data", {"brand_name": "puma"})
        
        context = f"Nike Data: {nike_data}\nPuma Data: {puma_data}"
        final_prompt = f"""
        Based on this real-time data:
        {context}
        
        Compare the average price and ratings between Nike and Puma. 
        Which brand currently offers better value for money?
        """
        
        print("--- Context Provided to AI ---")
        print(final_prompt)

if __name__ == "__main__":
    asyncio.run(run_comparison())