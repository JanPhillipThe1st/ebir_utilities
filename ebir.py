import argparse
import datetime
import glob
import logging
import re
# Get a logger instance (or create a new one if it doesn't exist)
logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO) # Set the minimum logging level
# Create a console handler and set its formatter
# Create a file handler
file_handler = logging.FileHandler('runs.log')
file_handler.setLevel(logging.INFO) # Set the handler's level

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(file_handler)

parser = argparse.ArgumentParser(description="A simple script with command-line arguments.")

wh_agent_data = dict()
def getWithholdingAgentDetails(*args):
    global wh_agent_data
    args= parser.parse_known_args()[0]
    wh_agent_data = vars(args)
    
    if wh_agent_data["TIN"] == "000-000-000":
        tin = input("Please input tin in Format 000-000-000:")
        wh_agent_data["TIN"] = tin
        pass
    if wh_agent_data["RDO"] is None:
        rdo = input("Please RDO code in format (092):")
        wh_agent_data["RDO"] = rdo
        pass
    if wh_agent_data["branch_code"] is None:
        branch_code = input("Please input branch_code in Format (0000):")
        wh_agent_data["branch_code"] = branch_code
        pass
    if wh_agent_data["month"] is None:
        month = input("Please input month in Format (04):")
        wh_agent_data["month"] = month
        pass
    if wh_agent_data["year"] is None:
        year = input("Please input year in Format (2025):")
        wh_agent_data["year"] = year
        pass
    if wh_agent_data["barangay"] is None:
        barangay = input("Please input barangay in Format (SAN JOSE):")
        wh_agent_data["barangay"] = barangay
        pass
    
def getTransactions() -> tuple():
    global wh_agent_data
    transactions = set()
    item_number = 1
    total_wh_amount = 0
    total_wh_tax = 0
    while True:
        if input("Would you like to add another record?" if len(transactions) >0 else "Press Enter to Input Transaction: ").lower() != "n":
            line = "D1,1601EQ,"+item_number+","+input("Input Business TIN (format:'123456999'): ")+ ","
            line += input("Input Branch Code (format: 0000): ") + ","
            line += f'"{input("Input Business Name: ")}",'
            line += input("(Optional) Input owner LAST name: ") +","
            line += input("(Optional) Input owner FIRST name: ") +","
            line += input("(Optional) Input owner MIDDLE name: ") +","
            line += f"{wh_agent_data["month"]}/{wh_agent_data["year"]},"
            witheld_amount = float(input("Withheld Amount: "))
            atc = input("Input ATC in format (WI158): ")
            atc = atc.upper()
            vat = 1
            match atc:
                case "WI158":
                    vat = 1
                case "WC157":
                    vat = 2
                case _:
                    vat = 1
            line += f"{atc},{vat:.2f},{witheld_amount:.2f},{(witheld_amount/100) * vat:.2f}\n"
            total_wh_amount += witheld_amount
            total_wh_tax += (witheld_amount/100) * vat
            transactions.add(line)
            print(transactions)
            item_number += 1
            pass
        else:
            break
    return (transactions,total_wh_amount,total_wh_tax)
if __name__ == "__main__":
    #get arguments
    current_date = datetime.datetime.now()
    parser.add_argument("--RDO",help="RDO code")
    parser.add_argument("--TIN",help="Format: '000-000-000'",default="000-000-000")
    parser.add_argument("--branch_code",help="THE LAST 4 DIGITS OF YOUR TIN")
    parser.add_argument("--month",help="Example: April = '--month 04'",default=str(current_date.month).zfill(2))
    parser.add_argument("--year",default=str(current_date .year))
    parser.add_argument("--barangay")
    parser.add_argument("--city",default="PAGADIAN CITY")
    parser.add_argument("--province",default="ZAMBOANGA DEL SUR")
    args,unknown_args = parser.parse_known_args()
    #000-456-123 to 000456123 
    #Create file name
    getWithholdingAgentDetails(args)
    tin = re.sub("[^0-9]+","",wh_agent_data["TIN"])
    file_name = "".join([tin,wh_agent_data["branch_code"],wh_agent_data["month"],wh_agent_data["year"],"1601EQ"])
    
    logger.info("Args: ")
    with open("1601EQ/"+file_name+".DAT","w") as file:
        file.write(f"HQAP,H1601EQ,{tin},{wh_agent_data["branch_code"]},{str(wh_agent_data["barangay"]).upper()} {str(wh_agent_data["city"]).upper()} {str(wh_agent_data["province"]).upper()},{wh_agent_data["month"]}/{wh_agent_data["year"]},{wh_agent_data["RDO"]}")
        file.write("\n")
        (transactions,total_wh_amount,total_wh_tax) = getTransactions()
        file.writelines(transactions)
        # C1,1601EQ,<<WH_AGENT_TIN>>,<<WH_AGENT_TIN_SUFFIX>>,MM/YYYY,<<TOTAL_WH_AMOUNT>>,<<TOTAL_WH_TAX>>
        file.write(f"C1,1601EQ,{tin},{wh_agent_data["branch_code"]},{wh_agent_data["month"]}/{wh_agent_data["year"]},{total_wh_amount:.2f},{total_wh_tax:.2f}")
        
        