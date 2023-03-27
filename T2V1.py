import numpy as np

TextString = "abcdefghijklmnopqrstuvwxyz"

class concert:
    def __init__(self, rows, column) -> None:
        self.Concert = np.zeros((rows, column), dtype=int)
        self.Seat_Groups = self.Get_Consequitive_Seats(self.CreateSeatsArray())
    
    def Update_Seat_Groups(self):
        self.Seat_Groups = self.Get_Consequitive_Seats(self.CreateSeatsArray())

    def emptyseats(self):
        return np.where(self.Concert == 0)
    
    def CreateSeatsArray(self):
        emptyseats = self.emptyseats()
        seats = []
        for ind, column in enumerate(emptyseats[1]):
            seats.append([emptyseats[0][ind], column])
        return seats

    def Get_Consequitive_Seats(self, emptyseats):
        if len(emptyseats) == 0:
            return emptyseats
        previous_seat = emptyseats[0]
        seat_groups = np.array((0))
        consequitive_seats = [0,0,0,0] #initialise a list
        self.reset_consequitive_seat(consequitive_seats, previous_seat) #primes the list
        for seat in emptyseats[1:]:
            if seat[0] != previous_seat[0] or seat[1] != previous_seat[1] + 1: #checks if break is nessisary
                seat_groups = self.sever_list(seat_groups, consequitive_seats)
                self.reset_consequitive_seat(consequitive_seats, seat)
            else:
                consequitive_seats[2] += 1
                consequitive_seats[3] += 1
            previous_seat = seat
        else:
            seat_groups = self.sever_list(seat_groups, consequitive_seats)
        return seat_groups
    

    def reset_consequitive_seat(self, consequitive_seat, seat):
        consequitive_seat[0] = seat[0]
        consequitive_seat[1] = seat[1]
        consequitive_seat[2] = seat[1]
        consequitive_seat[3] = 1
    
    def sever_list(self, seat_groups, consequitive_seats):
        try:
            seat_groups = np.append(seat_groups, [consequitive_seats], 0)
        except ValueError:
            seat_groups = np.asarray([consequitive_seats])
        return seat_groups

    
    def book_People(self, n_people):
        for entry in self.Seat_Groups:
            if entry[3] >= n_people:
                #book 4 consequitive rows
                row = entry[0]
                start = entry[1]
                end = start + n_people
                seats = self.book_Seats(row, start, end)
                return seats
        else:
            print("There are no more available seats")
            return None
    
    def book_Seats(self, row, start, end):
        seats = []
        for seat_column in range(start, end):
            self.Concert[row][seat_column] = 1
            seats.append(self.Get_Seat_Num(row, seat_column))
        #update the seat groups
        self.Update_Seat_Groups()
        return seats
    
    def Get_Seat_Num(self, row, column):
        seat_num = TextString[row].upper() + str(column+1)
        return seat_num

def main():
    concert1 = concert(rows =14, column =10)
    option = input("How many people are you booking for?\n: ")
    while option:
        try:
            n_people = int(option)
        except ValueError:
            print("Number?")
            continue
        seats = concert1.book_People(n_people)
        if seats == None:
            option = input("How many people are you booking for?\n: ")
            continue
        print(f"You have booked \n{', '.join(seats)}")
        option = input("How many people are you booking for?\n: ")


if __name__ == "__main__":
    main()