# -*- coding: utf-8 -*-
"""Insert Data component.

This module gets lists of Course and Department objects from ReadCourseData.py
and insert those data into desired databse
"""


import os
import logging
import datetime
import json
from google.protobuf.json_format import MessageToDict
from ReadCourseData import from_raw_to_list
from configparser import ConfigParser
from pymongo import MongoClient
from pathlib import Path

logging.basicConfig(filename = '../log/' + 
                str(datetime.datetime.now()).replace(' ', '_').replace(':', '')[:17] + '.log', 
                level=logging.INFO, 
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
env_config = ConfigParser()
env_config.read(Path('..') / 'config' / 'setting.config')
mongo_config = env_config['MongoDB']
QUARTER_INDEX = -16

def get_db():
    """Get MongoDB username and password from config file and returns desired databse.

    Raises:
        pymongo.errors: possibly connection errors or conficuration errors
    Returns:
        The database object

    """
    username, password = mongo_config['Mongo_User'], mongo_config['Mongo_Password']
    db_name = mongo_config['Mongo_DBName']
    client = MongoClient('mongodb+srv://' + username + ':' + password
                         + mongo_config['Mongo_Postfix'])
    return client.get_database(db_name)


def check_file_open(filename):
    """Check if the json file exist in the specific directory.

    Args:
        filename: the path to the desired file
    Raises:
        FileNotFoundError: File does not exit
    Returns:
        The database object

    """
    if filename:
        with open(filename, 'r') as f:
            return json.load(f)
    logger.error('File name: ', filename, ' cannot be found!')
    raise FileNotFoundError('File not found', filename)


def insert_data(course_list, dept_list, quarter_name):
    """Insert data into databse.

    Get every single Course and Department object from the lists and 
    insert them into the correct database collections 
        (named quarter_name + 'course'/'departments')

    Args:
        course_list: the list of Course objects
        dept_list: the list of Department objects
    Raises:
        pymongo.errors: possibly connection errors or conficuration errors
    Returns:
        None
 
    """
    db = get_db()
    course_collection = db[quarter_name + ' courses']
    dept_collection = db[quarter_name + ' departments']

    for course in course_list:
        temp_course = MessageToDict(course)
        course_collection.insert_one(temp_course)
    for dept in dept_list:
        temp_dept = MessageToDict(dept)
        dept_collection.insert_one(temp_dept)


def main():
    """Runner of this DBImport program.

    With help of other functions, this main function could read the data from
    json files and put them into desired databses.
    """
    logger.info('Excecution Started.')
    config = ConfigParser()
    config.read(Path('..') / 'config' / env_config['Config']['Config_File_Name'])
    path = config['locations']['path']
    year = int(config['data_info']['start_year'])

    try:
        while config['locations'][str(year)]:
            all_quarters_in_year = config['locations'][str(year)].split(',')
            for each_quarter in all_quarters_in_year:
                quarter_name, filename = each_quarter[:QUARTER_INDEX].replace('_', ' '), path + each_quarter
                course_raw_data = check_file_open(filename)
                course_list, department_list = from_raw_to_list(course_raw_data, quarter_name)
                insert_data(course_list, department_list, quarter_name)
            year += 1
    except pymongo.errors.ConnectionFailure:
        logger.error('MongoDB connection failure!')
        return
    except pymongo.errors:
        logger.error('Error with MongoDB!')
        return
    except FileNotFoundError fnfe:
        logger.error(fnfe)
        return
    except KeyError ke:
        logger.error(ke, 'is not found in json file!')
        return
    finally:
        logger.info('Excecution Finished.')

if __name__ == "__main__":
    main()
