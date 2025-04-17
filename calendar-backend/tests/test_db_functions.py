import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import datetime

from utils.db_class import DatabaseManager
from utils.db_function import (
    delete_function,
    get_daily_available_time_slot,
    get_weekly_available_time_slot
)

# 单元测试 - 使用模拟对象
@pytest.mark.asyncio
async def test_delete_function_success():
    # 创建模拟数据库实例
    mock_db = MagicMock()
    mock_collection = AsyncMock()
    mock_result = AsyncMock()
    mock_result.deleted_count = 1
    
    # 设置模拟行为
    mock_collection.delete_one.return_value = mock_result
    mock_db.get_async_collection.__aenter__.return_value = mock_collection
    mock_db.get_async_collection.__aexit__.return_value = None
    
    # 执行测试
    result = await delete_function(mock_db, '2023-05-01')
    
    # 验证结果
    assert result['success'] is True
    assert 'result' in result
    mock_collection.delete_one.assert_called_once_with({'date': '2023-05-01'})

@pytest.mark.asyncio
async def test_delete_function_exception():
    # 创建模拟数据库实例
    mock_db = MagicMock()
    mock_collection = AsyncMock()
    
    # 设置模拟行为 - 抛出异常
    mock_collection.delete_one.side_effect = Exception("测试异常")
    mock_db.get_async_collection.__aenter__.return_value = mock_collection
    mock_db.get_async_collection.__aexit__.return_value = None
    
    # 执行测试
    result = await delete_function(mock_db, '2023-05-01')
    
    # 验证结果
    assert result['success'] is False
    assert 'error' in result
    assert result['result'] is None

@pytest.mark.asyncio
async def test_get_daily_available_time_slot_success():
    # 创建模拟数据库实例
    mock_db = MagicMock()
    mock_collection = AsyncMock()
    mock_data = {'date': '2023-05-01', 'slots': [{'start': '09:00', 'end': '10:00'}]}
    
    # 设置模拟行为
    mock_collection.find_one.return_value = mock_data
    mock_db.get_async_collection.__aenter__.return_value = mock_collection
    mock_db.get_async_collection.__aexit__.return_value = None
    
    # 执行测试
    result = await get_daily_available_time_slot(mock_db, '2023-05-01')
    
    # 验证结果
    assert result['success'] is True
    assert result['result'] == mock_data
    mock_collection.find_one.assert_called_once_with({'date': '2023-05-01'})

@pytest.mark.asyncio
async def test_get_weekly_available_time_slot():
    # 创建模拟版本的get_daily_available_time_slot函数
    async def mock_get_daily(db, date):
        if date == '2023-05-01':
            return {
                'success': True,
                'result': {'date': '2023-05-01', 'slots': [{'start': '09:00', 'end': '10:00'}]}
            }
        elif date == '2023-05-02':
            return {
                'success': True,
                'result': {'date': '2023-05-02', 'slots': [{'start': '14:00', 'end': '15:00'}]}
            }
        else:
            return {
                'success': True,
                'result': None
            }
    
    # 模拟日期函数
    mock_dates = [
        datetime.date(2023, 5, 1),
        datetime.date(2023, 5, 2),
        datetime.date(2023, 5, 3),
        datetime.date(2023, 5, 4),
        datetime.date(2023, 5, 5),
        datetime.date(2023, 5, 6),
        datetime.date(2023, 5, 7)
    ]
    
    # 应用补丁
    with patch('utils.db_function.get_daily_available_time_slot', mock_get_daily), \
         patch('utils.db_function.get_current_week_dates', return_value=mock_dates):
        
        # 执行测试
        mock_db = MagicMock()
        result = await get_weekly_available_time_slot(mock_db)
        
        # 验证结果
        assert '2023-05-01' in result
        assert '2023-05-02' in result
        assert '2023-05-03' in result
        assert result['2023-05-01'] == [{'start': '09:00', 'end': '10:00'}]
        assert result['2023-05-02'] == [{'start': '14:00', 'end': '15:00'}]
        assert result['2023-05-03'] == []  # 没有时间槽的日期应返回空列表

# 集成测试 - 需要使用真实的测试数据库
@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_integration():
    """
    此测试需要连接到测试数据库
    运行前需要设置测试环境变量，指向测试数据库
    """
    # 创建临时数据
    test_date = '2023-05-01'
    test_data = {
        'date': test_date,
        'slots': [
            {'start': '09:00', 'end': '10:00'},
            {'start': '14:00', 'end': '15:00'}
        ]
    }
    
    # 创建数据库实例
    db = DatabaseManager()
    
    try:
        # 确保测试数据不存在
        await delete_function(db, test_date)
        
        # 插入测试数据 (这里假设有一个insert_function)
        async with db.get_async_collection() as collection:
            await collection.insert_one(test_data)
        
        # 测试查询功能
        result = await get_daily_available_time_slot(db, test_date)
        assert result['success'] is True
        assert result['result']['date'] == test_date
        assert len(result['result']['slots']) == 2
        
        # 测试删除功能
        delete_result = await delete_function(db, test_date)
        assert delete_result['success'] is True
        
        # 验证数据已删除
        check_result = await get_daily_available_time_slot(db, test_date)
        assert check_result['success'] is True
        assert check_result['result'] is None
        
    finally:
        # 清理测试数据
        await delete_function(db, test_date) 