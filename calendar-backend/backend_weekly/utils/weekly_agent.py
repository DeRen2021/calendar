from agents import function_tool,Agent
from .db_class import DatabaseManager
from .type import insert_avaliable_time_slot_type


db_instance = DatabaseManager()

@function_tool
async def insert_avaliable_time_slot(insert_avaliable_time_slot_type:insert_avaliable_time_slot_type):
    global db_instance
    try:
        async with db_instance.get_async_collection() as collection:
            result = await collection.insert_one({'date':insert_avaliable_time_slot_type.date,'slots':insert_avaliable_time_slot_type.slots})
            return result.inserted_id
    except Exception as e:
        return str(e)


prompt = """
Your job is to generate a list of avaliable time slots for the user for the next 5 days.

Once you finish each day's slot, please call the function insert_avaliable_time_slot
to insert the data into the database.
"""

weekly_agent = Agent(
    name="weekly_agent",
    instructions=prompt,
    tools=[insert_avaliable_time_slot],
)
