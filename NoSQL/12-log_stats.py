#!/usr/bin/env python3
""" log stats """
from pymongo import MongoClient


Methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

def log_stats(mongo_collectiion, option=None):
    """ provides stats """
    items = {}
    if option:
        value = mongo_collectiion.count_documents({
            "method": {"$regex": option}})
        print(f"\tmethod {option}: {value}")
        return

    result = mongo_collectiion.count_documents(items)
    print(f"{result} logs")
    print("Methods:")
    for method in Methods:
        log_stats(collection, method)
    status = collection.count_documents({"path": "/status"})
    print (f"{status} status check")


if __name__ == "__main__":
    collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(collection)
