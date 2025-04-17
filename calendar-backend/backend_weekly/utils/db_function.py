# DB package
from .db_class import DatabaseManager

#validate
from .type import insert_avaliable_time_slot_type

#date
from .date import get_current_week_dates



async def delete_function(db_instance: DatabaseManager, date: str):
    try:
        async with db_instance.get_async_collection() as collection:
            result = await collection.delete_one({'date': str(date)})
            return {
                'success': True,
                'deleted_count': result.deleted_count
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'deleted_count': None
        }
async def delete_function(db_instance:DatabaseManager,date:str):
    try:
        async with db_instance.get_async_collection() as collection:
            result = await collection.delete_one({'date':str(date)})
            return {
                'success':True,
                'result':result
            }
    except Exception as e:
        return {
            'success':False,
            'error':str(e),
            'result':None
        }
 




