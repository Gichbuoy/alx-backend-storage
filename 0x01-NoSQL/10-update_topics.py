#!/usr/bin/env python3
"""
Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes the topics of a school document based on the provided school name.

    Parameters:
    - mongo_collection (pymongo.collection.Collection): The PyMongo collection object.
    - name (str): The name of the school to update.
    - topics (list): The list of topics to be set for the school.

    Returns:
    - result: The result of the update operation.
    """
    mongo_collection.update_one(
        {'name': name},
        {'$set': {'topics': topics}}
        )


if __name__ == '__main__':
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    update_topics(
        school_collection,
        "Holberton school",
        ["Sys admin", "AI", "Algorithm"]
        )

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(
            school.get('_id'),
            school.get('name'),
            school.get('topics', "")
            ))

    update_topics(
        school_collection,
        "Holberton school",
        ["iOS"]
        )

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(
            school.get('_id'),
            school.get('name'),
            school.get('topics', "")
            ))
