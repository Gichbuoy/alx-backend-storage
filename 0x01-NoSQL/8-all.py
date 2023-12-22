#!/usr/bin/env python3

"""
List all documents in Python
"""

from typing import List


def list_all(mongo_collection) -> List:
    """lists all documents in a collection

    Args:
        mongo_collection (MongoClient.collection):
            will be the pymongo collection object

    Return: 
        list of documents in a collection
            or an empty list if there are no documents
    """
    return list(mongo_collection.find())


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017")
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
