from random import randint
from sorting import *
from more_itertools import first_true

class Student:
    def __init__(self, Name: str) -> None:
        self.Name = Name
        self.Group = None
        self.Cabin = None
        self.CabinName = None
    
    def Add_Group(self, Group)->None:
        self.Group = Group
        self.GroupName = Group.Name

    def Add_Cabin(self, Cabin)->None:
        self.Cabin = Cabin
        self.CabinName = Cabin.Name
    
    def Clear_Cabin(self) -> None:
        self.Cabin = None
        self.CabinName = None
    
    def Show(self) -> None:
        print(f"Name: {self.Name}, Group: {self.GroupName}, Cabin: {self.CabinName}")

class Group:
    def __init__(self, Name: str) -> None:
        self.Name = Name
        self.Students = []
        self.Size = 0
    
    def Add_Member(self, Student: Student):
        self.Size += 1
        self.Students.append(Student)
        Student.Add_Group(self)
    
    def Show_Group(self):
        print(f"Group name: {self.Name}, size: {self.size}")
    
    def Count_unalocated(self) -> int:
        Students = self.Students
        counter = 0
        for student in Students:
            if student.Cabin == None:
                counter += 1
        return counter

class Cabin:
    def __init__(self, Name: str, capacity: int) -> None:
        self.Students = []
        self.Name = Name
        self.Size = 0
        self.Capacity = capacity

    def Add_Member(self, Student: Student) -> None:
        self.Size += 1
        self.Students.append(Student)
        Student.Add_Cabin(self)
    
    def Remove_Member(self, Student: Student) -> None:
        for index, student in enumerate(self.Students):
            if Student == student:
                self.Students.pop(index)
                Student.Clear_Cabin()
                self.Size -= 1

    def Add_Group(self, Group: Group) -> None:
        Students = Group.Students
        for student in Students:
            if student.Cabin != None:
                continue
            if self.Size < 20:
                student.Add_Cabin(self)
                self.Add_Member(student)
            else:
                break

    def Get_Group_Size(self) -> dict:
        current_groups = []
        Group_num = {}
        for student in self.Students:
            if student.Group.Name not in current_groups:
                current_groups.append(student.Group.Name)
                Group_num[student.Group.Name] = 1
            else:
                Group_num[student.Group.Name] += 1
        return Group_num
    
    def Remove_Group(self, groupname: str) -> None:
        Students_remove = []
        for student in self.Students:
            if student.Group.Name == groupname:
                Students_remove.append(student)

        for student in Students_remove:
            self.Remove_Member(student)
        pass

    def Clear_Cabin(self) -> None:
        for student in self.Students:
            self.Remove_Member(student)
        pass

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

def CreateStudents(num_students: int) -> list[Student]:
    Students = []
    for i in range(0, num_students):
        Students.append(Student(Names[i]))
    return Students

def CreateGroups(group_num: int, students: list[Student]) -> list[Group]:
    #Fill in as many groups with minimum 2 people as possible
    len_students = len(students)
    max_num_groups = int(len_students/2)
    if max_num_groups < group_num:
        group_num = max_num_groups
    
    #Create x amount of groups
    Groups = []
    for group in range(0,group_num):
        Groups.append(Group(str(group)))

    #Slice the list into 2* num of groups and the rest
    end = 2 * group_num
    StudentAlocation = students[0:end]
    current_student = 0
    for group in Groups:
        while group.Size < 2:
            group.Add_Member(StudentAlocation[current_student])
            current_student += 1
    
    #Slice the other half of the group
    StudentAlocation = students[end:]
    for student in StudentAlocation:
        group_num = randint(0, len(Groups)-1)
        group = Groups[group_num]
        group.Add_Member(student)

    return Groups

def CreateCabins(Cabin_num: int, Cabin_capactiy: int) -> list[Cabin]:
    Cabins = []
    for index in range(0, Cabin_num):
        Cabins.append(Cabin(str(index), Cabin_capactiy))
    return Cabins

