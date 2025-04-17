from fastapi import FastAPI,HTTPException

from fastapi.middleware.cors import CORSMiddleware
from utils.db_function import insert_function, get_daily_available_time_slot, get_weekly_available_time_slot

from utils.date import *
from utils.type import front_end_booking_request_type
app = FastAPI(title="Calendar API",description="A simple API for a calendar")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     
        "http://localhost:8080",     
        "http://127.0.0.1:5173",     
        "*"                          
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "welcome to the calendar API"}


@app.get("/timeslots/week/{week_offset}")
async def get_weekly_slots(week_offset:int):
    """
    获取当前周的所有可用时间段
    """
    weekly_slots = get_weekly_available_time_slot(week_offset)
    return {"week_data": weekly_slots}

@app.post("/timeslots/book")
async def book_slot(request:front_end_booking_request_type):
    from utils.db_agent import parse_agent,db_agent
    from agents import Runner
    try:
        result = await Runner.run(db_agent, request.msg)
        return {"success":True,"message":result.final_output}
    except Exception as e:
        return {"success":False,"error":str(e)}

if __name__ == "__main__":
    import uvicorn
    port = 6765
    import subprocess
    subprocess.run(["uvicorn", "app:app", "--host", "0.0.0.0", "--port", str(port), "--reload"])






