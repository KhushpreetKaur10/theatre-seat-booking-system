import os
from datetime import datetime

rows = 10
cols = 10
availableSeats = 100
# ticketsList = [["❌"] * cols for _ in range(rows)]
bookings_per_row = [0] * 10
revenue_per_row = [0] * 10


seats_file_path = 'C:/Users/hp/Music/PYTHON GATEWAY/theatre/Seats.txt'
bookingFilePath = 'C:/Users/hp/Music/PYTHON GATEWAY/theatre/SeatBookings.txt'
collectionFilePath='C:/Users/hp/Music/PYTHON GATEWAY/theatre/Collection.txt'


def writeDefaultSeats():
    with open(seats_file_path, 'w', encoding='utf-8') as f:
        for _ in range(rows):
            for col in range(cols):
                f.write("❌")
                if col < cols - 1:
                    f.write("\t")
            f.write("\n")  

def readSeatsFromFile():
    ticketsList = []
    with open(seats_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            seats = line.strip().split("\t")
            ticketsList.append(seats)
    return ticketsList

def writeSeatsToFile():
    with open(seats_file_path, 'w', encoding='utf-8') as f:
        for row in ticketsList:
            f.write("\t".join(row) + "\n")


def calcAvailableSeats():
    return sum(row.count("❌") for row in ticketsList)


def seatBookings(row, start_col, count, totalBill):
    if not os.path.exists(bookingFilePath):
        open(bookingFilePath, 'w').close()
    with open(bookingFilePath, 'a') as f:
        today=datetime.now().strftime("%Y-%m-%d")
        for c in range(start_col, start_col + count):
            f.write(f"{today}, Row: {row+1}, Col: {c+1}, Rs.{totalBill//count}\n")
        f.write(f"Total Bill: {totalBill}\n\n")




def removeBookingFromFile(row, start_col, count, refundBill):
    if not os.path.exists(bookingFilePath):
        return
    today = datetime.now().strftime("%Y-%m-%d")
    price = refundBill // count
    seats_to_remove = [
        f"{today}, Row: {row+1}, Col: {c+1}, Rs.{price}"
        for c in range(start_col, start_col + count)
    ]
    with open(bookingFilePath, 'r') as f:
        lines = f.readlines()
    new_lines = []   #contains booked seats and total bill line
    current_block = [] #contains booked seats
    for line in lines:
        if line.strip() in seats_to_remove:
            continue 
        elif line.strip().startswith("Total Bill:"):
            total = 0
            for seat_line in current_block:
                if "Rs." in seat_line:
                    total += int(seat_line.strip().split("Rs.")[-1])
            new_lines.extend(current_block)
            new_lines.append(f"Total Bill: {total}\n\n")
            current_block = []
        elif line.strip().startswith(today):
            current_block.append(line)
        else:
            new_lines.append(line)
    with open(bookingFilePath, 'w') as f:
        f.writelines(new_lines)


# def collectionFile():
#     displayLines = []
#     displayLines.append("\n----------------- COLLECTION REPORT -----------------")
#     total_seats_booked = sum(bookings_per_row)
#     total_revenue = sum(revenue_per_row)
#     displayLines.append(f"Total seats booked: {total_seats_booked}")
#     displayLines.append(f"Total revenue: Rs.{total_revenue}")
#     displayLines.append("\nDetailed Row-wise Report:")
#     displayLines.append("Row\tPrice\t\tSeats Booked\tRevenue")
#     displayLines.append("-----------------------------------------------------")

#     for i in range(10):
#         if bookings_per_row[i] > 0:
#             row_price = calculatePrice(i, 1)
#             displayLines.append(f"{i + 1}\tRs.{row_price}\t\t{bookings_per_row[i]}\t\tRs.{revenue_per_row[i]}")

#     displayLines.append("-----------------------------------------------------")

#     # Write to file
#     with open(collectionFilePath, "w") as file:
#         for line in displayLines:
#             file.write(line + "\n")

#     # Read from file and display on terminal
#     with open(collectionFilePath, "r") as file:
#         content = file.read()
#         print(content)


        

        



def displaySeats():
    print("\n----------------------------🍿📽️ TICKET BOOKING📽️ 🍿------------------------------")
    for innerList in ticketsList:
        for element in innerList:
            print(element, end="\t")
        print()
    print("--------------------------------------------------------------------------")
    print(f"Total seats: 100")
    print(f"Available seats: {availableSeats}\n")


def movies():
    print("\n\n--------🎬 🎦 Movie shows today🎬 🎦-----------")
    print("1️⃣  Mufasa\n2️⃣  Ginny and Georgia\n3️⃣  Venom\n")
    movie=int(input("Which movie do you want to watch? "))
    if movie==1 or movie==2 or movie==3:
        displaySeats()
    else:
        print("⚠️  : Invalid input!")


def calculatePrice(row, count):
    row_num = row + 1
    if 1 <= row_num <= 4:
        return 120 * count
    elif 5 <= row_num <= 6:
        return 160 * count
    elif 7 <= row_num <= 10:
        return 200 * count
    else:
        return 0
    

def showPrice():
    print("---------------------------------------")
    print("Price for row 1 to 4 is: Rs.120")
    print("Price for row 5 & 6 is: Rs.160")
    print("Price for row 7 to 10 is: Rs.200")
    print("---------------------------------------")


def seatChoice(action):
    while True:
        try:
            count = int(input(f"\nEnter the no. of seats to {action}: "))
            if count > 10:
                print(f"⚠️ : You can {action} only 10 seats at once. Try again.\n")
                continue
            elif count <= 0 or count > 100:
                print("⚠️ : Invalid seat count. Try again.\n")
                continue
            row = int(input("Enter row no. (1-10): ")) - 1
            start_col = int(input("Enter starting column no. (1-10): ")) - 1
            if 0 <= row < rows and 0 <= start_col < cols:
                if start_col + count > cols:
                    print("⚠️ : Seat range exceeds the row limit. See tickets chart and Try again.\n")
                    continue
                return row, start_col, count
            else:
                print("⚠️ : Invalid row or column. Try again.\n")
        except ValueError:
            print("⚠️ : Invalid input! Enter only numeric value.\n")
            

def bookSeat():
    global ticketsList, availableSeats, bookings_per_row, revenue_per_row
    global booked
    showPrice()
    while True:
        seat_data = seatChoice("book")
        if seat_data is None:
            return
        row, start_col, count = seat_data
        available_count = 0
        for c in range(start_col, start_col + count):
            if ticketsList[row][c] == "❌":
                available_count += 1
        if available_count < count:
            print("⚠️ : Some seats in the selected range are already booked. See tickets chart\n")
            displaySeats()
            choice = input("Do you want to enter another range? (y/n): ").strip().lower()
            if choice == "y":
                continue
            elif choice == "n":
                if available_count == 0:
                    print("⚠️ : No seats are available to book in that range. Booking cancelled.\n")
                    return
                confirm = input("Do you want to proceed with booking the remaining available seats? (y/n): ").strip().lower()
                if confirm == "y":
                    booked = 0
                    for c in range(start_col, start_col + count):
                        if ticketsList[row][c] == "❌":
                            ticketsList[row][c] = "✅"
                            availableSeats -= 1
                            booked += 1
                    print(f"{booked} seat(s) booked in row {row + 1}.")
                    availableSeats=calcAvailableSeats()
                    writeSeatsToFile()
                    totalBill = calculatePrice(row, booked)

                    seatBookings(row, start_col, booked, totalBill)

                    print(f"Total bill: Rs.{totalBill}")
                    bookings_per_row[row] += booked
                    revenue_per_row[row] += totalBill
                    return 
                else:
                    print("Booking cancelled.")
                    return
            else:
                print("⚠️ : Invalid input. Booking cancelled.\n")
                return
        else:
            for c in range(start_col, start_col + count):
                ticketsList[row][c] = "✅"
                availableSeats -= 1
            print(f"\n{count} seat(s) booked in row {row + 1}.")
            writeSeatsToFile()
            availableSeats=calcAvailableSeats()
            totalBill = calculatePrice(row, count)
            seatBookings(row, start_col, count, totalBill)
            print(f"Total bill: Rs.{totalBill}")
            bookings_per_row[row] += count
            revenue_per_row[row] += totalBill
            return


def cancelSeat():
    global ticketsList, availableSeats, bookings_per_row, revenue_per_row
    while True:
        seat_data = seatChoice("cancel")
        if seat_data is None:
            return
        row, start_col, count = seat_data
        booked_count = 0
        for c in range(start_col, start_col + count):
            if ticketsList[row][c] == "✅":
                booked_count += 1
        if booked_count < count:
            print("⚠️ : Some of the selected seats are not currently booked. See tickets chart.\n")
            displaySeats()
            choice = input("Do you want to enter another range? (y/n): ").strip().lower()
            if choice == "y":
                continue
            elif choice == "n":
                if booked_count == 0:
                    print("⚠️ : No booked seats found in the selected range. Cancellation cancelled.\n")
                    return
                confirm = input("Do you want to proceed with cancelling the remaining booked seats? (y/n): ").strip().lower()
                if confirm == "y":
                    for c in range(start_col, start_col + count):
                        if ticketsList[row][c] == "✅":
                            ticketsList[row][c] = "❌"
                            availableSeats += 1
                    print(f"{booked_count} seat(s) cancelled in row {row + 1}.")
                    writeSeatsToFile()
                    availableSeats=calcAvailableSeats()
                    refundBill=calculatePrice(row, booked_count)
                    print(f"Money refunded: Rs.{refundBill}")
                    bookings_per_row[row] -= booked_count
                    revenue_per_row[row] -= refundBill
                    removeBookingFromFile(row,start_col,booked_count,refundBill)
                    return
                else:
                    print("Cancellation cancelled.")
                    return
            else:
                print("⚠️ : Invalid input. Cancellation cancelled.\n")
                return
        else:
            for c in range(start_col, start_col + count):
                ticketsList[row][c] = "❌"
                availableSeats += 1
            print(f"{count} seat(s) cancelled in row {row + 1}.")
            refundBill=calculatePrice(row, booked_count)
            writeSeatsToFile()
            availableSeats=calcAvailableSeats()
            print(f"Money refunded: Rs.{refundBill}")
            bookings_per_row[row] -= booked_count
            revenue_per_row[row] -= refundBill
            removeBookingFromFile(row,start_col,count,refundBill)
            return


def collection():
    print("\n----------------- COLLECTION REPORT -----------------")
    total_seats_booked = sum(bookings_per_row)
    total_revenue = sum(revenue_per_row)
    print(f"Total seats booked: {total_seats_booked}")
    print(f"Total revenue: Rs.{total_revenue}")
    print("\nDetailed Row-wise Report:")
    print("Row\tPrice\t\tSeats Booked\tRevenue")
    print("-----------------------------------------------------")
    for i in range(10):
        if bookings_per_row[i] > 0:
            row_price = calculatePrice(i, 1)
            print(f"{i + 1}\tRs.{row_price}\t\t{bookings_per_row[i]}\t\tRs.{revenue_per_row[i]}")
    print("-----------------------------------------------------")






def menu():
    # movies()
    displaySeats()
    while True:
        print("\nMENU:\n1. Show seat info\n2. Book seats\n3. Cancel seats\n4. See collection\n5. Quit")
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            displaySeats()
        elif choice == 2:
            bookSeat()
        elif choice == 3:
            cancelSeat()
        elif choice==4:
            collection()
        elif choice == 5:
            print("Quitting...🔒")
            break
        else:
            print("⚠️ : Invalid choice.\n")


if not os.path.exists(seats_file_path):
    writeDefaultSeats()
ticketsList = readSeatsFromFile()
availableSeats=calcAvailableSeats()
# verify
# for row in ticketsList:
#     print(row)
menu()
