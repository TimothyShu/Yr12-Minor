from collections.abc import Callable, Iterable, Mapping
from typing import Any
from T5V1 import *
import itertools
import threading

#create a generator 
stuff = [0,1,2,3,4,5,6,7,8,9]
Perms = itertools.permutations(stuff)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter) -> None:
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self, env :MyEnvironment) -> list[int, list]:

        local_env = env.Copy_()

        minimum = None
        
        #Go through the while loop
        while True:
            print("looping")
            if minimum == 0:
                break
            try:
                nex_perm = next(Perms)
            except StopIteration:
                break
            
            for num in nex_perm:
                Groupname = str(num)
                Group = local_env.Get_Group_by_Name(Groupname)
                AddGroup(local_env.Cabins, Group)
            #Add in all the groups left
            extrasequence = Fill_in_rest(Cabins, Groups)
            for student in local_env.Students:
                student.Show()
            #if minimum is smaller than current minimum, add new sequence
            if count_splits(Groups) < minimum or minimum == None:
                minchain = nex_perm[:] + extrasequence
                minimum = Groups
            
            #plus 1 to the counter
            self.counter += 1
            print(self.counter)
            #reset after a cycle
            local_env.reset()
        return [minimum, minchain]

def Fill_in_rest(Cabins : list[Cabin], Groups: list[Group]):
    Group_sequence = []
    Groups_left = []
    #Get amount of unallocated groups
    for group in Groups:
        if group.Count_unalocated() == 0:
            continue
        Groups_left.append(group)
    
    for group in Groups_left:
        AddGroup(Cabins, group)
        Group_sequence.append(group.Name)
    return Group_sequence


def AddGroup(Cabins: list[Cabin], Group: Group):
    curr_cabin = None
    for cabin in Cabins:
        if cabin.Capacity - cabin.Size == 0:
            continue
        curr_cabin = cabin
        break
    curr_cabin.Add_Group(Group)

Students = CreateStudents(100)
Cabins = CreateCabins(10, 20)
Groups = CreateGroups(10, Students)

for student in Students:
    student.Show()

baseEnv = MyEnvironment(Students, Cabins, Groups)
thread1 = myThread(1, "Thread-1", 0)
thread1.run(baseEnv)
