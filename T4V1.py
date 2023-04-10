import FileManager

employer_fieldname = ["Name", "Address", "Wages", "Work Status", "Active Positions"]
employee_fieldname = ["Name", "Address", "Occupation"]

class employer:
    def __init__(self, Name, location, wage_dictionary, work_status) -> None:
        self.Name = Name
        self.Address = location
        self.Wages = wage_dictionary
        self.Work_status = work_status
        self.Activepositions = []
    
    def Add_Position(self, PositionName) -> None:
        try:
            wage = self.wages[PositionName]
            print("Success")
        except KeyError:
            print("Position does not exist")

class emplyee:
    def __init__(self, Name, Address, Occupation) -> None:
        self.Name = Name
        self.Address = Address
        self.Occupation = Occupation
        self.Resume = []
        self.ResumeStatement = None
        pass
def Load_Employers() -> list:
    #Loop through all attributes
    Employers = FileManager.GetFile("T4Dir", "Employers.csv")
    pass

def Update_Employers(FilePath) -> None:
    pass

def load_Employees() -> list:
    Employees = FileManager.GetFile("T4Dir", "Employees.csv")
    pass

def Update_Employees() -> list:
    pass