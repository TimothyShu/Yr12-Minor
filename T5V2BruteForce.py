from collections.abc import Callable, Iterable, Mapping
from typing import Any
from T5V1 import *
import itertools
import threading
from sorting import sort_quick

#create a generator 
stuff = [0,1,2,3,4,5,6,7,8,9]
Perms = itertools.permutations(stuff)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, env) -> None:
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.env = env
        self.minimum = None
        self.minchain = None

    def run(self) -> list[int, list]:

        local_env = self.env.Copy_()

        minimum = None
        
        #Go through the while loop
        while True:
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
            extrasequence = Fill_in_rest(local_env.Cabins, local_env.Groups)
            
            #if minimum is smaller than current minimum, add new sequence
            if minimum == None:
                minchain = list(nex_perm[:]) + extrasequence[:]
                minimum = count_splits(local_env.Groups)
            elif count_splits(local_env.Groups) < minimum:
                minchain = list(nex_perm[:]) + extrasequence[:]
                minimum = count_splits(local_env.Groups)
            
            #plus 1 to the counter
            self.counter += 1
            #reset after a cycle
            local_env.reset()
        print(f"{self.name} compute: {self.counter}")
        self.minimum = minimum
        self.minchain = minchain

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
        Group_sequence.append(int(group.Name))
    return Group_sequence


def AddGroup(Cabins: list[Cabin], Group: Group):
    curr_cabin = None
    for cabin in Cabins:
        if cabin.Capacity - cabin.Size == 0:
            continue
        curr_cabin = cabin
        break
    if curr_cabin == None:
        return
    curr_cabin.Add_Group(Group)

S = CreateStudents(100)
C = CreateCabins(5, 20)
G = CreateGroups(10, S)

def finalcomb(sequence, env : MyEnvironment):
    for group in sequence:
        g_name = str(group)
        Group = env.Get_Group_by_Name(g_name)
        AddGroup(env.Cabins, Group)

def Algorithm_BruteForce():
    threads = 20
    baseEnv = MyEnvironment(S, C, G)
    Threads = []
    for n in range(0, threads):
        ThreadID = n
        Threadname = "Thread-"+str(n)
        new_Thread = myThread(ThreadID, Threadname, 0, baseEnv)
        new_Thread.start()
        Threads.append(new_Thread)

    finished = False
    p20 = False
    p40 = False
    p60 = False
    p80 = False
    while finished == False:
        for thread in Threads:
            if thread.minimum == 0:
                finished = True
                print("Found a zero!")
        count_calculations = [thread.counter for thread in Threads]
        calc_sum = sum(count_calculations)
        total_calc = 3628800
        percentage = calc_sum / total_calc
        if percentage > 0.2 and p20 == False:
            print(f"20% {calc_sum} completed")
            p20 = True
        if percentage > 0.4 and p40 == False:
            print(f"40% {calc_sum} completed")
            p40 = True
        if percentage > 0.6 and p60 == False:
            print(f"60% {calc_sum} completed")
            p60 = True
        if percentage > 0.8 and p80 == False:
            print(f"80% {calc_sum} completed")
            p80 = True
        if percentage == 1:
            print("100%")
            print("done!")
            finished = True
        time.sleep(5)

    #sort threads based on minimum

    sort_quick(Threads, lambda thread: thread.minimum)

    #get the minimum
    min_thread = Threads[0]

    min_thread_chain = min_thread.minchain
    finalcomb(min_thread_chain, baseEnv)
    splits = count_splits(baseEnv.Groups)
    print(f"Brute force: {splits}")
    return baseEnv

if __name__ == "__main__":
    baseEnv = Algorithm_BruteForce()
    Students = baseEnv.Students
    search_students(Students)