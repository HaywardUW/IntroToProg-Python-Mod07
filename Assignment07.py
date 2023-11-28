# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Kyle Hayward, 11/28/2023, Completed Script
# ------------------------------------------------------------------------------------------ #

# Import the json module
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # A table of student data
menu_choice: str  = '' # Holds the choice made by the user

# Creating the Person Class
class Person:
    """
    A class representing data pertaining to a person.

    Properties:
        first_name - The student's first name.
        last_name - The student's last name.

    ChangeLog:
    Kyle Hayward, 11/28/2023, Created the class.
    """

    # Creating the constructor with private attributes for first_name and last_name
    def __init__(self, first_name = '', last_name = ''):
        self.first_name = first_name
        self.last_name = last_name

    # Creating the property getter for first_name
    @property
    def first_name(self):
        return self.__first_name.title()

    # Creating the property setter for the first_name
    @first_name.setter
    def first_name(self, value):
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should only contain letters.")

    # Creating the property getter for last_name
    @property
    def last_name(self):
        return self.__last_name.title()

    # Creating the property setter for last_name
    @last_name.setter
    def last_name(self, value):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should only contain letters.")

    # Overriding the __str__() method to return a coma-seperated string of data
    def __str__(self):
        return f'{self.first_name},{self.last_name}'

# Creating the Student class which inherits code from the Person class
class Student(Person):
    """
    A class representing student data.

    Properties:
        first_name - The student's first name.  # Inherited from the Person class
        last_name - The student's last name.  # Inherited from the Person class
        course_name - The course in which is being registered for.
    
    ChangeLog:
    Kyle Hayward, 11/28/2023, Created the class.
    """

    # Creating the constructor with private attributes including course_name
    def __init__(self, first_name='', last_name='', course_name=''):
        # Passing parameter data to the Person "super" class
        super().__init__(first_name = first_name, last_name = last_name)
        self.course_name = course_name

    # Creating the property getter for course_name
    @property
    def course_name(self):
        return self.__course_name.title()
    
    # Creating the property setter for course_name
    @course_name.setter
    def course_name(self, value):
        if value.isalpha() or not value.isalpha() or value == "":  # Essentially letting any data input here
            self.__course_name = value         
        else:
            raise ValueError("There was a non-specific error.")
            
    # Overriding the default __str__() method behavior to return a coma-seperated string of data
    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #

