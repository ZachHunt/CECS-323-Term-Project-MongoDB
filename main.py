import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
from datetime import datetime


def pp(thing):
    for thingee in thing:
        pprint(thingee)


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    :param collection:  The pointer to the departments collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["departments"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while True:
        try:
            name = input("Department name --> ")
            abbreviation = input("Department's abbreviation --> ")
            chair_name = input("Department's chair name --> ")
            building = input("Department's building ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', "
                             "'EN5', 'ET', 'HSCI', 'NUR', 'VEC') --> ")
            office = int(input("Department's office --> "))
            description = input("Department's description --> ")

            name_count: int = collection.count_documents({"name": name})
            unique_name = name_count == 0

            if not unique_name:
                print("We already have a department by that name.  Try again.")
                continue

            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0

            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
                continue

            chair_name_count = collection.count_documents({"chair_name": chair_name})
            unique_chair_name = chair_name_count == 0

            if not unique_chair_name:
                print("We already have a department with that chair name.  Try again.")
                continue

            building_and_office_count = collection.count_documents({"building": building, "office": office})
            unique_building_and_office = building_and_office_count == 0

            if not unique_building_and_office:
                print("We already have a department in that building and office.  Try again.")
                continue

            # description_count = collection.count_documents({"description": description})
            # unique_description = description_count == 0
            #
            # if not unique_description:
            #     print("We already have a department with that description.  Try again.")
            #     continue

            # Build a new students document preparatory to storing it
            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chair_name,
                "building": building,
                "office": office,
                "description": description
            }

            create_department_collection()

            results = collection.insert_one(department)
            print("Department added!")
            break

        except ValueError:
            print("Inputted value for the field is invalid. Please input an integer.")
            print("Please try again.")

        except Exception as e:
            # print a user-friendly message instead of the traceback string
            print("An error occurred:", end=" ")
            error_str = str(e)

            if "'name'" in error_str:
                print(
                    "Inputted value for the 'name' field is invalid due to violation of validation constraint. {}".format(
                        error_str))

            elif "'abbreviation'" in error_str:
                print("Inputted value for the 'abbreviation' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'chair_name'" in error_str:
                print("Inputted value for the 'chair_name' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'building'" in error_str:
                print("Inputted value for the 'building' field is invalid due to violation of "
                      "validation constraint. The building name must be one of the enum value. {}".format(error_str))

            elif "'description'" in error_str:
                print("Inputted value for the 'description' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            print("Please try again.")


def add_course(db):
    """
        :param collection:  The pointer to the course collection.
        :return:            None
        """
    # Create a "pointer" to the students collection within the db database.
    course_collection = db["courses"]
    unique_name: bool = False
    unique_number: bool = False
    course_name: str = ''
    course_number: int = 0
    description: str = ''
    units: int = 0

    while True:
        try:
            dept = select_department(db)
            dept_abbre = dept["abbreviation"]
            course_name = input("Course name --> ")
            course_number = int(input("Course number --> "))
            description = input("Course description --> ")
            units = int(input("Course units --> "))

            name_count: int = course_collection.count_documents({"name": course_name})
            unique_name = name_count == 0

            if not unique_name:
                print("We already have a course by that name.  Try again.")
                continue

            number_count = course_collection.count_documents({"abbreviation": course_number})
            unique_number = number_count == 0

            if not unique_number:
                print("We already have a course with that number.  Try again.")
                continue

            # Build a new students document preparatory to storing it
            course = {
                "department_abbreviation": dept_abbre,
                "course_name": course_name,
                "course_number": course_number,
                "description": description,
                "units": units
            }

            create_course_collection()

            results = course_collection.insert_one(course)
            department_collection = db['departments']
            pp(department_collection.aggregate([{"$lookup": {"from": "courses",
                                                             "localField": "abbreviation",
                                                             "foreignField": "department_abbreviation",
                                                             "as": "courses"}
                                                 }, {"$match": {"courses": {"$exists": True,
                                                                            "$type": 'array',
                                                                            "$not": {"$size": 0}}}}
                                                ]))
            print("Course added!")

            break

        except ValueError:
            print("Inputted value is invalid. Please input an integer.")
            print("Please try again.")

        except Exception as e:
            # print a user-friendly message instead of the traceback string
            print("An error occurred:", end=" ")
            error_str = str(e)

            if "'course_name'" in error_str:
                print(
                    "Inputted value for the 'course_name' field is invalid due to violation of validation constraint. {}".format(
                        error_str))

            elif "'course_number'" in error_str:
                print("Inputted value for the 'course_number' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'units'" in error_str:
                print("Inputted value for the 'units' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'description'" in error_str:
                print("Inputted value for the 'description' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            print("Please try again.")


def add_section(db):
    """
    :param collection:  The pointer to the sections collection.
    :return:            None
    """
    # Create a "pointer" to the sections collection within the db database.
    collection = db["sections"]

    # init attributes
    department_abbreviation: str = ''  # fk from courses
    course_number: int = 0  # fk from courses
    # student_id: int = 0                # fk from student
    section_number: int = 0
    semester: str = ''
    section_year: int = 0
    building: str = ''
    room: int = 0
    schedule: str = ''
    start_time: int = 0
    instructor: str = ''

    # init uniqueness checks

    # 1. {course, sectionNumber, semester, sectionYear}
    unique_constraint_1: bool = False
    # 2. {semester, sectionYear, building, room, schedule, startTime}
    unique_constraint_2: bool = False
    # 3. {semester, sectionYear, schedule, startTime, instructor}
    unique_constraint_3: bool = False
    # 4. {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
    # unique_constraint_4: bool = False

    while True:
        try:
            # getting migrating foreign keys from the courses class: department abbrev and course num
            course_document = select_course(db)
            department_abbreviation = course_document['department_abbreviation']
            course_number = course_document['course_number']

            # student_document = select_student(db)
            # student_id = student_document['_id']

            # the rest of the attributes is coming from the keyboard inputs
            section_number = int(input("Section number --> "))
            semester = input("Semester ('Fall', 'Spring', 'Winter', 'Summer I', 'Summer II', 'Summer III') --> ")
            section_year = int(input("Section year --> "))
            building = input("Building ('NAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', "
                             "'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC') --> ")
            room = int(input("Room number (between 1 and 999) --> "))
            schedule = input("Schedule (MW', 'MWF', 'TuTh', 'F', 'S') --> ")
            start_hour = int(input('Start HOUR in a 24-hour time format (between hour 8 and hour 19) note:'
                                   'the start time will be calculated with inputs and resulting '
                                   'inputs must be between 800 - 1930) --> '))
            start_minute = int(input('Start MINUTE (between 0 minute and 59 minutes) --> '))
            start_time = (start_hour * 100) + start_minute
            instructor = input("Instructor name --> ")

            # checking uniqueness
            # I.
            constraint_1_count = collection.count_documents({"course_number": course_number,
                                                             "section_number": section_number,
                                                             "semester": semester,
                                                             "section_year": section_year})

            unique_constraint_1 = constraint_1_count == 0
            if not unique_constraint_1:
                print("We already have a section with that course number, section number, semester,"
                      "and section year.  Try again.")
                continue

            # II.
            constraint_2_count = collection.count_documents({"semester": semester, "section_year": section_year,
                                                             "building": building, "room": room,
                                                             "schedule": schedule, "start_time": start_time})

            unique_constraint_2 = constraint_2_count == 0
            if not unique_constraint_2:
                print("We already have a section with that semester, section year, building, room,"
                      "schedule, and start time.  Try again.")
                continue

            # III.
            constraint_3_count = collection.count_documents({"semester": semester, "section_year": section_year,
                                                             "schedule": schedule, "start_time": start_time,
                                                             "instructor": instructor})

            unique_constraint_3 = constraint_3_count == 0
            if not unique_constraint_3:
                print("We already have a section with that semester, section year, schedule, start time,"
                      "and instructor.  Try again.")
                continue

            # IV.
            # FIXME: ADD STUDENT ID TO THIS UNIQUE CONSTRAINT TO GET STUDENT ID
            # constraint_4_count = collection.count_documents({"semester": semester, "section_year": section_year,
            #                                                  "department_abbreviation": department_abbreviation,
            #                                                  "course_number": course_number, "student_id": student_id})

            # unique_constraint_4 = constraint_4_count == 0
            # if not unique_constraint_4:
            #     print("We already have a section with that semester, section year, department abbreviation, "
            #           "course number, and student id.  Try again.")
            #     continue

            section = {
                "department_abbreviation": department_abbreviation,
                "course_number": course_number,
                "section_number": section_number,
                "semester": semester,
                "section_year": section_year,
                "building": building,
                "room": room,
                "schedule": schedule,
                "start_time": start_time,
                "instructor": instructor
            }

            create_section_collection()

            results = collection.insert_one(section)
            print("section added!")
            break

        except ValueError:
            print("Inputted value for the field is invalid. Please input an integer.")
            print("Please try again.")

        except Exception as e:
            # print a user-friendly message instead of the traceback string
            print("An error occurred:", end=" ")
            error_str = str(e)

            if "'section_number'" in error_str:
                print("Inputted value for the 'section_number' field is invalid "
                      "due to violation of validation constraint. {}".format(error_str))

            elif "'semester'" in error_str:
                print("Inputted value for the 'semester' field is invalid due to violation of "
                      "validation constraint. The semester term must be one of the enum value. {}".format(error_str))

            elif "'section_year'" in error_str:
                print("Inputted value for the 'section_year' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'building'" in error_str:
                print("Inputted value for the 'building' field is invalid due to violation of "
                      "validation constraint. The building name must be one of the enum value. {}".format(error_str))

            elif "'room'" in error_str:
                print("Inputted value for the 'room' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'schedule'" in error_str:
                print("Inputted value for the 'schedule' field is invalid due to violation of "
                      "validation constraint. The schedule day(s) must be one of the enum value. {}".format(error_str))

            elif "'start_time'" in error_str:
                print("Inputted value for the 'start_time' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            elif "'instructor'" in error_str:
                print("Inputted value for the 'instructor' field is invalid due to violation of "
                      "validation constraint. {}".format(error_str))

            print("Please try again.")


def add_student(db):
    """
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    eMail: str = ''

    while True:
        try:
            last_name = input("Last name --> ")
            first_name = input("First name --> ")
            eMail = input("Student eMail --> ")

            name_count = collection.count_documents({"last_name": last_name, "first_name": first_name})
            unique_name = name_count == 0

            if not unique_name:
                print("We already have a student with that last and first name.  Try again.")
                continue

            email_count = collection.count_documents({"eMail": eMail})
            unique_email = email_count == 0

            if not unique_email:
                print("We already have a student with that email.  Try again.")
                continue

            student = {
                "last_name": last_name,
                "first_name": first_name,
                "eMail": eMail
            }

            create_student_collection()

            results = collection.insert_one(student)
            print("student added!")
            break

        except Exception as e:
            # print a user-friendly message instead of the traceback string
            print("An error occurred:", end=" ")
            error_str = str(e)
            print(error_str)

            # if "'_id'" in error_str:
            #     print("student id error")
            #
            # if "'last_name'" in error_str:
            #     print("Inputted value for the 'last_name' field is invalid due "
            #           "to violation of validation constraint. {}".format(error_str))
            #
            # elif "'first_name'" in error_str:
            #     print("Inputted value for the 'student_name' field is invalid due to violation of "
            #           "validation constraint. {}".format(error_str))
            #
            # elif "'eMail'" in error_str:
            #     print("Inputted value for the 'eMail' field is invalid due to violation of "
            #           "validation constraint. {}".format(error_str))

            print("Please try again.")


def add_major(db):
    collection = db["majors"]
    unique_name: bool = False
    name: str = ""
    description: str = ""
    while not unique_name:
        department = select_department(db)
        department_abbreviation = department['abbreviation']
        name = input("Major name --> ")
        description = input("Major description --> ")
        name_count = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name. Try again.")

    # Build a new major document prepatory to storing it.
    major = {
        "name": name,
        "description": description,
        "department_abbreviation": department_abbreviation
    }

    create_major_collection()

    results = collection.insert_one(major)
    print("Major added!")


def add_student_major(db):
    student_major_collection = db["student_majors"]
    unique_student_major: bool = False
    day: int = 0
    month: int = 0
    year: int = 0
    declarationDate: datetime
    correct_time: bool = False
    student = select_student(db)

    while True:
        try:
            while not unique_student_major:
                major = select_major(db)
                student_major_count: int = student_major_collection.count_documents({"student_id": student["_id"],
                                                                                     "major_name": major["name"]})
                unique_student_major = student_major_count == 0
                if not unique_student_major:
                    print(f"{student['first_name']} {student['last_name']} already has the major {major['name']}."
                          f" Try again.")

            while not correct_time:
                year = int(input("Enter the declaration year (YYYY) --> "))
                month = int(input("Enter the declaration month (MM) --> "))
                day = int(input("Enter the declaration day (DD) --> "))
                declarationDate = datetime(year, month, day)
                todayDate = datetime.now()
                print("Today's date is ", todayDate)
                if declarationDate > todayDate:
                    print("You living in the future? Try again.")
                else:
                    print("This date is fine.")
                    correct_time = True

            student_major = {
                "student_id": student["_id"],
                "student_first_name": student["first_name"],
                "student_last_name": student["last_name"],
                "major_name": major["name"],
                "department_abbreviation": major["department_abbreviation"],
                "declaration_date": declarationDate
            }
            create_student_majors_collection()
            student_major_collection.insert_one(student_major)
            print("Major added to Student! ")
        except Exception as e:
            print(e)
        break


def add_major_student(db):
    student_major_collection = db["student_majors"]
    unique_student_major: bool = False
    day: int = 0
    month: int = 0
    year: int = 0
    declarationDate: datetime
    correct_time: bool = False
    while True:
        try:
            while not unique_student_major:
                student = select_student(db)
                major = select_major(db)
                student_major_count: int = student_major_collection.count_documents({"student_id": student["_id"],
                                                                                     "major_name": major["name"]})
                unique_student_major = student_major_count == 0
                if not unique_student_major:
                    print("This major already has this student. Try again.")

            while not correct_time:
                year = int(input("Enter the declaration year (YYYY) --> "))
                month = int(input("Enter the declaration month (MM) --> "))
                day = int(input("Enter the declaration day (DD) --> "))
                declarationDate = datetime(year, month, day)
                todayDate = datetime.now()
                print("Today's date is ", todayDate)
                if declarationDate > todayDate:
                    print("You living in the future? Try again.")
                else:
                    print("This date is fine.")
                    correct_time = True

            student_major = {
                "student_id": student["_id"],
                "student_first_name": student["first_name"],
                "student_last_name": student["last_name"],
                "major_name": major["name"],
                "department_abbreviation": major["department_abbreviation"],
                "declaration_date": declarationDate
            }
            create_student_majors_collection()
            student_major_collection.insert_one(student_major)
            print("Student added to Major! ")
        except Exception as e:
            print(e)
        break


def add_student_section(db):
    collection = db["enrollments"]
    unique_student_section: bool = False
    while (True):
      try:
        while not unique_student_section:
            student = select_student(db)
            section = select_section(db)
            type = input("Enter passfail or lettergrade: ")
            category = type.lower().replace(" ", "")
            satisfactory = ['A', 'B', 'C']
            if category == "lettergrade":
                grade = input("Enter minimum satisfactory grade: ")
                grade_case = grade.upper().replace(" ", "")
                print(grade_case)
                print(grade_case in satisfactory)
                if grade_case in satisfactory:
                    student_section_count = collection.count_documents({"semester": section["semester"],
                                                                        "section_year": section["section_year"],
                                                                        "department_abbreviation": section[
                                                                            "department_abbreviation"],
                                                                        "course_number": section["course_number"],
                                                                        "section_number": section["section_number"],
                                                                        "student_id": student["_id"],
                                                                        })

                    unique_student_section = student_section_count == 0
                    if not unique_student_section:
                        print("Student is already enrolled in that section.")
                    if unique_student_section:
                        lettergrade_enrollment = {
                            "department_abbreviation": section["department_abbreviation"],
                            "course_number": section["course_number"],
                            "semester": section["semester"],
                            "section_year": section["section_year"],
                            "section_number": section["section_number"],
                            "student_id": student["_id"],
                            "enrollment_category_data": category,
                            "min_satisfactory_grade": grade_case
                        }
                        collection.insert_one(lettergrade_enrollment)
                        print("Lettergrade enrollment added.")
                else:
                    print("Minimum satisfactory grade must be either A, B, or C.")
            if category == "passfail":
                applicationDate = datetime.now()
                if applicationDate <= datetime.now():
                    student_section_count = collection.count_documents({"semester": section["semester"],
                                                                        "section_year": section["section_year"],
                                                                        "department_abbreviation": section[
                                                                            "department_abbreviation"],
                                                                        "course_number": section["course_number"],
                                                                        "section_number": section["section_number"],
                                                                        "student_id": student["_id"],
                                                                        })

                    unique_student_section = student_section_count == 0
                    if not unique_student_section:
                        print("Student is already enrolled in that section.")
                    if unique_student_section:
                        passfail_enrollment = {
                            "department_abbreviation": section["department_abbreviation"],
                            "course_number": section["course_number"],
                            "semester": section["semester"],
                            "section_year": section["section_year"],
                            "section_number": section["section_number"],
                            "student_id": student["_id"],
                            "enrollment_category_data": category,
                            "application_date": applicationDate
                        }
                        collection.insert_one(passfail_enrollment)
                        print("Passfail enrollment added.")
                else:
                    print("Application date is in the future. Please try again.")
            if category != "passfail" and not "lettergrade":
                print("Must enter either passfail or letter grade.")
      except Exception as e:
          print(e)
      break


def add_section_student(db):
    collection = db["enrollments"]
    unique_section_student: bool = False
    while (True):
        try:
            while not unique_section_student:
                section = select_section(db)
                student = select_student(db)
                type = input("Enter passfail or lettergrade: ")
                category = type.lower().replace(" ", "")
                if category == "lettergrade":
                    satisfactory = ['A', 'B', 'C']
                    grade = input("Enter minimum satisfactory grade: ")
                    grade_case = grade.upper().replace(" ", "")
                    print(grade_case)
                    print(grade_case in satisfactory)
                    if grade_case in satisfactory:
                        section_student_count = collection.count_documents({"semester": section["semester"],
                                                                            "section_year": section["section_year"],
                                                                            "department_abbreviation": section[
                                                                                "department_abbreviation"],
                                                                            "course_number": section["course_number"],
                                                                            "section_number": section["section_number"],
                                                                            "student_id": student["_id"]})

                        unique_section_student = section_student_count == 0
                        if not unique_section_student:
                            print("Student is already enrolled in that section.")
                        if unique_section_student:
                            lettergrade_enrollment = {
                                "department_abbreviation": section["department_abbreviation"],
                                "course_number": section["course_number"],
                                "semester": section["semester"],
                                "section_year": section["section_year"],
                                "section_number": section["section_number"],
                                "student_id": student["_id"],
                                "enrollment_category_data": category,
                                "min_satisfactory_grade": grade_case
                            }
                            collection.insert_one(lettergrade_enrollment)
                            print("Lettergrade enrollment added.")
                    else:
                        print("Minimum satisfactory grade must be either A, B, or C.")
                if category == "passfail":
                    applicationDate = datetime.now()
                    if applicationDate <= datetime.now():
                        section_student_count = collection.count_documents({"semester": section["semester"],
                                                                            "section_year": section["section_year"],
                                                                            "department_abbreviation": section[
                                                                                "department_abbreviation"],
                                                                            "course_number": section["course_number"],
                                                                            "section_number": section["section_number"],
                                                                            "student_id": student["_id"]})

                        unique_section_student = section_student_count == 0
                        if not unique_section_student:
                            print("That section already has that student.")
                        if unique_section_student:
                            passfail_enrollment = {
                                "department_abbreviation": section["department_abbreviation"],
                                "course_number": section["course_number"],
                                "semester": section["semester"],
                                "section_year": section["section_year"],
                                "section_number": section["section_number"],
                                "student_id": student["_id"],
                                "enrollment_category_data": category,
                                "application_date": applicationDate
                            }
                            collection.insert_one(passfail_enrollment)
                            print("Passfail enrollment added.")
                    else:
                        print("Application date is in the future. Please try again.")
                if category != "passfail" and not "lettergrade":
                    print("Must enter either passfail or letter grade.")
        except Exception as e:
            print(e)


def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''

    while not found:
        abbreviation = input("Department's abbreviation --> ")

        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department found by that abbreviation_count.  Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department


def select_course(db):
    """
    Select a course by the combination of department abbreviation and course number
    :param db:      The connection to the database.
    :return:        The selected course.
    """
    # Create a connection to the courses collection from this database
    collection = db["courses"]
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = 0

    while not found:
        department_abbreviation = input("Department's abbreviation --> ")
        course_number = int(input("Course Number -->"))

        course_count: int = collection.count_documents({"department_abbreviation": department_abbreviation,
                                                        "course_number": course_number})
        found = course_count == 1
        if not found:
            print("No course was found with that department abbreviation and course number.  Try again.")
    found_course = collection.find_one({"department_abbreviation": department_abbreviation,
                                        "course_number": course_number})
    return found_course


def select_section(db):
    # Create a connection to the courses collection from this database
    collection = db["sections"]
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = 0
    section_number: int = 0
    section_year: int = 0
    semester: str = ''

    while not found:
        department_abbreviation = input("Department's abbreviation --> ")
        course_number = int(input("Course Number --> "))
        section_number = int(input("Section Number--> "))
        section_year = int(input("Section Year--> "))
        semester = input("Section semester --> ")

        section_count: int = collection.count_documents({"department_abbreviation": department_abbreviation,
                                                         "course_number": course_number,
                                                         "section_number": section_number,
                                                         "section_year": section_year,
                                                         "semester": semester})
        found = section_count == 1
        if not found:
            print(
                "No section was found with that department abbreviation, course number, or section number.  Try again.")
    found_section = collection.find_one({"department_abbreviation": department_abbreviation,
                                         "course_number": course_number,
                                         "section_number": section_number,
                                         "section_year": section_year,
                                         "semester": semester})
    return found_section


def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def select_major(db):
    majors = db["majors"]
    found: bool = False
    department_abbreviation: str = ''
    major_name: str = ''

    while not found:
        department_abbreviation = input("Department's abbreviation --> ")
        major_name = input("Major name -->")

        major_count: int = majors.count_documents({"department_abbreviation": department_abbreviation,
                                                   "name": major_name})
        found = major_count == 1
        if not found:
            print("No major was found with that department abbreviation and name.  Try again.")
    found_major = majors.find_one({"department_abbreviation": department_abbreviation,
                                   "name": major_name})
    return found_major


def delete_department(db):
    department = select_department(db)

    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    department_abbreviation = department["abbreviation"]
    courses = db["courses"]

    course_count: int = courses.count_documents({"department_abbreviation": department_abbreviation})

    if course_count > 0:
        print(f"Sorry, there are {course_count} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        deleted = departments.delete_one({"_id": department["_id"]})
        print(f"We just deleted: {deleted.deleted_count} departments.")


def delete_course(db):
    course = select_course(db)

    # Create a "pointer" to the students collection within the db database.
    courses = db["courses"]
    course_number = course["course_number"]
    department_abbreviation = course["department_abbreviation"]
    sections = db["sections"]

    section_count: int = sections.count_documents({"department_abbreviation": department_abbreviation,
                                                   "course_number": course_number})

    if section_count > 0:
        print(f"Sorry, there are {section_count} sections in that course.  Delete them first, "
              "then come back here to delete the course.")
    else:
        deleted = courses.delete_one({"_id": course["_id"]})
        print(f"We just deleted: {deleted.deleted_count} course(s).")


def delete_section(db):
    """
    Delete a section from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # section = select_section(db)
    #
    # # Create a "pointer" to the sections collection within the db database.
    # sections = db["sections"]
    # students = db["students"]
    #
    # student_count: int = sections.count_documents({"department_abbreviation": department_abbreviation,
    #                                                "course_number": course_number})
    section = select_section(db)

    # Create a "pointer" to the students collection within the db database.
    sections = db["sections"]
    department_abbreviation = section["department_abbreviation"]
    course_number = section["course_number"]
    section_number = section["section_number"]
    semester = section["semester"]
    section_year = section["section_year"]
    enrollments = db["enrollments"]

    student_count: int = enrollments.count_documents({
        "department_abbreviation": department_abbreviation,
        "course_number": course_number,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year})

    if student_count > 0:
        print(f"Sorry, there are {student_count} students in that section.  Delete them first, "
              "then come back here to delete the section.")
    else:
        deleted = sections.delete_one({"_id": section["_id"]})
        print(f"We just deleted: {deleted.deleted_count} section(s).")


def delete_student(db):
    student = select_student(db)

    students = db["students"]
    last_name = student["last_name"]
    first_name = student["first_name"]
    student_majors = db["student_majors"]

    stu_major_count: int = student_majors.count_documents({
        "last_name": last_name,
        "first_name": first_name})

    if stu_major_count > 0:
        print(f"Sorry, there are {stu_major_count} majors associated with that student.  Delete them first, "
              "then come back here to delete the student.")
    else:
        deleted = students.delete_one({"_id": student["_id"]})
        print(f"We just deleted: {deleted.deleted_count} students(s).")


def delete_student_section(db):
    """ Undeclare a student from a particular section.
    :param db:  The current database connection.
    :return:    None
    """
    print("Prompting you for the student and the section that they no longer have.")
    enrollments = db["enrollments"]
    student = select_student(db)
    section = select_section(db)

    deleted = enrollments.delete_one({"student_id": student["_id"],
                                      "department_abbreviation": section["department_abbreviation"],
                                      "course_number": section["course_number"],
                                      "section_number": section["section_number"],
                                      "semester": section["semester"],
                                      "section_year": section["section_year"]})

    print(f"We just deleted: {deleted.deleted_count} enrollments for specified student from section.")


def delete_section_student(db):
    """ Undeclare a section from a particular student.
    :param db:  The current database connection.
    :return:    None
    """
    print("Prompting you for the section and the student that they no longer will be enrolled in.")
    enrollments = db["enrollments"]
    student = select_student(db)
    section = select_section(db)

    deleted = enrollments.delete_one({"student_id": student["_id"],
                                      "department_abbreviation": section["department_abbreviation"],
                                      "course_number": section["course_number"],
                                      "section_number": section["section_number"],
                                      "semester": section["semester"],
                                      "section_year": section["section_year"]})

    print(f"We just deleted: {deleted.deleted_count} enrollments for specified section from student.")


def delete_student_major(db):
    student_majors = db["student_majors"]
    student = select_student(db)
    major = select_major(db)

    deleted_student_major = student_majors.delete_one({"student_id": student["_id"],
                                                       "major_name": major["name"]})
    print(f"We just deleted: {deleted_student_major.deleted_count} student from this major.")


def delete_major_student(db):
    student_majors = db["student_majors"]

    student = select_student(db)
    major = select_major(db)

    deleted_student_major = student_majors.delete_one({"student_id": student["_id"],
                                                       "major_name": major["name"]})
    print(f"We just deleted: {deleted_student_major.deleted_count} this major from this student.")


def delete_major(db):
    majors = db["majors"]
    major = select_major(db)
    student_majors = db["student_majors"]
    major_name = major["name"]

    student_count: int = student_majors.count_documents({"major_name": major_name})

    if student_count > 0:
        print(f"Sorry, there are {student_count} students in this major. Delete them first.")
    else:
        deleted = majors.delete_one({"_id": major["_id"]})
        print(f"We just deleted: {deleted.deleted_count} major.")


def list_department(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)
        print()


def list_course(db):
    courses = db["courses"].find({}).sort([("course_name", pymongo.ASCENDING)])

    for course in courses:
        pprint(course)
        print()


def list_section(db):
    sections = db["sections"].find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                             ("course_number", pymongo.ASCENDING),
                                             ("section_number", pymongo.ASCENDING)])

    for section in sections:
        pprint(section)
        print()


def list_student(db):
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING),
                                             ("eMail", pymongo.ASCENDING)])

    for student in students:
        pprint(student)
        print()


def list_major(db):
    majors = db["majors"].find({}).sort([("name", pymongo.ASCENDING)])

    for major in majors:
        pprint(major)
        print()


def list_student_major(db):
    student_majors = db["student_majors"].find({}).sort([("student_id", pymongo.ASCENDING)])

    for thingee in student_majors:
        pprint(thingee)
        print()


def list_major_student(db):
    major_students = db["student_majors"].find({}).sort([("student_id", pymongo.ASCENDING)])

    for thingee in major_students:
        pprint(thingee)
        print()


def list_enrollment(db):
    """
    List out all enrollment records sorted by department, course,
    section number.
    :param sess:    The current connection.
    :return:        None
    """
    enrollments = db["enrollments"].find({}).sort(
        [("department_name", pymongo.ASCENDING),
         ("course_number", pymongo.ASCENDING),
         ("section_year", pymongo.ASCENDING),
         ("last_name", pymongo.ASCENDING),
         ("first_name", pymongo.ASCENDING)
         ]
    )

    for enrollment in enrollments:
        pprint(enrollment)
        print()


def create_department_collection():
    # Create the department schema

    department_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'A specific division or unit within an educational institution, such as a university or college, that focuses on a particular field of study or discipline.',
            'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': 'string',
                    'description': 'given name of the department'
                },
                'abbreviation': {
                    'bsonType': 'string',
                    'description': 'condensed form of the name of the department',
                    'maxLength': 6
                },
                'chair_name': {
                    'bsonType': 'string',
                    'description': 'given name of the professor who performs administrative duties of specifed department',
                    'maxLength': 80
                },
                'building': {
                    'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                    'description': 'given name of building can only be one of the enum values and is required'
                },
                'office': {
                    'bsonType': 'int',
                    'description': 'integer number that identifies the specific office of department'
                },
                'description': {
                    'bsonType': 'string',
                    'description': 'constructed insight and overview of what the department serves',
                    'maxLength': 80
                }
            }
        }
    }

    # try:
    #     db.create_collection("departments")
    # except Exception as e:
    #     print(e)

    # collMod command on the departments collection is used to modify properties of an existing collection
    # when this command is executed, the departments schema will be set as the validator for the collection.
    # db.command("collMod", "departments", validator=department_validator)
    # print("department validator added to the departments collection in the database.")

    if "departments" not in db.list_collection_names():
        db.create_collection("departments", validator=department_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        db.command("collMod", "departments", validator=department_validator)

    db['departments'].create_index([('name', pymongo.ASCENDING)], unique=True)
    db['departments'].create_index([('abbreviation', pymongo.ASCENDING)], unique=True)
    db['departments'].create_index([('chair_name', pymongo.ASCENDING)], unique=True)
    db['departments'].create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], unique=True)


