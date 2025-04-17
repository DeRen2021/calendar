from utils.date import get_eastern_date
from utils.prompt import read_file_as_string
from utils.db_function import insert_function
import logging
from utils.config import OPENAI_API_KEY
import asyncio
import os


from agents import Agent, ModelSettings, function_tool,Runner


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    return logging.getLogger(__name__)

async def weekly_plan_agent():
    date = get_eastern_date()

    
    try:
        user_habits = read_file_as_string()
        logger.info("read user habits success")
    except Exception as e:
        logger.error(f"read user habits failed: {str(e)}")
        raise
    
    prompt = f"""
    Your job is to generate a list of avaliable time slots for the user for the next 5 days.
    The user's habits are as follows:
    {
        user_habits
    }
    Once you finish each day's slot, please call the function insert_one to insert the data into the database.
    """
    
    logger.info(f"prompt generated\n{prompt}\n")

    plan_agent = Agent(
        name="Weekly Plan Agent",
        instructions=prompt,
        tools=[insert_function],
    )
    try:
        result = await Runner.run(plan_agent, f"Todays date is {date}")
        logger.info(result.final_output)
    except Exception as e:
        logger.error(f"error: {str(e)}")
        raise

if __name__ == "__main__":

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    logger = setup_logging()
    logger.info("logging start")

    asyncio.run(weekly_plan_agent())
    





    

    


    