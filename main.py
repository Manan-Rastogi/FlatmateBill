from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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
        



bill = Bill(amount=20000, period="March 2023")
virat = Flatmate(name="Virat Kohli", days_in_house=21)
rohit = Flatmate(name="Rohit Sharma", days_in_house=25)

bills = bill.generateIndividualBill(flatname1= virat, flatname2= rohit)

pdf = PdfReport()

pdf.generate(flatname1= virat, flatname2=rohit, bills=bills, bill=bill)