def create_course_collection():
    course_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'Classes offered by a department that are taken by students. Courses are usually part of a program that leads to a college degree/certificate.',
            'required': ["department_abbreviation", 'course_name', 'course_number', 'description', 'units'],
            'properties': {
                '_id': {},
                'department_abbreviation': {
                    'bsonType': 'string',
                    'description': 'condensed form of the name of the course department'
                },
                'course_name': {
                    'bsonType': 'string',
                    'description': 'given name of the course'
                },
                'course_number': {
                    'bsonType': 'int',
                    'description': 'a unique integer that identifies a specific class within one department',
                    "minimum": 100,
                    "maximum": 699
                },
                'description': {
                    'bsonType': 'string',
                    'description': 'constructed insight and overview of what the course serves'
                },
                'units': {
                    'bsonType': 'int',
                    'description': 'the amount of academic work required to earn a degree represented as one integer from 1 to 5',
                    "minimum": 1,
                    "maximum": 5
                }
            }
        }
    }

    if "courses" not in db.list_collection_names():
        db.create_collection("courses", validator=course_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        db.command("collMod", "courses", validator=course_validator)

    # Uniqueness Constraints
    db['courses'].create_index([('department_abbreviation', pymongo.ASCENDING), ('course_name', pymongo.ASCENDING)],
                               unique=True)
    db['courses'].create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
                               unique=True)


