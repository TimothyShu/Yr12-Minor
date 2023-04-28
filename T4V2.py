import FileManager
from random import randint
from itertools import chain, product

#This is for emails
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import smtplib

employer_fieldname = ["Name", "Address", "Work Status", "Active Positions"]
employee_fieldname = ["Name", "Address", "Occupation"]

Base_Employer_ID = 000000
Base_Employee_ID = 100000
letter = "abcdefghijklmnopqrstuvwxyz"

work_status_options = ["On site", "Off site", "Both"]
resume = ["resume1", "resume2", None]
resumeStatement = ["Statement1", "Statement2", None]
TF = [True, False]
list_names = ["".join(perm) for perm in chain.from_iterable(product(letter, repeat=i) for i in range(1, 4))]

class EMPLOYER:
    def __init__(self, Name, location, work_status, ID=None, Looking_For_Position=False, Email=None) -> None:
        self.Name = Name
        self.Address = location
        self.Work_status = work_status
        self.Looking_For_Position = Looking_For_Position
        self.ID = ID
        self.Email = Email
        if self.ID == None:
            self.New = True
        else:
            self.New = False
    
    
    def Add_Employer(self, Employers):
        if self.New == False:
            return
        if len(Employers) == 1:
            self.ID = Base_Employer_ID
            return
        last_ID = Employers[-2].ID
        self.ID = last_ID + 1
        self.New = False

class EMPLOYEE:
    def __init__(self, Name, Address, Occupation = None, ID = None, Resume = None, ResumeStatement = None, Email=None) -> None:
        self.Name = Name
        self.Address = Address
        self.Occupation = Occupation
        self.Resume = Resume
        self.ResumeStatement = ResumeStatement
        self.ID = ID
        self.Email = Email
        if self.ID == None:
            self.New = True
        else:
            self.New = False

    def Add_Employee(self, Employees) -> None:
        if self.New == False:
            return
        if len(Employees) == 1:
            self.ID = Base_Employee_ID
            return
        last_ID = Employees[-2].ID
        self.ID = last_ID + 1
        self.New = False


def Load_Employers() -> list:
    employers = []

    #Loop through all attributes
    Workbook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    #This opens the workbook
    Employers = Workbook["Employers"]

    row = 1
    cell = Employers.cell(row = 1, column = 2).value
    while cell:
        #loop through the whole row
        column = [Employers.cell(row = row, column = ind).value for ind in range(1,7)]
        employers.append(column)
        row += 1
        cell = Employers.cell(row = row, column = 2).value

    Workbook.close()

    for ind, Employer in enumerate(employers):
        employers[ind] = Read_Employer(Employer)

    return employers

def Read_Employer(Employer) -> EMPLOYER:
    return EMPLOYER(Employer[1], Employer[2], Employer[3], Employer[0], Employer[4], Employer[5])

def Update_Employer(ID, Employers) -> None:
    WorkBook, filepath = FileManager.GetFile("T4Dir", "Data_Store.xlsx", True)
    Employersheet = WorkBook["Employers"]
    row = Find_ID(ID, Employersheet)
    index = row -1
    Employer = Employers[index]
    #Add all the columns based on the value
    if Employer.New == True:
        Employer.Add_Employer(Employers)
    Employersheet.cell(row=row, column=1).value = Employer.ID
    Employersheet.cell(row=row, column=2).value = Employer.Name
    Employersheet.cell(row=row, column=3).value = Employer.Address
    Employersheet.cell(row=row, column=4).value = Employer.Work_status
    Employersheet.cell(row=row, column=5).value = Employer.Looking_For_Position
    Employersheet.cell(row=row, column=6).value = Employer.Email
    WorkBook.save(filepath)
    WorkBook.close()

def load_Employees() -> list:

    employees = []

    Workbook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    Employees = Workbook["Employees"]

    row = 1
    cell = Employees.cell(row = 1, column = 1).value
    while cell:
        #loop through the whole row
        column = [Employees.cell(row = row, column = ind).value for ind in range(1,8)]
        employees.append(column)
        row += 1
        cell = Employees.cell(row = row, column = 1).value

    Workbook.close()

    for ind, Employee in enumerate(employees):
        employees[ind] = Read_Employees(Employee)
    
    return employees

def load_Employee(ID):
    wb = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    ws = wb["Employees"]
    row = Find_ID(ID, ws)
    return [ws.cell(row = row, column = ind).value for ind in range(1,8)]

