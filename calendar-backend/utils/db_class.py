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
            
