#!/usr/bin/env python3
""" insert argument into document """


def insert_school(mongo_collection, **kwargs):
    """ inserts a document into a mongo collection """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