def create_major_collection():
    major_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'A specific field of study that a student chooses to focus on during their undergraduate education.',
            'required': ['name', 'description', 'department_abbreviation'],
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': 'string',
                    'description': 'given name of the major'
                },
                'description': {
                    'bsonType': 'string',
                    'description': 'constructed insight and overview of what the course serves'
                },
                'department_abbreviation': {
                    'bsonType': 'string',
                    'description': 'condensed form of the name of the department this major is from'
                }
            }
        }
    }

    if "majors" not in db.list_collection_names():
        db.create_collection("majors", validator=major_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        db.command("collMod", "majors", validator=major_validator)
    db['majors'].create_index([('name', pymongo.ASCENDING)], unique=True)


def create_section_collection():
    section_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'An offering of a Course in a specific place and time.',
            'required': ['department_abbreviation', 'course_number', 'section_number', 'semester', 'section_year',
                         'building', 'room', 'schedule', 'start_time', 'instructor'],
            'properties': {
                '_id': {},
                'department_abbreviation': {
                    'bsonType': 'string',
                    'description': 'condensed form of the name of the department and is required',
                    'maxLength': 6
                },
                'course_number': {
                    'bsonType': 'int',
                    'description': 'digit value to identify specific course and is required'
                },
                'section_number': {
                    'bsonType': 'int',
                    'description': 'digit value to identify specific class session of course and is required'
                },
                'semester': {
                    'enum': ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II', 'Summer III'],
                    'description': 'given term can only be one of the enum values and is required'
                },
                'section_year': {
                    'bsonType': 'int',
                    'description': 'what academic year the specific course section is being taught and is required'
                },
                'building': {
                    'enum': ['NAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4',
                             'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                    'description': 'given name of building can only be one of the enum values and is required'
                },
                'room': {
                    'bsonType': 'int',
                    'description': 'specific location space within building and is required',
                    'minimum': 1,
                    'maximum': 999
                },
                'schedule': {
                    'enum': ['MW', 'MWF', 'TuTh', 'F', 'S'],
                    'description': 'given sets of the days of the week can '
                                   'only be one of the enum values and is required'
                },
                'start_time': {
                    'bsonType': 'int',
                    'description': 'time of when course section begins which must be between the time of '
                                   '800 am to 730pm (1930) and is required',
                    'minimum': 800,
                    'maximum': 1930
                },
                'instructor': {
                    'bsonType': 'string',
                    'description': 'time of when course section begins and is required',
                    'maxLength': 80
                },
            }
        }
    }
    if "sections" not in db.list_collection_names():
        db.create_collection("sections", validator=section_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        db.command("collMod", "departments", validator=section_validator)

    # Uniqueness Constraints
    db['sections'].create_index([('course', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING),
                                 ('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING)], unique=True)

    db['sections'].create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                                 ('schedule', pymongo.ASCENDING), ('start_time', pymongo.ASCENDING),
                                 ('building', pymongo.ASCENDING), ('room', pymongo.ASCENDING)], unique=True)

    db['sections'].create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                                 ('schedule', pymongo.ASCENDING), ('start_time', pymongo.ASCENDING),
                                 ('instructor', pymongo.ASCENDING)], unique=True)

    # ensuring that no student can be enrolled in more than one section of the same course during the same term
    db['sections'].create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                                 ('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING),
                                 ('student_id', pymongo.ASCENDING)], unique=True)

    print("created uniqueness section constraints.")


