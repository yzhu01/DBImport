# -*- coding: utf-8 -*-
"""Read Course Data component.

This module helps the runner to read course data from json files and return
lists of Course and Department objects for databse insertion
"""

import json
import os
import datetime
from pymongo import MongoClient
from pathlib import Path

class Course:
    """Course class.

    This class contains all information about the Course Object.

    Attributes:
        UID: an unique ID for each course, still working on deciding the pattern
        crn: the CRN of the course
        course_num: the course number, for example 'D001A' in 'EWRT' department
        section_num: the section number, for example '004' in 'EWRT D001A 004' Course
        campus: 'DA' or 'FH' or something else
        num_credit: the number of credits for this course
        course_title: the title for this course, for example 'FINAN ACCOUNTING I' for 'ACCT D001A'
        days: on what days do the course hold, for example 'MTWRF'
        startTime: the start time of this particular course
        endTime: the end time of this particular course
        cap: the capacity (maximum number of student enrollment) for this course
        wl_cap: the capacity of the waitlist for this course
        instructor_name: the name of the instructor
        startDate: the date of the first day of this course
        endDate: the date of the last day for his course
        location: the room at which this course holds
        attribute: currently holds space for GE curriculum, more usage could be deceloped
        lab: the list that holds the lab session for this course, still developing the schema
        act: the list which records the numebr of enrollment for this course (a timestamp list could be considered?)
        wl_act: the list which records the number of waitlisted student for this course(share timestamp with above)

    """

    def __init__(self, **kwargs):
        """Initialize an object for Course class.

        kwargs parameter: same as the class attributes above

        Initialize a Course object with the **kwargs
        """
        self.UID = kwargs.get('UID')
        self.crn = kwargs.get('crn')
        self.course_num = kwargs.get('course_num')
        self.section_num = kwargs.get('section_num')
        self.campus = kwargs.get('campus')
        self.num_credit = kwargs.get('num_credit')
        self.course_title = kwargs.get('course_title')
        self.days = kwargs.get('days')
        self.startTime = kwargs.get('startTime')
        self.endTime = kwargs.get('endTime')
        self.cap = kwargs.get('cap')
        self.wl_cap = kwargs.get('wl_cap')
        self.instructor_name = kwargs.get('instructor_name')
        self.startDate = kwargs.get('startDate')
        self.endDate = kwargs.get('endDate')
        self.location = kwargs.get('location')
        self.attribute = kwargs.get('attribute')
        self.lab = list()
        self.act = list()
        self.wl_act = list()


class Instructor:
    """Instructor class.

    This class contains some information about the Instructor Object

    Attributes:
        firstName, middleName, lastName: three components of name for the insructor
        website, email: the relative information about this instructor
        department: a list of departments that this instructor takes part in
        relatedCourse: a list of courses this instructor was/is/will taught/teaching/teach

    """

    def __init__(self, **kwargs):
        """Initialize an object for Instructor class.

        kwargs parameter: same as the class attributes above

        Initialize a Instructor object with the **kwargs
        """
        self.firstName, self.middleName = kwargs.get('firstName'), kwargs.get('middleName')
        self.lastName = kwargs.get('lastName')
        self.website, self.email = '', ''
        self.department = list()
        self.relatedCourse = dict()


class Department:
    """The Department class contains some information about the Department Object.

    Attributes:
        deptName: the name of this department
        courses: a list of courses that this department offers

    """

    def __init__(self, deptName):
        """Initialize an object for Department class.

        Parameters: deptName: the name of this department

        Initialize a Department object with the **kwargs
        """
        self.deptName, self.courses = deptName, list()


class Lab:
    """No usage so far, still thinking about how to implement lab with courses."""

    def __init__(self, **kwargs):
        """Initialize an object for Instructor class."""
        self.UID = kwargs.get('UID')
        self.days = kwargs.get('days')
        self.startTime = kwargs.get('startTime')
        self.endTime = kwargs.get('endTime')
        self.startDate = kwargs.get('startDate')
        self.endDate = kwargs.get('endDate')
        self.instructor = kwargs.get('instructor')
        self.location = kwargs.get('location')

#########################END OF CLASS DECLARATION#################################


def read_course(course_information_list, course_list, department):
    """Convert course json object to lists of objects.

    With the course_information_list inclues the quarter name, raw json file of the quarter,
    and the department name, this function read data from json file and initialize Course objects
    using the data from json file. The initialized Course obejcts will be put into the course_list
    argument and the list of all course titles under this department name will be returned

    Args:
      course_information_list:
              - course_information_list[0]: the name of the quarter, 
                      used to access course values in json file
              - course_information_list[1]: the raw json file
      course_list: the list of courses, mutates during runtime to 
                          be filled with course objects
      department: the department name, used to access the json file 
                      and to record what courses are in this department
    Raises:
        KeyError: If the attributes provided is not in the json key list
    Returns:
        The list containing the name of all courses in this department

    """
    temp_dept = Department(department)
    for each_course in course_information_list[1][course_information_list[0]]['CourseData'][department]:
        temp_course = Course(UID=each_course['CRN'], crn=each_course['CRN'],
                             course_num=each_course['Crse'], section_num=each_course['Sec'],
                             campus=each_course['Cmp'], num_credit=each_course['Cred'],
                             course_title=each_course['Title'], days=each_course['Days'],
                             startTime=each_course['Time'][:8], endTime=each_course['Time'][9:],
                             cap=each_course['Cap'], wl_cap=each_course['WL Cap'],
                             instructor_name=each_course['Instructor'], startDate=each_course['Date'][:5],
                             endDate=each_course['Date'][6:], location=each_course['Location'],
                             attribute=each_course['Attribute'])
        course_list.append(temp_course)
        course_ineach_dept = '{0} {1} {2}'.format(temp_dept.deptName,
                                                  temp_course.course_num, temp_course.course_title)
        if course_ineach_dept not in temp_dept.courses:
            temp_dept.courses.append(course_ineach_dept)
    return temp_dept


def from_raw_to_list(course_raw, quarter_name):
    """Convert opened json files to two lists of Course objects and Department objects.

    Args:
        course_raw: opened json file
        quarter_name: the name of the quarter, used to access the 'CourseData' key in the json file
    Raises:
        KeyError: If the 'course_raw' attribute provided is not in the json key list
    Returns:
        the two lists of Course objects and Department objects

    """
    course_list, department_list = [], []
    for department in course_raw[quarter_name]['CourseData']:
        department_list.append(read_course([quarter_name, course_raw], course_list, department))
    return course_list, department_list
