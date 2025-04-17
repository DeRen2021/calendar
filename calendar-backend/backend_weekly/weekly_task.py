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

    week_dates = get_current_week_dates(week_offset=1)

    week_arrangemnt_text = read_weekly_txt()


    prompt = f"""
    The weekly arrangement text is as follows:
    {week_arrangemnt_text}

    Please generate a list of avaliable time slots for the user for the next 5 days.
    The date is {week_dates}.
    """

    print(prompt)

    result = await Runner.run(weekly_agent,prompt)

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