def create_student_collection():
    # Create the student schema

    student_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'An individual who may or may not be enrolled at the university, who enrolls in '
                           'courses toward some educational objective.  That objective could be a formal '
                           'degree program, or it could be a specialized certificate.',
            'required': ['last_name', 'first_name', 'eMail'],
            'properties': {
                '_id': {},
                'first_name': {
                    'bsonType': 'string',
                    'description': 'given name of the student',
                    'maxLength': 50
                },
                'last_name': {
                    'bsonType': 'string',
                    'description': 'surname of the student',
                    'maxLength': 50
                },
                'eMail': {
                    'bsonType': 'string',
                    'description': 'electronic mail address of the student',
                    'maxLength': 255
                }
            }
        }
    }

    if "students" not in db.list_collection_names():
        db.create_collection("students", validator=student_validator)
    else:
        # collMod command on the departments collection is used to modify properties of an existing collection
        # when this command is executed, the departments schema will be set as the validator for the collection.
        db.command("collMod", "students", validator=student_validator)

    # Uniqueness Constraints
    db['students'].create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)], unique=True)
    db['students'].create_index([('eMail', pymongo.ASCENDING)], unique=True)

    print("student uniqueness constraints added to students collection")


def create_enrollment_collection():
    enrollment_category_data = {
        'oneOf': [
            # Pass_Fail Needs application date
            {
                'bsonType': 'object',
                'required': ['application_date'],
                'additionalProperties': False,
                'properties': {
                    'application_date': {
                        'bsonType': 'BITC',
                        'description': 'The day month and year that the student applied for pass fail grading'
                    }
                }
            },
            # Letter Grade Needs minimum satisfactory grade
            {
                'bsonType': 'object',
                'required': ['min_satisfactory_grade'],
                'additionalProperties': False,
                'properties': {
                    'min_satisfactory_grade': {
                        'bsonType': 'string',
                        'enum': ['A', 'B', 'C']
                    }
                }
            }
        ]
    }

    enrollment_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A specific instance of a student enrolling into a specific section.',
            'required': ["department_abbreviation", "course_number", "section_number", "semester", "section_year",
                         " student_id", "enrollment_category_data"],
            'properties': {
                '_id': {},
                'department_abbreviation': {
                    'bsonType': 'string',
                    'maxLength': 6,
                    'description': 'a shortened name given to the department'

                },
                'course_number': {
                    'bsonType': 'int',
                    'minimum': 100,
                    'maximum': 699,
                    'description': 'value used to identify specific course and is required'

                },
                'section_number': {
                    "bsonType": 'serial',
                    "description": 'used to identify which specific course'
                },
                'semester': {
                    'enum': ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II', 'Summer III'],
                    'description': 'given term can only be one of the enum values and is required'
                },
                'section_year': {
                    'bsonType': 'int',
                    'description': 'what academic year the specific course section is being taught and is required'

                },
                'student_id': {
                    'bsonType': 'serial',
                    'description': 'used to identify which specific student'
                },
                'enrollment_category_data': enrollment_category_data
            }
        }
    }
    try:
        db.create_collection("enrollments")
    except Exception as e:
        print(e)
    db.command("collMod", "enrollments", validator=enrollment_validator)
    print("enrollment validator added to the enrollments collection in the database.")

    db['enrollments'].create_index([('section_number', pymongo.ASCENDING), ('student_id', pymongo.ASCENDING)],
                                   unique=True)
    db['enrollments'].create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                                    ('department_abbreviation', pymongo.ASCENDING),
                                    ('course_number', pymongo.ASCENDING),
                                    ('student_id', pymongo.ASCENDING)], unique=True)


