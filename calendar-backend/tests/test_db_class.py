import pytest
import asyncio
from unittest.mock import patch, MagicMock
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.db_class import DatabaseManager

class TestDatabaseManager:
    """测试DatabaseManager类的各个功能"""
    
    def test_get_sync_client(self):
        """测试同步客户端获取"""
        # 重置类变量
        DatabaseManager._sync_client = None
        DatabaseManager._sync_db = None
        DatabaseManager._sync_collection = None
        
        # 获取同步客户端
        collection = DatabaseManager.get_sync_client()
        
        # 验证结果
        assert collection is not None
        assert isinstance(collection, Collection)
        
        # 测试单例模式
        collection2 = DatabaseManager.get_sync_client()
        assert collection is collection2
    
    @pytest.mark.asyncio
    async def test_get_async_client(self):
        """测试异步客户端获取"""
        # 重置类变量
        DatabaseManager._async_client = None
        DatabaseManager._async_db = None
        DatabaseManager._async_collection = None
        
        # 获取异步客户端
        collection = await DatabaseManager.get_async_client()
        
        # 验证结果
        assert collection is not None
        assert isinstance(collection, AsyncIOMotorCollection)
        
        # 测试单例模式
        collection2 = await DatabaseManager.get_async_client()
        assert collection is collection2
    
    def test_context_manager_sync(self):
        """测试同步上下文管理器"""
        # 创建模拟对象
        mock_collection = MagicMock()
        
        with patch.object(DatabaseManager, 'get_sync_client', return_value=mock_collection):
            with DatabaseManager.get_collection() as collection:
                assert collection is mock_collection
    
    @pytest.mark.asyncio
    async def test_context_manager_async(self):
        """测试异步上下文管理器"""
        # 创建模拟对象
        mock_collection = MagicMock()
        
        with patch.object(DatabaseManager, 'get_async_client', return_value=mock_collection):
            async with DatabaseManager.get_async_collection() as collection:
                assert collection is mock_collection
    
    def test_close_sync(self):
        """测试关闭同步连接"""
        # 创建模拟对象
        mock_client = MagicMock()
        
        # 设置类属性
        DatabaseManager._sync_client = mock_client
        DatabaseManager._sync_db = MagicMock()
        DatabaseManager._sync_collection = MagicMock()
        
        # 调用关闭方法
        DatabaseManager.close_sync()
        
        # 验证结果
        mock_client.close.assert_called_once()
        assert DatabaseManager._sync_client is None
        assert DatabaseManager._sync_db is None
        assert DatabaseManager._sync_collection is None
    
    @pytest.mark.asyncio
    async def test_close_async(self):
        """测试关闭异步连接"""
        # 创建模拟对象
        mock_client = MagicMock()
        
        # 设置类属性
        DatabaseManager._async_client = mock_client
        DatabaseManager._async_db = MagicMock()
        DatabaseManager._async_collection = MagicMock()
        
        # 调用关闭方法
        await DatabaseManager.close_async()
        
        # 验证结果
        mock_client.close.assert_called_once()
        assert DatabaseManager._async_client is None
        assert DatabaseManager._async_db is None
        assert DatabaseManager._async_collection is None
    
    def test_auto_close_sync(self):
        """测试同步自动关闭功能"""
        # 创建模拟对象
        mock_collection = MagicMock()
        
        with patch.object(DatabaseManager, 'get_sync_client', return_value=mock_collection), \
             patch.object(DatabaseManager, 'close_sync') as mock_close:
            with DatabaseManager.get_collection(auto_close=True) as collection:
                pass
            
            # 验证close_sync被调用
            mock_close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_auto_close_async(self):
        """测试异步自动关闭功能"""
        # 创建模拟对象
        mock_collection = MagicMock()
        
        with patch.object(DatabaseManager, 'get_async_client', return_value=mock_collection), \
             patch.object(DatabaseManager, 'close_async') as mock_close:
            async with DatabaseManager.get_async_collection(auto_close=True) as collection:
                pass
            
            # 验证close_async被调用
            mock_close.assert_called_once() 