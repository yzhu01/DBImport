import json
import os
from pymongo import MongoClient
from pathlib import Path 
from dotenv import load_dotenv

class Course:

	def __init__(self, **kwargs):
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
	def __init__(self, **kwargs):
		self.firstName = kwargs.get('firstName')
		self.middleName = kwargs.get('middleName')
		self.lastName = kwargs.get('lastName')
		self.website = ''
		self.email = ''
		self.department = list()
		self.relatedCourse = dict()

class Department:
	def __init__(self, deptName):
		self.deptName = deptName
		self.courses = list()

class Lab:
	def __init__(self,**kwargs):
		self.UID = kwargs.get('UID')
		self.days = kwargs.get('days')
		self.startTime = kwargs.get('startTime')
		self.endTime = kwargs.get('endTime')
		self.startDate = kwargs.get('startDate')
		self.endDate = kwargs.get('endDate')
		self.instructor = kwargs.get('instructor')
		self.location = kwargs.get('location')

def from_raw_to_list(course_raw):
	course_list, department_list = [], []

	for department in course_raw['2018 Winter De Anza']['CourseData']:
		temp_dept = Department(department)
		temp_dept = read_course(course_raw, course_list, department, temp_dept)
		department_list.append(temp_dept)


	return course_list, department_list

def read_course(course_raw, course_list, department, temp_dept):
	for c in course_raw['2018 Winter De Anza']['CourseData'][department]:
			temp_course = Course(UID = c['CRN'],crn = c['CRN'], course_num = c['Crse'], 
							 section_num = c['Sec'], campus = c['Cmp'], num_credit = c['Cred'],
							 course_title = c['Title'], days = c['Days'], startTime = c['Time'][:8], 
							 endTime = c['Time'][9:], cap = c['Cap'], 
							 wl_cap = c['WL Cap'],instructor_name = c['Instructor'],startDate = c['Date'][:5], 
							 endDate = c['Date'][6:],location = c['Location'],attribute = c['Attribute'])
			course_list.append(temp_course)
			course_ineach_dept = '{0} {1} {2}'.format(temp_dept.deptName, temp_course.course_num, temp_course.course_title) 
			if course_ineach_dept not in temp_dept.courses:
				temp_dept.courses.append(course_ineach_dept)
	return temp_dept


def course_obj_to_dict(course):
	temp_course = {
			'UID' : course.UID,
			'crn': course.crn,
			'course_num' : course.course_num,
			'section_num' : course.section_num,
			'campus' : course.campus,
			'num_credit' : course.num_credit,
			'course_title' : course.course_title,
			'days' : course.days,
			'start_time' : course.startTime,
			'end_time' : course.endTime,
			'cap' : course.cap,
			'wl_cap' : course.wl_cap,
			'instructor_name' : course.instructor_name,
			'start_date' : course.startDate,
			'end_date' : course.endDate,
			'location' : course.location,
			'attribute' : course.attribute,
		}
	return temp_course

def dept_obj_to_dict(dept):
	temp_dept = {
			'department_name' : dept.deptName,
			'course_list' : dept.courses
		}
	return temp_dept

def get_db():
	env_path = Path('.') / '.env'
	load_dotenv(dotenv_path=env_path)
	username = os.getenv('Mongo_User')
	password = os.getenv('Mongo_Password')
	db_name = 'yifeil_test'      #os.getenv('Mongo_DBName') #just tesing the code
	client = MongoClient('mongodb+srv://' + username +':' + password + '@fhdatimedb-jjsjm.mongodb.net/test?retryWrites=true&w=majority')
	return client.get_database(db_name)

def insert_data(course_list, dept_list):
	db = get_db()
	tc = db.new_test_courses  #tc for test_course, just testing the code
	td = db.new_test_depts	#td for test_dept., just testing the code


	for course in course_list:
		temp_course = course_obj_to_dict(course)
		tc.insert_one(temp_course)

	for dept in dept_list:
		temp_dept = dept_obj_to_dict(dept)
		td.insert_one(temp_dept)




def main():

	filename = input('Please enter file path (Example E:\\Personal_Workflow\\FHDA\\DBImport\\2018_Winter_De_Anza_courseData.json)\n')

	if filename:
		with open(filename, 'r') as f:
			course_raw_data = json.load(f)

	course_list, department_list = from_raw_to_list(course_raw_data)
	print('Total loaded course:', len(course_list))

	insert_data(course_list, department_list)


if __name__ == '__main__':
	main()