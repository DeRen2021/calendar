import pytest
import datetime

from utils.db_class import DatabaseManager
from utils.db_function import (
    delete_function,
    get_daily_available_time_slot,
    get_weekly_available_time_slot
)

# 标记为集成测试，可以通过 pytest.mark.integration 来单独运行
pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_delete_and_get_functions(test_db):
    """测试删除和获取功能的完整流程"""
    # 测试数据
    test_date = '2023-06-01'
    test_slots = [
        {'start': '09:00', 'end': '10:00'},
        {'start': '14:00', 'end': '15:00'}
    ]
    test_data = {
        'date': test_date,
        'slots': test_slots
    }
    
    # 清理可能存在的测试数据
    await delete_function(test_db, test_date)
    
    # 插入测试数据
    async with test_db.get_async_collection() as collection:
        await collection.insert_one(test_data)
    
    # 测试获取单日数据
    result = await get_daily_available_time_slot(test_db, test_date)
    assert result['success'] is True
    assert result['result'] is not None
    assert result['result']['date'] == test_date
    assert len(result['result']['slots']) == 2
    
    # 测试删除功能
    delete_result = await delete_function(test_db, test_date)
    assert delete_result['success'] is True
    
    # 验证数据已删除
    after_delete = await get_daily_available_time_slot(test_db, test_date)
    assert after_delete['success'] is True
    assert after_delete['result'] is None

@pytest.mark.asyncio
async def test_weekly_time_slot(test_db):
    """测试获取一周数据的功能"""
    # 获取当前周的日期
    now = datetime.datetime.now()
    start_of_week = now - datetime.timedelta(days=now.weekday())
    dates = [
        (start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(7)
    ]
    
    # 清理测试数据
    for date in dates:
        await delete_function(test_db, date)
    
    # 为其中两天创建数据
    test_data1 = {
        'date': dates[0],
        'slots': [{'start': '09:00', 'end': '10:00'}]
    }
    test_data2 = {
        'date': dates[2],
        'slots': [{'start': '14:00', 'end': '15:00'}]
    }
    
    async with test_db.get_async_collection() as collection:
        await collection.insert_one(test_data1)
        await collection.insert_one(test_data2)
    
    # 测试获取周数据
    weekly_result = await get_weekly_available_time_slot(test_db)
    
    # 验证结果
    assert len(weekly_result) == 7  # 应该有7天的数据
    assert weekly_result[dates[0]] == test_data1['slots']
    assert weekly_result[dates[2]] == test_data2['slots']
    assert weekly_result[dates[1]] == []  # 没有数据的日期应该返回空列表
    
    # 清理测试数据
    for date in dates:
        await delete_function(test_db, date)

@pytest.mark.asyncio
async def test_get_nonexistent_date(test_db):
    """测试获取不存在日期的行为"""
    nonexistent_date = '2099-12-31'
    
    # 确保数据不存在
    await delete_function(test_db, nonexistent_date)
    
    # 获取不存在的日期
    result = await get_daily_available_time_slot(test_db, nonexistent_date)
    
    # 验证结果
    assert result['success'] is True
    assert result['result'] is None

@pytest.mark.asyncio
async def test_error_handling(test_db):
    """测试错误处理 - 这个测试可能需要模拟数据库错误"""
    with pytest.raises(Exception):
        # 通过提供无效的日期格式来触发错误
        await get_daily_available_time_slot(None, 'invalid-date')
        
    # 或者可以模拟数据库错误
    with pytest.raises(Exception):
        # 关闭数据库连接后尝试操作
        await test_db.close_async()
        await get_daily_available_time_slot(test_db, '2023-01-01') 