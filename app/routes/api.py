from fastapi import APIRouter
from app.data_fetcher import fetch_data
from app.data_processor import process_data

router = APIRouter()

@router.get("/generate_data")
async def generate_data():    
    df = await fetch_data() 
    rfp_count, file_count, avg_services_per_month = process_data(df)
    return {
        "total_files_created": file_count,
        "rfps_analyzed": rfp_count,
        "average_services_requested": [avg_services_per_month]
    }

@router.get("/")
def home():
    return{"message":"This is my CWSSG's API practical interview Data Engineer. Please go to /generate_data"}