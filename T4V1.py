import FileManager

employer_fieldname = ["Name", "Address", "Wages", "Work Status", "Active Positions"]
employee_fieldname = ["Name", "Address", "Occupation"]

Base_Employer_ID = 000000
Base_Employee_ID = 100000

class EMPLOYER:
    def __init__(self, Name, location, wage_dictionary, work_status, ID=None, Active_positions = []) -> None:
        self.Name = Name
        self.Address = location
        self.Wages = wage_dictionary
        self.Work_status = work_status
        self.Active_positions = Active_positions
        self.ID = ID
        if self.ID == None:
            self.New = True
        else:
            self.New = False
    
    def Add_Position(self, PositionName) -> None:
        try:
            wage = self.wages[PositionName]
            print("Success")
        except KeyError:
            print("Position does not exist")
    
    def Add_Employer(self, Employers):
        if self.New == False:
            return
        if len(Employers) == 0:
            self.ID = Base_Employer_ID
            return
        last_ID = Employers[-1][0]
        self.ID = last_ID + 1
        self.New = False

class EMPLOYEE:
    def __init__(self, Name, Address, Occupation, ID = None, Resume = [], ResumeStatement = None) -> None:
        self.Name = Name
        self.Address = Address
        self.Occupation = Occupation
        self.Resume = Resume
        self.ResumeStatement = ResumeStatement
        self.ID = ID
        if self.ID == None:
            self.New = True
        else:
            self.New = False
        pass

    def Add_Employee(self, Employees) -> None:
        if self.New == False:
            return
        if len(Employees) == 0:
            self.ID = Base_Employee_ID
            return
        last_ID = Employees[-1][0]
        self.ID = last_ID + 1
        self.New = False


def Load_Employers() -> list:
    employers = []

    #Loop through all attributes
    Workbook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    #This opens the workbook
    Employers = Workbook["Employers"]
    print(Employers)

    row = 1
    cell = Employers.cell(row = 1, column = 1).value
    while cell:
        #loop through the whole row
        column = [Employers.cell(row = row, column = ind).value for ind in range(1,6)]
        employers.append(column)
        row += 1
        cell = Employers.cell(row = row, column = 1).value

    Workbook.close()

    for ind, Employer in enumerate(employers):
        employers[ind] = Read_Employer(Employer)

    return employers

def Read_Employer(Employer) -> EMPLOYER:
    return EMPLOYER(Employer[1], Employer[2], Employer[3], Employer[4], Employer[0], Employer[5])

def Update_Employer(ID, Employers) -> None:
    WorkBook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    Employersheet = WorkBook["Employers"]
    row = Find_ID(ID, Employers)
    index = row -1
    Employer = Employers[index]
    #Add all the columns based on the value
    if Employer.New == True:
        Employer.Add_Employer(Employers)
    Employersheet.cell(row=row, column=1).value == Employer.ID
    Employersheet.cell(row=row, column=2).value == Employer.Name
    Employersheet.cell(row=row, column=3).value == Employer.Address
    Employersheet.cell(row=row, column=4).value == Employer.Occupation
    Employersheet.cell(row=row, column=5).value == Employer.Resume
    Employersheet.cell(row=row, column=6).value == Employer.ResumeStatement
    WorkBook.close()

def load_Employees() -> list:

    employees = []

    Workbook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    Employees = Workbook["Employees"]

    row = 1
    cell = Employees.cell(row = 1, column = 1).value
    while cell:
        #loop through the whole row
        column = [Employees.cell(row = row, column = ind).value for ind in range(1,5)]
        employees.append(column)
        row += 1
        cell = Employees.cell(row = row, column = 1).value

    Workbook.close()

    for ind, Employee in enumerate(employees):
        employees[ind] = Read_Employees(Employee)
    
    return employees

def Read_Employees(Employee) -> EMPLOYEE:
    return EMPLOYEE(Employee[1], Employee[2], Employee[3], Employee[0], Employee[4], Employee[5])

def Update_Employee(ID,Employees) -> list:
    WorkBook = FileManager.GetFile("T4Dir", "Data_Store.xlsx")
    Employeesheet = WorkBook["Employees"]
    row = Find_ID(ID, Employees)
    index = row -1
    Employee = Employees[index]
    #Add all the columns based on the value
    if Employee.New == True:
        Employee.Add_Employer(Employees)
    Employeesheet.cell(row=row, column=1).value == Employee.ID
    Employeesheet.cell(row=row, column=2).value == Employee.Name
    Employeesheet.cell(row=row, column=3).value == Employee.Address
    Employeesheet.cell(row=row, column=4).value == Employee.Wages
    Employeesheet.cell(row=row, column=5).value == Employee.Work_status
    Employeesheet.cell(row=row, column=6).value == Employee.Active_positions
    WorkBook.close()

def Find_ID(ID, Worksheet) -> int:
    row = 1
    while Worksheet.cell(row = row, column = 1).value:
        if Worksheet.cell(row = row, column = 1).value == ID:
            return row
        row += 1
    return row

print(Load_Employers())
print(load_Employees())