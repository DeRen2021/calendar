from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from contextlib import asynccontextmanager, contextmanager
from pymongo.server_api import ServerApi
from utils.config import URI, DB_NAME, COLLECTION_NAME

class DatabaseManager:
    _sync_client = None
    _async_client = None
    _sync_db = None
    _async_db = None
    _sync_collection = None
    _async_collection = None

    @classmethod
    def get_sync_client(cls):
        """获取同步客户端（按需创建）"""
        if not cls._sync_client:
            cls._sync_client = MongoClient(URI, server_api=ServerApi('1'))
            cls._sync_db = cls._sync_client[DB_NAME]
            cls._sync_collection = cls._sync_db[COLLECTION_NAME]
        return cls._sync_collection

    @classmethod
    async def get_async_client(cls):
        """获取异步客户端（按需创建）"""
        if not cls._async_client:
            cls._async_client = AsyncIOMotorClient(URI, server_api=ServerApi('1'))
            cls._async_db = cls._async_client[DB_NAME]
            cls._async_collection = cls._async_db[COLLECTION_NAME]
        return cls._async_collection

    @classmethod
    @contextmanager
    def get_collection(cls, auto_close=False):
        """
        同步上下文管理器
        auto_close: 是否在使用后自动关闭连接
        """
        try:
            yield cls.get_sync_client()
        finally:
            if auto_close:
                cls.close_sync()

    @classmethod
    @asynccontextmanager
    async def get_async_collection(cls, auto_close=False):
        """
        异步上下文管理器
        auto_close: 是否在使用后自动关闭连接
        """
        try:
            yield await cls.get_async_client()
        finally:
            if auto_close:
                await cls.close_async()

    @classmethod
    def clear_collection_sync(cls):
        """清空集合（同步方式）"""
        collection = cls.get_sync_client()
        result = collection.delete_many({})
        return result.deleted_count

    @classmethod
    async def clear_collection_async(cls, filter_query=None):
        """
        清空集合（异步方式）
        
        Args:
            filter_query (dict, optional): 筛选条件。如果提供，只删除匹配的文档。默认为None（删除所有文档）。
        
        Returns:
            int: 删除的文档数量
        """
        collection = await cls.get_async_client()
        
        # 如果没有提供筛选条件，则删除所有文档
        if filter_query is None:
            filter_query = {}
            
        result = await collection.delete_many(filter_query)
        return result.deleted_count

    @classmethod
    async def clear_dates_collection_async(cls, date_list=None):
        """
        清空指定日期的记录（异步方式）
        
        Args:
            date_list (list, optional): 日期列表。如果提供，只删除这些日期的记录。默认为None。
        
        Returns:
            int: 删除的文档数量
        """
        collection = await cls.get_async_client()
        
        if date_list:
            # 删除指定日期的记录
            filter_query = {"date": {"$in": [str(date) for date in date_list]}}
        else:
            # 仅删除date字段存在的记录（保留系统设置等其他记录）
            filter_query = {"date": {"$exists": True}}
            
        result = await collection.delete_many(filter_query)
        return result.deleted_count

    @classmethod
    async def close_async(cls):
        """关闭异步连接"""
        if cls._async_client:
            cls._async_client.close()
            cls._async_client = None
            cls._async_db = None
            cls._async_collection = None

    @classmethod
    def close_sync(cls):
        """关闭同步连接"""
        if cls._sync_client:
            cls._sync_client.close()
            cls._sync_client = None
            cls._sync_db = None
            cls._sync_collection = None
            
    @classmethod
    def __del__(cls):
        """析构函数，确保在类被销毁时关闭连接"""
        if cls._sync_client:
            cls.close_sync()
            