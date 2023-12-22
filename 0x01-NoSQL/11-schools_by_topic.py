#!/usr/bin/env python3
"""
schools with diff topics
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools having a specific topic.

    Parameters:
    - mongo_collection (pymongo.collection.Collection): The PyMongo collection object.
    - topic (str): The topic to search for.

    Returns:
    - school_list (list): A list of dictionaries representing schools with the specified topic.
    """
    return list(mongo_collection.find({"topics": {"$in": [topic]}}))


if __name__ == '__main__':
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    j_schools = [
        {
            'name': "Holberton school",
            'topics': ["Algo", "C", "Python", "React"]
        },
        {'name': "UCSF", 'topics': ["Algo", "MongoDB"]},
        {'name': "UCLA", 'topics': ["C", "Python"]},
        {'name': "UCSD", 'topics': ["Cassandra"]},
        {'name': "Stanford", 'topics': ["C", "React", "Javascript"]}
    ]
    for j_school in j_schools:
        insert_school(school_collection, **j_school)

    schools = schools_by_topic(school_collection, "Python")
    for school in schools:
        print("[{}] {} {}".format(
            school.get('_id'),
            school.get('name'),
            school.get('topics', "")
            ))
