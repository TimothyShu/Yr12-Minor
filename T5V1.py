from random import randint

class Cabins:
    def __init__(self, Name) -> None:
        self.Students = []
        self.Name = Name

class Group:
    def __init__(self, Name) -> None:
        self.Name = Name
        self.Students = []
        self.size = 0
    
    def Add_Member(self):
        self.size += 1
    
    def Show_Group(self):
        print(f"Group name: {self.Name}, size: {self.size}")

class Student:
    def __init__(self, Name) -> None:
        self.Name = Name
        self.Group = None
        self.Cabin = None
    
    def Add_Group(self, Group)->None:
        self.Group = Group

    def Add_Cabin(self, Cabin)->None:
        self.Cabin = Cabin

def create_student_name() -> list:
    Names = []
    #letters
    letters = "abcdefghijklmnopqrstuvwxyz"
    for letter in letters:
        for num1 in range(0,10):
            for num2 in range(0,10):
                Names.append(f"{letter}-{num1}{num2}")
            pass
        pass
    return Names

def CreateStudents(num_students) -> list[Student]:
    Students = []
    for i in range(0, num_students):
        Students.append(Student(Names[i]))
    return Students

def GenerateGroups(group_num, students):
    #Fill in as many groups with minimum 2 people as possible
    max_num_groups = int(students/2)
    if max_num_groups < group_num:
        group_num = max_num_groups
    

def AddRandomGroup(Groups):
    pass

Names = create_student_name()

Students = CreateStudents(100)