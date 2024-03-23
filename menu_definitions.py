from Menu import Menu
from Option import Option
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(db)"),
    Option("List", "list_objects(db)"),
    Option("Delete", "delete(db)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    #Option("Department", "add_department(db)"),
    #Option("Course", "add_course(db)"),
    #Option("Major", "add_major(db)"),
    Option("Student", "add_student(db)"),
    #Option("Section", "add_section(db)"),
    #("Student to Major", "add_student_major(db)"),
    #Option("Major to Student", "add_major_student(db)"),
    #Option("Student to Section", "add_student_section(db)"),
    #Option("Section to Student", "add_section_student(db)"),
    # Option("Student to PassFail", "add_student_PassFail(db)"),
    # Option("Student to LetterGrade", "add_student_LetterGrade(db)"),
    Option("Exit", "pass")
])


role_menu = Menu('role', 'Please indicate your role:', [
    Option("Hacker", "Hacker"),
    Option("Commitee Member", "Commitee_Member"),
    Option("Sponsor", "Sponsor"),
    Option("Guest Speaker", "Guest_Speaker"),
    Option("Judge", "Judge")
])




delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    #Option("Department", "delete_department(db)"),
    #Option("Course", "delete_course(db)"),
    #Option("Major", "delete_major(db)"),
    Option("Student", "delete_student(db)"),
    #Option("Section", "delete_section(db)"),
    #Option("Student to Major", "delete_student_major(db)"),
    #Option("Major to Student", "delete_major_student(db)"),
    #Option("Student to Section", "delete_student_section(db)"),
    #Option("Section to Student", "delete_section_student(db)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    #Option("Department", "list_department(db)"),
    #Option("Course", "list_course(db)"),
    #Option("Major", "list_major(db)"),
    Option("Student", "list_student(db)"),
    #Option("Section", "list_section(db)"),
    #Option("Student to Major", "list_student_major(db)"),
    #Option("Major to Student", "list_major_student(db)"),
    #Option("Student to Section", "list_enrollment(db)"),
    #Option("Section to Student", "list_enrollment(db)"),
    # Option("Enrollment", "list_enrollment(db)"),
    Option("Exit", "pass")
])
"""
schedule_menu = Menu('schedule', 'Please indicate the section schedule:', [
    Option("Monday/Wednesday", "MW"),
    Option("Monday/Wednesday/Friday", "MWF"),
    Option("Tuesday/Thursday", "TuTh"),
    Option("Friday only", "F"),
    Option("Saturday only", "S"),
    Option("test bogus", "LOL")
])

semester_menu = Menu('semester', 'Please indicate the section semester:', [
    Option("Fall", "Fall"),
    Option("Spring", "Spring"),
    Option("Winter", "Winter"),
    Option("Summer I", "Summer I"),
    Option("Summer II", "Summer II"),
    Option("Summer III", "Summer III")
])

letter_grade_menu = Menu('letter_grade', 'Please select one of the valid letter grades:', [
    Option("A", "A"),
    Option("B", "B"),
    Option("C", "C"),
    Option("D", "D"),
    Option("F", "F")
])
"""
# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
