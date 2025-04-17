from utils.date import get_current_week_dates
from utils.weekly_arrangement import read_weekly_txt
from utils.weekly_agent import weekly_agent, db_instance
from utils.db_class import DatabaseManager
from utils.config import OPENAI_API_KEY,URI,DB_NAME,COLLECTION_NAME
from agents import Agent, Runner
import asyncio

async def main():
    delete_result = await db_instance.clear_dates_collection_async()
    print(delete_result)
    print(f"Deleted {delete_result} records")
    current_week_dates = get_current_week_dates(week_offset=0)
    next_week_dates = get_current_week_dates(week_offset=1)

    week_arrangemnt_text = read_weekly_txt()

    #perhaps base on user requirements, if user want to have available time slots on weekends
    prompt = """
    The weekly arrangement text is as follows:
    {arrangemnt_text}

    Please generate a list of avaliable time slots for the user for the next 5 days.
    The date is {dates}.
    """

    this_week = {"arrangemnt_text":week_arrangemnt_text,"dates":current_week_dates}
    formatted_this_week = prompt.format(**this_week)
    next_week = {"arrangemnt_text":week_arrangemnt_text,"dates":next_week_dates}
    formatted_next_week = prompt.format(**next_week)

    
    result = await Runner.run(weekly_agent,formatted_this_week)
    print(result.final_output)

    result = await Runner.run(weekly_agent,formatted_next_week)
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())