# Defining the file processing class
class FileProcessor:
    """
    A set of processing functions that reads from and writes to JSON files.

    ChaneLog: (Who, When, What)
    Kyle Hayward, 11/21/2023, Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ 
        This function opens the JSON file and loads the data into a list of dictionary rows

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created Function
        Kyle Hayward, 11/28/2023, Converted json dictionary objects to a list of student objects
        """

        try:
            # Open file in read mode
            file = open(file_name, 'r')
            # List of json dictionary objects
            list_of_dict_data = json.load(file)
            # Convert json dict objects to student objects
            for student in list_of_dict_data:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)
            file.close()
        # Error handling to create a file if it does not exist
        except FileNotFoundError as e:
            print()
            print('*' * 50)
            IO.output_error_messages(message="The file doesn't exist!"
                                             "\nCreating the file."
                                             "\nFile has been created.")
            print('*' * 50)
            # Creates the "Enrollments" JSON file
            file = open(FILE_NAME, 'w')
        # Catch all exception error handling
        except Exception as e:
            IO.output_error_messages(message="There was a non-specific error!",
                                     error=e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes student list data to the JSON file and presents data to the user.
            While this function also contains presentation data, it is still largely a File Processing function.

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created Function
        Kyle Hayward, 11/28/2023, Converted list of student objects to json compatible list of dictionaries.
        """

        try:
            # Creating a new empty list to hold json data
            list_of_dict_data = []
            # Converting list of student objects to json compatible list of dictionaries
            for student in student_data:
                student_json = {"FirstName": student.first_name, 
                                "LastName": student.last_name, 
                                "CourseName": student.course_name}
                # Appending data to the newly created list
                list_of_dict_data.append(student_json)
            # Open "Enrollments.json" and writes the student list data to it
            file = open(file_name, "w")
            # Changing the first argument to be the list of dict data
            json.dump(list_of_dict_data, file)
            file.close()

            print()
            print('*' * 50)
            print("The following data is saved: \n")
            # Loops through the students list and prints each row
            for student in student_data:
                print(f'{student.first_name}, '
                      f'{student.last_name}, '
                      f'{student.course_name}!')
            print('*' * 50)

        except TypeError as e:
            IO.output_error_messages(message="Please validate the data is in valid JSON format.",
                                     error=e)
        except Exception as e:
            IO.output_error_messages(message="There was a non-specific error.",
                                     error=e)
        finally:
            if not file.closed:
                file.close()


################################################
# -- Present the Data (Input/Output) --#

# Defining the presentation input/output class
class IO:
    """
    A set of presentation functions that manages user input and output

    ChangeLog: (Who, When, What)
    Kyle Hayward, 11/21/2023, Created CLass
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error message to the user

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created Function
        :return: None
        """

        print(message, end="\n\n")
        if error is not None:
            print("Technical Error Message")
            print(error,
                  error.__doc__,
                  type(error),
                  sep="\n")

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of options to the user

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created Function

        :return: None
        """

        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """ This function receives the menu selection from the user

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created Function

        :return: A string with the users menu selection
        """

        choice = "0"
        try:
            print('*' * 50)
            choice = input("Enter your menu selection: ")
            print('*' * 50)
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose menu option 1, 2, 3, or 4.")
        except Exception as e:
            IO.output_error_messages(e.__str__())

        return choice

    @staticmethod
    def output_student_data(student_data: list):
        """ This function displays all data contained in the students list

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2016, Created Function

        :return: None
        """

        # Checks whether or not initial data exists in the json file
        if not student_data:
            print()
            print('*' * 50)
            print("There is currently no data to display.")
            print("Please choose menu option 1 to enter data.")
            print('*' * 50)
        # Loops through the list and prints all the data
        else:
            print()
            print('*' * 50)
            print("The current data is: \n")
            for student in student_data:
                print(f'{student.first_name}, '
                      f'{student.last_name}, '
                      f'{student.course_name}')
            print('*' * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function prompts for and stores student's first name, last name and course data

        ChangeLog: (Who, When, What)
        Kyle Hayward, 11/21/2023, Created function
        Kyle Hayward, 11/28/2023, Updated to use a student object rather than dictionary

        :return: None
        """

        try:
            # Creating a new student object using each property's validation code
            print()
            print('*' * 50)
            student = Student()  # Using default empty string arguments
            student.first_name = input("Please enter the student's first name: ")
            student.last_name = input("Please enter the student's last name: ")
            student.course_name = input("Please enter the course name: ")
            student_data.append(student)

            # Print the data that has been registered
            print()
            print('*' * 50)
            print()
            print(f'You have registered '
                  f'{student.first_name} '
                  f'{student.last_name} for '
                  f'{student.course_name}!\n')
            print('*' * 50)

        except ValueError as e:
            IO.output_error_messages(message="That is not the correct type of data!",
                                     error=e)
        except Exception as e:
            IO.output_error_messages(message="There was a non-specific error!",
                                     error=e)
        return student_data

# End of function definitions

################################################
# -- Main body of the script --#


students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Repeating the following tasks
while True:
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Register a student for a course
    if menu_choice == "1":
        IO.input_student_data(student_data=students)
        continue

    # Show current registration data
    elif menu_choice == "2":
        IO.output_student_data(student_data=students)
        continue

    # Save data to file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Exit the program
    elif menu_choice == "4":
        break

print()
print('*' * 50)
print("The program has exited!")
print('*' * 50)
