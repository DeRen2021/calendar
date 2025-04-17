import pytest
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock

from utils.db_class import DatabaseManager

# 保存原始环境变量
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    # 保存原始环境变量
    original_uri = os.environ.get('MONGODB_URI', '')
    original_db = os.environ.get('DB_NAME', '')
    original_collection = os.environ.get('COLLECTION_NAME', '')
    
    # 设置测试环境变量
    os.environ['MONGODB_URI'] = os.environ.get('TEST_MONGODB_URI', 'mongodb://localhost:27017')
    os.environ['DB_NAME'] = 'test_calendar_db'
    os.environ['COLLECTION_NAME'] = 'test_calendar_collection'
    
    yield
    
    # 恢复原始环境变量
    os.environ['MONGODB_URI'] = original_uri
    os.environ['DB_NAME'] = original_db
    os.environ['COLLECTION_NAME'] = original_collection

# 创建模拟数据库实例
@pytest.fixture
def mock_db():
    mock = MagicMock()
    mock_collection = AsyncMock()
    
    # 设置异步上下文管理器行为
    mock.get_async_collection.__aenter__.return_value = mock_collection
    mock.get_async_collection.__aexit__.return_value = None
    
    return mock, mock_collection

# 提供真实的测试数据库实例
@pytest.fixture
async def test_db():
    db = DatabaseManager()
    
    # 测试前清空集合
    async with db.get_async_collection() as collection:
        await collection.delete_many({})
    
    yield db
    
    # 测试后清空集合
    async with db.get_async_collection() as collection:
        await collection.delete_many({})
    
    # 关闭连接
    await db.close_async()

# 为pytest提供事件循环
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 