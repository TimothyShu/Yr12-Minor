from random import randint
from datetime import datetime
import time

n = 10
r = 1000

test_data = [randint(0, r) for n in range(n)]

def sort_insert(array, key = lambda x:x) -> None:
    for n in range(1, len(array)):
        current_position = n
        temp = array[current_position]
        while key(temp) < key(array[current_position -1]) and current_position >=1:
            array[current_position] = array[current_position -1]
            current_position -= 1
        array[current_position] = temp
    pass

def sorted_insert(array, key = lambda x:x) -> list:
    #duplicate the array
    new_array = array[:]
    for n in range(1, len(new_array)):
        current_position = n
        temp = new_array[current_position]
        while key(temp) < key(new_array[current_position -1]) and current_position >=1:
            new_array[current_position] = new_array[current_position -1]
            current_position -= 1
        new_array[current_position] = temp
    return new_array

def sort_select(array, key = lambda x:x) -> None:
    for n in range(len(array)):
        current_ind = n
        minima = current_ind
        for i in range(n, len(array)):
            if key(array[minima]) >= key(array[i]):
                minima = i
        swap(minima, current_ind, array)

def sorted_select(array, key = lambda x:x) -> list:
    #duplicate the array
    new_array = array[:]
    for n in range(0,len(new_array)):
        current_ind = n
        minima = current_ind
        for i in range(n, len(new_array)):
            if key(new_array[minima]) >= key(new_array[i]):
                minima = i
        swap(minima, current_ind, new_array)
    return new_array

def sorted_quick(array, key):
    new_array = array[:]
    return sort_quick(new_array, key)

#This is a recursive sorting method
def sort_quick(array, key = lambda x:x) -> list:
    #This is the end of the recursion
    if len(array) <= 1:
        #return array
        return

    #choose an element of the unsorted
    pivot_element = array[-1]
    #print(pivot_element)
    large_pointer = None
    for index in range(0, len(array)-1):
        value = array[index]
        if large_pointer == None:
            if key(value) > key(pivot_element):
                large_pointer = index
                continue
            continue
        if key(value) < key(pivot_element):
            swap(large_pointer, index, array)
            large_pointer += 1
            
    # change the middle index with the pivot element
    if large_pointer == None:
        # then the array must all be smalled than the pivot element
        # We'll take away the pivot and then pass the rest of the array through the function
        left_side = array[:-1]
        sort_quick(left_side, key=key)
        array[:-1] = left_side
        array[-1] = pivot_element
        return

    swap(-1, large_pointer, array)

    if large_pointer == 0:
        # then the array must all lbe bigger than the pivot element
        right_side = array[1:]
        sort_quick(right_side, key=key)
        array[0] = pivot_element
        array[1:] = right_side
        return

    #split the array into left and right

    #left side
    left_side = array[:large_pointer]
    sort_quick(left_side, key=key)

    #right side
    right_side = array[large_pointer+1:]
    sort_quick(right_side,key=key)

    # adding the sorted left side, the middle and the sorted right side
    array[:large_pointer] = left_side
    array[large_pointer] = pivot_element
    array[large_pointer+1:] = right_side
    return



def swap(position1, position2, array) -> None:
    temp =  array[position1]
    array[position1] = array[position2]
    array[position2] = temp

if __name__ == "__main__":
    sort_select(test_data)
    print(test_data)
    
    
