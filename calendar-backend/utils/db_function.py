# DB package
from .db_class import DatabaseManager

#validate
from .type import insert_avaliable_time_slot_type

#date
from utils.date import get_current_week_dates



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
 
async def get_daily_available_time_slot(db_instance:DatabaseManager, date:str):
    try:
        async with db_instance.get_async_collection() as collection:
            result = await collection.find_one({'date': str(date)})
            return {
                'success': True,
                'result': result
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'result': None
        }



async def get_weekly_available_time_slot(db_instance:DatabaseManager, week_offset:int = 0):
    week_dates = get_current_week_dates(week_offset=week_offset)
    result_dict = {}
    
    for date_obj in week_dates:
        date = str(date_obj)
        daily_result = await get_daily_available_time_slot(db_instance, date)
        if daily_result['success'] and daily_result['result'] is not None:
            db_record = daily_result['result']
            result_dict[db_record['date']] = db_record['slots']
        else:
            result_dict[date] = []
    
    return result_dict



