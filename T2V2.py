import numpy as np

TextString = "abcdefghijklmnopqrstuvwxyz"

Occupied = "-X"

"""Create an image to show the seats"""
#Let the user select where their seats are
#Give an option to automatically choose the closeset seats if there are no consequitive seats

class concert:
    def __init__(self, rows, column) -> None:
        self.Concert = np.zeros((rows, column), dtype=int)
        self.AllEmptySeats = self.CreateSeatsArray()
        self.Seat_Groups = self.Get_Consequitive_Seats(self.AllEmptySeats)
    
    def Update_Seat_Groups(self):
        self.AllEmptySeats = self.CreateSeatsArray()
        self.Seat_Groups = self.Get_Consequitive_Seats(self.AllEmptySeats)

    def Get_Num_EmptySeats(self) -> int:
        return len(self.AllEmptySeats)

    def emptyseats(self) -> np.ndarray:
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
    
    def Show_concert(self):
        print(f"   {' '.join([str(i+1) for i in range(0, len(self.Concert[0]))])}")
        for row_num, row in enumerate(self.Concert):
            print(f"{TextString[row_num].upper()}: {' '.join([Occupied[i] for i in row])}")

    def reset_consequitive_seat(self, consequitive_seat, seat):
        consequitive_seat[0] = seat[0] # Row
        consequitive_seat[1] = seat[1] # Start column
        consequitive_seat[2] = seat[1] # End column
        consequitive_seat[3] = 1 # How many seats
    
    def sever_list(self, seat_groups, consequitive_seats) -> np.ndarray:
        try:
            seat_groups = np.append(seat_groups, [consequitive_seats], 0)
        except ValueError:
            seat_groups = np.asarray([consequitive_seats])
        return seat_groups

    def Validate_Seats(self, seat):
        try:
            row = TextString.index(seat[0].lower())
            column = int(seat[1])-1
        except ValueError:
            print("Invalid Seat")
            return False
        
        try:
            self.Concert[row][column]
        except IndexError:
            print("Seat does not exist")
            return False
        
        if self.Concert[row][column] == 1:
            print("Seat already occupied")
            return False
        
        return [row, column]

    def Manual(self, n_people):
        self.Show_concert()
        seat = input("Choose the seat you want to book\n: ")
        tickets = []
        for i in range(0, n_people):
            seat = self.Validate_Seats(seat)
            while seat == False:
                print("The seat you've entered is not valid or unavailable")
                seat = input("Choose the seat you want to book\n: ")
                seat = self.Validate_Seats(seat)
            tickets.append(seat)
            if n_people -1 - i == 0:
                break
            print(f"{n_people - i-1} more to book")
            seat = input("Choose the seat you want to book\n: ")
        tickets = np.asarray(tickets)
        seats = self.book_Seats_ByList(tickets)
        print(f"You have booked \n{', '.join(seats)}")


    def Automatic(self, n_people):
        self.Show_concert()
        option = input("Do you want to book in a general location\n: ").lower()
        while option:
            if option == 'yes':
                self.Prefered_automatic(n_people)
                break
            elif option == 'no':
                break
            else:
                print("That is not an option")
            option = input("Do you want to book in a general location\n: ").lower()
        pass

    def Prefered_automatic(self, n_people) -> None:
        seat = input("Select an empty seat")
        seat = self.Validate_Seats(seat)
        while seat == False:
            seat = input("Select an empty seat")
            seat = self.Validate_Seats(seat)
        for seat_group in self.Seat_Groups:
            if seat_group[0] == seat[0]:
                continue
            if seat_group[1] > seat[1]:
                continue
            if seat_group[2] < seat[1]:
                continue
            if seat_group[3] < n_people:
                continue
            row = seat[0]
            column = seat[1]
            start = seat_group[1]
            space_from_left = column - start
            print(row)
            if space_from_left < n_people-1:
                start_column = start
                end_column = start + n_people
                pass
            else:
                start_column = column - n_people
                end_column = column
            seats = self.book_Seats(row, start_column, end_column)
            print(f"You have booked \n{', '.join(seats)}")
            break
        else:
            print("There arn't any available consequitive seats around the seat.")
            pass
        pass

    def Sequiential_Automatic(self, n_people) -> None:
        for entry in self.Seat_Groups:
            if entry[3] >= n_people:
                #book 4 consequitive rows
                row = entry[0]
                start = entry[1]
                end = start + n_people
                seats = self.book_Seats(row, start, end)
                return seats
        else:
            print("There are no more available consequitive seats")
            return None
    
    def Automatic_Fit(self, n_people) -> None:
        option = input("Do you want to book seats that might not be together?").lower()
        if option == "yes":
            pass
        elif option == "no":
            return
        else:
            self.Automatic_Fit(n_people)
            return
        self.Show_concert()
        seat = input("Select an empty seat")
        seat = self.Validate_Seats(seat)
        while seat == False:
            seat = input("Select an empty seat")
            seat = self.Validate_Seats(seat)
        
        list_of_seats = []


    def book_People(self, n_people):
        option = input("Book manually or automatically?\n: ").lower()
        while option:
            if option == "manual":
                self.Manual(n_people)
                break
            elif option == "automatic":
                self.Automatic(n_people)
                break
            else:
                print("option not recognised")
            option = input("Book manually or automatically?\n: ").lower()
    
    def book_Seats(self, row, start, end):
        print(f"Booking from {start} to {end} on row {row}")
        seats = []
        for seat_column in range(start, end):
            self.Concert[row][seat_column] = 1
            seats.append(self.Get_Seat_Num(row, seat_column))
        #update the seat groups
        self.Update_Seat_Groups()
        return seats
    
    def book_Seats_ByList(self, tickets):
        seats = []
        for ticket in tickets:
            self.Concert[ticket[0]][ticket[1]] = 1
            seats.append(self.Get_Seat_Num(ticket[0], ticket[1]))
        self.Update_Seat_Groups()
        return seats

    def Get_Seat_Num(self, row, column):
        seat_num = TextString[row].upper() + str(column+1)
        return seat_num
    
    def main(self) -> None:
        option = input("How many people are you booking for?\n: ")
        while option:
            try:
                n_people = int(option)
            except ValueError:
                print("Number?")
                option = input("How many people are you booking for?\n: ")
                continue
            if self.Get_Num_EmptySeats() > n_people:
                print(f"There arn't enough seats in the concert for {n_people} people")
                print(f"Ther concert has {self.Get_Num_EmptySeats()} spare seats left")
                continue
            self.book_People(n_people)
            self.Show_concert()
            option = input("How many people are you booking for?\n: ")
        self.Show_concert()


def main():
    concert1 = concert(rows =14, column =10)
    concert1.Show_concert()
    option = input("How many people are you booking for?\n: ")
    concert1.main()

    


if __name__ == "__main__":
    main()