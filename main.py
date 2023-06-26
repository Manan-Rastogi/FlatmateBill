from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from dotenv import load_dotenv
from filestack import Security, Client, Filelink
import os

load_dotenv()

class Flatmate:
    """
    Creates a Flatmate(Person) Who lives in the flat and pays a share of the bill.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house



class Bill:
    """
    Bill class contains data about a bill, such as Total Amount, Period.
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period

    def generateIndividualBill(self, flatname1: Flatmate, flatname2: Flatmate):

        return {
            flatname1.name: flatname1.days_in_house*self.amount / (flatname1.days_in_house + flatname2.days_in_house),
            flatname2.name: flatname2.days_in_house*self.amount / (flatname1.days_in_house + flatname2.days_in_house)
        }


class PdfReport:
    """
    Creates a PDF Report for the bill.
    """

    def __init__(self):
        pass
    
    def generate(self, flatname1: Flatmate, flatname2: Flatmate, bills: dict, bill: Bill):
        filename = str(flatname1.name).replace(" ", "") + "_" + str(flatname2.name).replace(" ", "") + "_" + str(bill.period).replace(" ", "_") + ".pdf"
        c = canvas.Canvas(filename, pagesize=A4)

        c.setFont("Helvetica", 12)

        # Add some text to the PDF
        text = flatname1.name + " - " + flatname2.name + " Bill Split"
        c.drawString(100, 750, text)

        # Draw a line
        c.line(100, 730, 500, 730)

        c.drawString(100, 700, flatname1.name + ": ")
        c.drawString(200, 700, str(format(bills[flatname1.name], '.2f')) + " for " + str(flatname1.days_in_house) + " days.")

        c.drawString(100, 680, flatname2.name + ": ")
        c.drawString(200, 680, str(format(bills[flatname2.name], '.2f')) + " for " + str(flatname2.days_in_house) + " days.")


        c.drawString(100, 650, "Total Bill: " + str(format(bill.amount, '.2f')))
        c.drawString(100, 630, "Payable: "+ str(format(bills[flatname1.name] + bills[flatname2.name], '.2f')))


        c.save()


        # Filestack
        client = Client(os.environ.get("API_KEY"))
        filelink = client.upload(filepath=filename)

        print(filelink.url)
        


if __name__ == "__main__" :
    
    amount = float(input("Enter the Total bill amount: "))
    period = input("Enter the Period of the bill (eg March 2023): ")
    bill = Bill(amount, period)

    
    

    name1 = input("Enter name of 1st Flatmate: ")
    days_in_house1 = int(input("Enter no of days for {}: ".format(name1)))
    flatmate1 = Flatmate(name1, days_in_house1)

    name2 = input("Enter name of 2nd Flatmate: ")
    days_in_house2 = int(input("Enter no of days for {}: ".format(name2)))
    flatmate2 = Flatmate(name2, days_in_house2)

    bills = bill.generateIndividualBill(flatname1= flatmate1, flatname2= flatmate2)

    print(bills)
   
    pdf = PdfReport()

    pdf.generate(flatname1= flatmate1, flatname2=flatmate2, bills=bills, bill=bill)