def create_student_majors_collection():
    student_majors_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'A list of individuals and their choices of fields of study.',
            'required': ['major_name', 'department_abbreviation', 'student_id', 'declaration_date',
                         'student_first_name', 'student_last_name'],
            'properties': {
                '_id': {},
                'major_name': {
                    'bsonType': 'string',
                    'description': 'The given name of the department'

                },
                'department_abbreviation': {
                    'bsonType': 'string',
                    'description': 'A shorthand version of the name of a department'
                },
                'student_id': {
                    'description': 'A computer-generated surrogate key created in MongoDB'
                },
                'declaration_date': {
                    'bsonType': 'date',
                    'description': 'The time which the student declared the major.'
                },
                'student_first_name': {
                    'bsonType': 'string',
                    'description': 'The given name of a student.'
                },
                'student_last_name': {
                    'bsonType': 'string',
                    'description': 'The surname of a student.'
                }

            }
        }
    }

    if "student_majors" not in db.list_collection_names():
        db.create_collection("student_majors", validator=student_majors_validator)
        db.command("collMod", "student_majors", validator=student_majors_validator)
    db['student_majors'].create_index([('major_name', pymongo.ASCENDING), ('student_id', pymongo.ASCENDING)],
                                      unique=True)
    db['student_majors'].create_index([('department_abbreviation', pymongo.ASCENDING)])


if __name__ == '__main__':
    cluster = f"mongodb+srv://zacharyhunt01:good21dead@cluster0.7kkplej.mongodb.net/"
    print(f"mongodb+srv://zacharyhunt01:<password>@cluster0.7kkplej.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)

    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())

    # db will be the way that we refer to the database from here on out.
    db = client["ProjectRun"]

    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # set up departments schema
    #create_department_collection()

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)


