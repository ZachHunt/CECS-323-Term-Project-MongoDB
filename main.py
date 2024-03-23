
import dis
import pymongo
from pymongo import ASCENDING, MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from menu_definitions import role_menu
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
from datetime import datetime

# basic menu functions
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

# for opening menu for roles
def choose_roles(db):
    choose_action: str =''
    #while choose_action != role_menu.last_action():
    choose_action = role_menu.menu_prompt()
    return choose_action

#just returns role
def role_return(role):
    return role


#add a student      
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
    discord_user: str = ''
    student_id: int = 0
    role: str = ''

    

    while True:
        try:
            last_name = input("Last name --> ")
            first_name = input("First name --> ")
            student_id = int(input("Student ID --> "))
            eMail = input("Student eMail --> ")
            discord_user = input("Discord Username --> ")
            role = choose_roles(db)
            print(role)

            name_count = collection.count_documents({"last_name": last_name, "first_name": first_name})
            unique_name = name_count == 0

            if not unique_name:
                print("We already have a student with that last and first name.  Try again.")
                continue

            id_count = collection.count_documents({"student_id": student_id})
            unique_id = id_count == 0

            if not unique_id:
                print("We already have a student with that ID.  Try again.")
                continue


            email_count = collection.count_documents({"eMail": eMail})
            unique_email = email_count == 0

            if not unique_email:
                print("We already have a student with that email.  Try again.")
                continue

            #discord_count = collection.count_documents({"discord_user": discord_user})
            #unique_discord = discord_count == 0
            
            #if not unique_discord:
            #    print("We already have someone with that discord username. Try again.")
            #    continue
            
            student = {
                "last_name": last_name,
                "first_name": first_name,
                "student_id": student_id,
                "eMail": eMail,
                "discord_user": discord_user,
                "role": role
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

# remove student
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

# List student
def list_student(db):
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING),
                                             ("student_id", pymongo.ASCENDING),
                                             ("eMail", pymongo.ASCENDING),
                                             ("discord_user", pymongo.ASCENDING),
                                             ("role", pymongo.ASCENDING)])

    for student in students:
        pprint(student)
        print()
        
# MongoDB Collections
def create_student_collection():
    # Create the student schema

    student_validator = {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'An individual who is participating in the marina hacks competition ',
            'required': ['last_name', 'first_name', 'student_id', 'eMail', 'discord_user', 'role'],
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
                'student_id': {
                    'bsonType': 'int',
                    'description': 'unique identification number of the student',
                    'maxLength': 20
                },
                'eMail': {
                    'bsonType': 'string',
                    'description': 'electronic mail address of the student',
                    'maxLength': 255
                },
                'discord_user': {
                    'bsonType': 'string',
                    'description': 'discord user name of student',
                    'maxLength': 50
                },
                'role': {
                    'enum': ['Hacker', 'Commitee_Member', 'Sponsor', 'Guest_Speaker', 'Judge'],
                    'description': 'what role will the student play during marina hacks competition',
                    'maxLength': 50
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
    db['students'].create_index([('student_id', pymongo.ASCENDING)], unique=True)
    db['students'].create_index([('eMail', pymongo.ASCENDING)], unique=True)
    db['students'].create_index([('discord_user', pymongo.ASCENDING)])
    db['students'].create_index([('role', pymongo.ASCENDING)])
    
    print("student uniqueness constraints added to students collection")
        
if __name__ == '__main__':
    cluster = f"mongodb+srv://zacharyhunt01:good21dead@cluster0.7kkplej.mongodb.net/"
    print(f"mongodb+srv://zacharyhunt01:<password>@cluster0.7kkplej.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)

    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())

    # db will be the way that we refer to the database from here on out.
    db = client["MarinaHacksCollection"]

    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # set up departments schema
    #create_department_collection()

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)