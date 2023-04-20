import FileManager
from random import randint
from itertools import chain, product

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
        column = [Employers.cell(row = row, column = ind).value for ind in range(1,6)]
        employers.append(column)
        row += 1
        cell = Employers.cell(row = row, column = 2).value

    Workbook.close()

    for ind, Employer in enumerate(employers):
        employers[ind] = Read_Employer(Employer)

    return employers

def Read_Employer(Employer) -> EMPLOYER:
    return EMPLOYER(Employer[1], Employer[2], Employer[3], Employer[0], Employer[4])

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
        column = [Employees.cell(row = row, column = ind).value for ind in range(1,7)]
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
    return EMPLOYEE(Employee[1], Employee[2], Employee[3], Employee[0], Employee[4], Employee[5])

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
    pass

def Login_Employer(userID):
    #Load their account
    print(f"You're logged into the account with ID {userID}")
    Account = load_Employer(userID)
    pass

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


Employers = Load_Employers()
Employees = load_Employees()