def load_Employer(ID):
    wb = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    ws = wb["Employers"]
    row = Find_ID(ID, ws)
    return [ws.cell(row = row, column = ind).value for ind in range(1,7)]

def Read_Employees(Employee) -> EMPLOYEE:
    return EMPLOYEE(Employee[1], Employee[2], Employee[3], Employee[0], Employee[4], Employee[5], Employee[6])

def Update_Employee(ID,Employees) -> list:
    WorkBook, filepath = FileManager.GetFile("T4Dir", "Data_Store.xlsx", True)
    Employeesheet = WorkBook["Employees"]
    row = Find_ID(ID, Employeesheet)
    index = row -1
    Employee = Employees[index]
    #Add all the columns based on the value
    if Employee.New == True:
        Employee.Add_Employee(Employees)
    Employeesheet.cell(row=row, column=1).value = Employee.ID
    Employeesheet.cell(row=row, column=2).value = Employee.Name
    Employeesheet.cell(row=row, column=3).value = Employee.Address
    Employeesheet.cell(row=row, column=4).value = Employee.Occupation
    Employeesheet.cell(row=row, column=5).value = Employee.Resume
    Employeesheet.cell(row=row, column=6).value = Employee.ResumeStatement
    Employeesheet.cell(row=row, column=7).value = Employee.Email
    WorkBook.save(filepath)
    WorkBook.close()

def Find_ID(ID, Worksheet) -> int:
    row = 1
    while Worksheet.cell(row = row, column = 2).value:
        if Worksheet.cell(row = row, column = 1).value == ID:
            return row
        row += 1
    return row

def Find_Username(username, Worksheet) -> int:
    row = 1
    while Worksheet.cell(row = row, column = 2).value:
        if Worksheet.cell(row = row, column = 2).value == username:
            return row
        row += 1
    return row

def Create_Account():
    #Either employer or employee account
    option = input("Are you an employee or an employer?").lower()
    while option:
        if option == "employee":
            Create_Employee_Account()
            break
        elif option == "employer":
            Create_Employer_Account()
            break
        else:
            option = input("Are you an employee or an employer?").lower()

def Login_Account():
    tries = 0
    username = input("What is your username?\n: ")
    password = input("What is your password?\n: ")
    while username and tries < 4:
        valid, userID = Check_Login_Details(username, password)
        if valid == True:
            if userID >= 100000:
                #This is an employee
                Login_Employee(userID)
            else:
                #This is an employer
                Login_Employer(userID)
            break
        else:
            tries += 1
            username = input("What is your username?\n: ")
            password = input("What is your password?\n: ")

def Login_Employee(userID):
    #Load their account
    print(f"You're logged into the account with ID {userID}")
    Account = load_Employee(userID)
    print(f"Your username: {Account[1]}")
    print(f"Your address: {Account[2]}")
    print(f"Your Current Occupation: {Account[3]}")
    print(f"Your Resume: {Account[4]}")
    print(f"Your ResumeStatement: {Account[5]}")
    print(f"Your email: {Account[6]}")
    Account = EMPLOYEE(Account[1], Account[2], Account[3], userID, Account[4], Account[5], Account[6])
    Filter = []
    option = input("1. update Resume\n2. find Employers\n3. add filter\n4. delete filter\n: ")
    if len(Filter) == 0:
        print("Filters: None")
    else:
        print(f"Filters: {', '.join([filt.Name for filt in Filter])}")
    while option:
        if option == "1":
            UpdateResume(userID)
        elif option == "2":
            FindEmployers(Filter, Account)
        elif option == "3":
            Filter = Create_Employer_Filter()
        elif option == "4":
            Filter = []
        option = input("1. update Resume\n2. find Employers\n3. add filter\n4. delete filter\n: ")
        if len(Filter) == 0:
            print("Filters: None")
        else:
            print(f"Filters: {', '.join([filt.Name for filt in Filter])}")
    pass



