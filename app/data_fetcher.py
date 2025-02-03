from http.client import HTTPException
# import requests
import pandas
import httpx

# Endpoint to fetch data
API_URL = "https://opendata.usac.org/resource/jt8s-3q52.json"

# Year of the dataset 2024: [{"count":"135697"}]
YEAR = 2024

# Pagination limit per request
LIMIT = 20000 

async def fetch_data():
    offset = 0
    all_data = []
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            try:            
                response = await client.get(f"{API_URL}?funding_year={YEAR}&$limit={LIMIT}&$offset={offset}")                
                data = response.json()                                                
                if not data:
                    break
                all_data.extend(data)
                offset += LIMIT
            except httpx.ReadTimeout:
                print("API request timed out. Retrying...")
            except httpx.RequestError as e:
                print(f"API request failed: {e}")
                break
    return pandas.DataFrame(all_data)