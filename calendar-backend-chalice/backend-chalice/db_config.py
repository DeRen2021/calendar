import boto3
from pymongo import MongoClient


ssm = boto3.client("ssm")

resp = ssm.get_parameter(
    Name="mango_connection_string",
    WithDecryption=True              
)
resp1 = ssm.get_parameter(
    Name="db_name",
    WithDecryption=True              
)
resp2 = ssm.get_parameter(
    Name="collection_name",
    WithDecryption=True              
)

connection_string = resp["Parameter"]["Value"]
db_name = resp1["Parameter"]["Value"]
collection_name = resp2["Parameter"]["Value"]

client = MongoClient(connection_string)
db = client[db_name]
collection = db[collection_name]