def Login_Employer(userID):
    #Load their account
    print(f"You're logged into the account with ID {userID}")
    Account = load_Employer(userID)
    print(f"Your username: {Account[1]}")
    print(f"Your address: {Account[2]}")
    print(f"Your work status: {Account[3]}")
    print(f"Your looking for position: {Account[4]}")
    print(f"Your email: {Account[5]}")
    Account = EMPLOYER(Account[1], Account[2], Account[3], userID, Account[4], Account[5])
    Filters = []
    option = input("1. find Employees\n2. add filters:\n3. delete filters\n: ")
    if len(Filters) == 0:
        print("Filters: None")
    else:
        print(f"Filters: {', '.join([filt.Name for filt in Filters])}")
    while option:
        if option == "1":
            FindEmployees(Filters, Account)
        elif option == "2":
            Filters = Create_Employee_Filter()
            pass
        elif option == "3":
            Filters = []
        option = input("1. find Employees\n2. add filters\n3. delete filters\n: ")
        if len(Filters) == 0:
            print("Filters: None")
        else:
            print(f"Filters: {', '.join([filt.Name for filt in Filters])}")
    pass

def FindEmployees(Filters, Employer):
    #Applying the filter
    Employee_list = Employees[:]
    for filter in Filters:
        Employee_list = filter.Filter(Employee_list)


    for ind, Employee in enumerate(Employee_list):
        print(f"{ind}. {Employee.Name}")
    option = input("Select an Employee that you want information on\n: ")
    while option:
        try:
            num = int(option)
        except ValueError:
            print("That is not a number")
            continue
        try:
            Employee = Employee_list[num]
        except IndexError:
            print("That is not a correct number")
            continue
        ShowEmployee(Employee, Employer)
        option = input("Select an Employee that you want information on\n: ")

def ShowEmployee(Employee, Employer):
    print("Details of Employee")
    print(f"Name: {Employee.Name}")
    print(f"Address: {Employee.Address}")
    print(f"Occupation: {Employee.Occupation}")
    print(f"Resume: {Employee.Resume}")
    print(f"Resume statement: {Employee.ResumeStatement}")
    print(f"email: {Employee.Email}")
    option = input("Do you want to email this employee?")
    while option:
        if option == "y":
            Bot.Email_Employee(employee=Employee, employer=Employer)
            print("Email successful")
        option = input("Do you want to email this employee?")

def UpdateResume(userID):
    Employee = Get_Employee(userID)
    resume = Get_Resume()
    option = input("Do you want to confirm?\n: ").lower()
    while option:
        if option == "yes":
            Employee.Resume = resume
            #update the employee account
            Update_Employee(userID, Employees)
            print(f"Your new resume: {Employee.Resume}")
            return
        option = input("Do you want to confirm?\n: ").lower()
    pass

def FindEmployers(Filter, Employee):

    Employer_list = Employers[:]
    for filter in Filter:
        Employer_list = filter.Filter(Employer_list)


    for ind, Employer in enumerate(Employer_list):
        print(f"{ind}. {Employer.Name}")
    option = input("Select an employment agency by the number infront of their name\n: ")
    while option:
        try:
            num = int(option)
        except ValueError:
            print("That is not a number")
            continue
        try:
            Employer = Employer_list[num]
        except IndexError:
            print("That is not a correct number")
            continue
        ShowEmployer(Employer, Employee)
        option = input("Select an employment agency by the number infront of their name\n: ")

def ShowEmployer(Employer, Employee):
    print("Details of Employer")
    print(f"Name: {Employer.Name}")
    print(f"address: {Employer.Address}")
    print(f"Work Status: {Employer.Work_status}")
    print(f"Looking for position: {Employer.Looking_For_Position}")
    print(f"email: {Employer.Email}")
    option = input("Do you want to email this employer?")
    while option:
        if option == "y":
            Bot.Email_Employer(Employer, Employee)
            print("Email successful")
        option = input("Do you want to email this employer?")

def Get_Employee(ID):
    for Employee in Employees:
        if Employee.ID == ID:
            return Employee
    else:
        return None

def Check_Login_Details(username, password):
    Workbook = FileManager.GetFile("T4Dir", "Login_Details.xlsx")
    Worksheet = Workbook["Details"]
    row = Find_Username(username, Worksheet)
    if Worksheet.cell(row=row, column=3).value == password:
        userID = Worksheet.cell(row=row, column = 1).value
        return True, userID
    else:
        return False, None

def Create_Employer_Account():
    #get useranme
    username = Get_username()
    password = Get_password()
    Companyname = Get_Company_Name()
    Companyaddress = Get_Address()
    WorkStatus = Get_Work_Status()
    email = Get_Email()

    confirm = input("Are you sure you want to confirm?\n: ").lower()
    if confirm == "yes":
        pass
    else:
        return

    Employers.append(EMPLOYER(Companyname, Companyaddress, WorkStatus, Email=email))
    Update_Employer(None, Employers)
    EmployerID = Employers[-1].ID
    
    Update_Username_password(EmployerID, username, password)

