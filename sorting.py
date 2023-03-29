from random import randint

n = 100
r = 1000

test_data = [randint(0, r) for n in range(n)]
print(test_data)
def bubble_sort(array):
    for n in range(len(array)-2):
        sort_position = 1
        for ind in range(len(array)-sort_position):
            if array[ind] < array[ind+1]:
                swap(ind, ind+1, array)
    pass

def insertion_sort(array):
    for n in range(1, len(array)):
        current_position = n
        temp = array[current_position]
        while temp > array[current_position -1] and current_position >=1:
            array[current_position] = array[current_position -1]
            current_position -= 1
        array[current_position] = temp
    pass

def selection_sort(array):
    for n in range(len(array)):
        current_ind = n
        minima = current_ind
        for i in range(n, len(array)-1):
            if array[minima] >= array[i]:
                minima = i
        swap(minima, current_ind, array)


def swap(position1, position2, array):
    temp =  array[position1]
    array[position1] = array[position2]
    array[position2] = temp

if __name__ == "__main__":
    selection_sort(test_data)
    print(f'This is sorted: \n {test_data}')
    
