from utils.db_function import get_weekly_available_time_slot
from utils.db_function import get_collection_client,get_daily_available_time_slot_tool
from utils.type import insert_avaliable_time_slot_type,booking_request_type
from agents import function_tool,Agent
import asyncio


@function_tool
def book_slot(input:insert_avaliable_time_slot_type):
    try:
        collection = get_collection_client()
        query = {'date':input.date}
        update_slots = {"$set":{"slots":input.slots}}
        result = collection.update_one(query,update_slots)
        return {"success":True,"message":"slot booked successfully"}
    except Exception as e:
        return {"success":False,"error":str(e)}
    

db_agent = Agent(
    name="db_agent",
    instructions="""
    your job is to update the available time slots in the database, 
    ie when user book an appointment in a given slot for example
    if user book an appointment on 2025-03-25 from 10:00 to 10:20
    from slot 9:00 to 12:00, you need to update the available time slots in the database
    to 9:00 to 10:00 and 10:20 to 12:00
    and also the orginal slot in that day, 
    you will call get_daily_available_time_slot function to get the available time slots in that day
    with input in format like '2025-03-25'
    then you will call book_slot function to update the database
    """,
    tools=[book_slot,get_daily_available_time_slot_tool],
)

parse_agent = Agent(
    name="parse_agent",
    instructions="""
    your job is to parse the user's request and extract the 
    date, start_time, end_time, name, user_email, reason, format
    if user's is missing some information, set it to be None
    """,
    output_type=booking_request_type,
)   