def Update_Username_password(ID, username, password):
    workbook, filepath = FileManager.GetFile("T4Dir", "Login_Details.xlsx", GetPath=True)
    WorkSheet = workbook["Details"]
    row = Find_ID(ID, WorkSheet)
    WorkSheet.cell(row=row, column=1).value = ID
    WorkSheet.cell(row=row, column=2).value = username
    WorkSheet.cell(row=row, column=3).value = password
    workbook.save(filepath)
    workbook.close()
    pass

def Create_Employee_Account():
    #get useranme
    username = Get_username()
    password = Get_password()
    Name = Get_Name()
    Occupation = Get_Occupation()
    Address = Get_Address()
    Resume = Get_Resume()
    Email = Get_Email()

    confirm = input("Are you sure you want to confirm?\n: ").lower()
    if confirm == "yes":
        pass
    else:
        return

    Employees.append(EMPLOYEE(Name, Address, Occupation, Resume=Resume, Email=Email))
    Update_Employee(None, Employees)
    EmployeeID = Employees[-1].ID
    
    Update_Username_password(EmployeeID, username, password)

def Get_username():
    return input("Please give a username\n: ")

def Get_password():
    return input("Please give a password\n: ")

def Get_Company_Name():
    return input("Please give a company name\n: ")

def Get_Name():
    return input("Please give a name\n: ")

def Get_Address():
    return input("Please give an address\n: ")

def Get_Occupation():
    option = input("Do you have a current occupation (1. for No, or type in your occupation)\n: ")
    if option == '1':
        return None
    else:
        return option

def Get_Resume():
    option = input("Do you want to put in a Resume (1. for no, or type in you resume)\n: ")
    if option == '1':
        return None
    else:
        return option

def Get_Work_Status():
    print("These are the available options")
    for i, option in enumerate(work_status_options):
        print(f"{i+1}. {option}")
    print("Select a number from 1 to 3")
    option = input(": ")
    while option not in ["1", "2", "3"]:
        print("That is not an available option")
        option = input(": ")
    num = int(option) -1
    return work_status_options[num]

def Get_Email():
    return input("Please input your email\n: ")

def Generate_Employees(num_entry):
    letter = "abcdefghijklmnopqrstuvwxyz"
    for n in range(0,num_entry):

        #Generate the name
        name = list_names[n]
        Name = name.upper() + " Employee"
        #Generate the address
        address = name + " st"
        #Occupation
        Occupation = Employers[randint(0,49)].Name
        #Generate the work status
        Employeeresume = resume[randint(0,2)]
        #Generate looking for position
        EmployeeStatement = resumeStatement[randint(0,2)]
        #Generate the email
        email = name + "@gmail.com"

        #append all of this to the excel spreadsheet
        Employees.append(EMPLOYEE(Name, address, Occupation, None, Employeeresume, EmployeeStatement, email))
        Update_Employee(None, Employees)

        EmployeeID = Employees[-1].ID

        Update_Username_password(EmployeeID, Name, "password")

def Generate_Employers(num_entry):
    letter = "abcdefghijklmnopqrstuvwxyz"
    for n in range(0,num_entry):

        #Generate the name
        name = list_names[n]
        Name = name.upper() + " corp"
        #Generate the address
        address = name + " st"
        #Generate the work status
        work_status = work_status_options[randint(0,2)]
        #Generate looking for position
        looking_for_position = TF[randint(0,1)]
        #Generate the email
        email = name + "@gmail.com"

        #append all of this to the excel spreadsheet
        Employers.append(EMPLOYER(Name, address, work_status, Looking_For_Position=looking_for_position, Email=email))
        Update_Employer(None, Employers)

        EmployerID = Employers[-1].ID

        Update_Username_password(EmployerID, Name, "password")