def Algorithm(Groups: list[Group], Students: list[Student], Cabins: list[Cabin]):
    #Do it randomly
    #Loop through each group and randomly allocate a cabin
    unalocated_Groups = []

    #Sort the groups based on size
    sort_quick(Groups, key=lambda group: -group.Size)

    for group in Groups:
        cabin_num = randint(0, len(Cabins)-1)
        # We have to check if the group can fit in
        cabin = Cabins[cabin_num]
        if group.Size + cabin.Size > cabin.Capacity:
            #We'll skip and add it to unalocated
            unalocated_Groups.append(group)
            continue
        # Or else, we'll add the group to the Cabin
        cabin.Add_Group(group)

    #Now we loop through unalocated groups and see if they can fit in
    to_pop = []
    for index, group in enumerate(unalocated_Groups):
        for cabin in Cabins:
            #Check if there is free space
            free_space = cabin.Capacity - cabin.Size
            if free_space >= group.Size:
                cabin.Add_Group(group)
                #Remove the group from unalocated
                to_pop.append(index)
                break
            pass
    
    #sort the list in reverse
    sort_quick(to_pop, key=lambda x: -x)
    for group in to_pop:
        unalocated_Groups.pop(group)
    
    #This begins part 2 of the Alg
    #___________________
    #|                  |
    #|      Part 2      |
    #|__________________|

    #After this, we have filled all groups except the last,
    #These groups are of the largest size

    #Find cabin with the most free spots
    sort_quick(Cabins, key=lambda cabin: -(cabin.Capacity - cabin.Size))

    for index, cabin in enumerate(Cabins):
        #since we are looping through all cabins,
        #we want to skip thhe ones that are complete
        if cabin.Capacity - cabin.Size == 0:
            break
        #Find the size of groups in the Cabin
        Group_Size = cabin.Get_Group_Size()
        #We'll sort this by converting the dict into a list
        Group_Size = sorted(Group_Size.items(), key=lambda x: x[1])

        #get the smallest group and see if it can fit into another Cabin
        for entry in Group_Size:
            groupname = entry[0]
            groupsize = entry[1]
            for newcabin in Cabins:
                if groupsize <= newcabin.Capacity - newcabin.Size:
                    #We'll slot the group into the cabin
                    #First we remove it
                    cabin.Remove_Group(groupname)

                    #Then we add it to the new cabin

                    group = first_true(Groups, None, lambda group: group.Name==groupname)

                    #Adding new group to new cabin
                    newcabin.Add_Group(group)
                    break
            pass
    for cabin in Cabins:
        pass
        #print(f"Cabin name: {cabin.Name}, Cabin capacity: {cabin.Capacity}, Cabin size: {cabin.Size}")

    #This begins part 3 of the Alg
    #___________________
    #|                  |
    #|      Part 3      |
    #|__________________|

    for group in Groups:
        print(group.Count_unalocated())
    #We will now split them up and fill in all of the remaining spots
    remaining_students = []
    for group in unalocated_Groups:
        for student in group.Students:
            remaining_students.append(student)
    
    #We'll just itteratively add students
    current_index = 0
    for cabin in Cabins:
        if current_index >= len(remaining_students):
            break
        free_space = cabin.Capacity - cabin.Size
        while free_space > 0:
            cabin.Add_Member(remaining_students[current_index])
            current_index += 1
            free_space -= 1
    return

def count_splits(groups: list[Group]):
    splits = 0
    for group in groups:
        cabins = []
        for student in group.Students:
            if student.Cabin.Name not in cabins:
                cabins.append(student.Cabin.Name)
        group_splits = len(cabins)-1
        splits += group_splits
    return splits

def search_students():
    option = input("1.show all student names, 2.inquire student\n: ")
    while option:
        if option == "1":
            for student in Students:
                print(student.Name)
        elif option == "2":
            name = input("Name?\n: ")
            for student in Students:
                if student.Name == name:
                    student.Show()
                    break
            else:
                print("He does not exist")
        else:
            print("Please choose again")
        option = input("1.show all student names, 2.inquire student\n: ")
    pass

def Create_env() -> list[list[Student], list[Group], list[Cabin]]:
    Students = CreateStudents(100)
    Groups = CreateGroups(10, Students)
    Cabins = CreateCabins(5, 20)
    return [Students, Groups, Cabins]

Names = create_student_name()
if __name__ == "__main__":

    Students = CreateStudents(100)

    Groups = CreateGroups(10, Students)

    Cabins = CreateCabins(5, 20)

    Algorithm(Groups, Students, Cabins)
    print(count_splits(Groups))
    #search_students()

"""for n in Cabins:
    print(n.Size)
    
for n in Groups:
    print(n.Size)"""