def Create_Employee_Filter():
    Filters = []
    print("What filters do you want to apply?")
    print("1. Occupation")
    print("2. Resume")
    print("3. Resumestatment")
    option = input(": ")
    while option:
        match option:
            case "1":
                Occupation = filterquestions(
                    "Currently Occupied?", binary=True
                )
                Filters.append(
                    Filter(
                        lambda employee: (not Occupation) if employee.Occupation == None else (Occupation), 
                        "Occupation"
                        )
                    )
            case "2":
                Resume = filterquestions(
                    "Current Resume", binary=False
                )
                Filters.append(
                    Filter(
                        lambda employee: True if employee.Resume == Resume else False,
                        "Resume"
                    )
                )
            case "3":
                ResumeStatement = filterquestions(
                    "Resume Statement", binary=True
                )
                Filters.append(
                    Filter(
                        lambda employee: ResumeStatement if employee.ResumeStatement == None else not ResumeStatement,
                        "Resume Statement"
                    )
                )
            case n_:
                print("Try again")
        print("What filters do you want to apply?")
        print("1. Occupation")
        print("2. Resume")
        print("3. Resumestatment")
        option = input(": ")
    return Filters

def Create_Employer_Filter():
    Filters = []
    print("What filters do you want to apply?")
    print("1. Looking for position")
    print("2. Work status")
    option = input(": ")
    while option:
        match option:
            case "1":
                L_F_P = filterquestions(
                    "Looping for positions?", binary=True
                )
                Filters.append(
                    Filter(
                        lambda employer: (not L_F_P) if employer.Looking_For_Position == None else (L_F_P), 
                        "L_F_P"
                        )
                    )
            case "2":
                Resume = filterquestions(
                    "Work status", binary=False
                )
                Filters.append(
                    Filter(
                        lambda employer: True if employer.Work_status == Resume else False,
                        "Work status"
                    )
                )
            case n_:
                print("Try again")
        print("What filters do you want to apply?")
        print("1. Looking for position")
        print("2. Work status")
        option = input(": ")
    return Filters

def filterquestions(question, binary = True):
    if binary == True:
        print(question)
        print("1. True\n2. False")
        option = input(": ")
        while option:
            if option == "1":
                return True
            elif option == "2":
                return False
            print(question)
            print("1. True\n2. False")
            option = input(": ")
    else:
        print(question)
        answer = input(": ")
        return answer
    pass

class Filter:
    def __init__(self, condition, Name) -> None:
        self.Name = Name
        self.condition = condition ## this should be a lambda function
    
    def Filter(self, array) -> list:
        filtered_array = []
        for entry in array:
            if self.condition(entry):
                filtered_array.append(entry)
        return filtered_array
    
    def Show(self) -> None:
        print(self.Name)

class Mailter:
    def __init__(self) -> None:
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login("timbot11105@gmail.com", "geelqvzkrzactxul")
        self.Address = "timbot11105@gmail.com"
        pass

    def sendmessage(self):
        msg = MIMEMultipart()
        msg["Subject"] = "Test Test test"
        msg.attach(MIMEText(
            """
            Hello,

            This is a test messsage

            this tests the indents of the email

            regards

            T
            """
        ))
        to = ["70928@joeys.org", "tims11105@gmail.com"]
        self.smtp.sendmail(from_addr=self.Address,
                           to_addrs=to,
                           msg=msg.as_string())
    
    def Email_Employer(self, employer, employee):
        destination = employer.Email
        msg = MIMEMultipart()
        msg["Subject"] = "A prospective new employee"
        msg.attach(MIMEText(
            f"""
            Hello {employer.Name}

            {employee.Name} has expressed interest in working at your company,
            They can be contacted at {employee.Email}.

            Their profile:
            Current Occupation: {employee.Occupation}
            Resume: {employee.Resume}
            Statement: {employee.ResumeStatement}

            Regards

            This is an automated email
            """
        ))
        self.smtp.sendmail(from_addr=self.Address,
                           to_addrs=[destination],
                           msg=msg.as_string())
    
    def Email_Employee(self, employer, employee):
        destination = employee.Email
        msg = MIMEMultipart()
        msg["Subject"] = "An Employer has contacted you"
        msg.attach(MIMEText(
            f"""
            Hello {employee.Name}

            {employer.Name} has expressed interest employing you at their company,
            They can be contacted at {employer.Email}.

            Their profile:
            Work status: {employer.Work_status}
            Looking for Position: {employer.Looking_For_Position}

            Regards

            This is an automated email
            """
        ))
        self.smtp.sendmail(from_addr=self.Address,
                           to_addrs=[destination],
                           msg=msg.as_string())

    def close(self):
        self.smtp.quit()

def main():
    option = input("1.create an account\n2. login\n: ")
    while option:
        if option == "1":
            Create_Account()
        if option == "2":
            Login_Account()
        option = input("1.create an account\n2. login\n: ")

Bot = Mailter()
Employers = Load_Employers()
Employees = load_Employees()
main()
Bot.close()