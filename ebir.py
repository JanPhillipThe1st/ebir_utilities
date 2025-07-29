import argparse
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

if __name__ == "__main__":
    #get arguments
    parser.add_argument("--RDO",help="RDO code")
    parser.add_argument("--TIN",help="Format: '000-000-000'",default="000-000-000")
    parser.add_argument("--branch_code",help="THE LAST 4 DIGITS OF YOUR TIN")
    parser.add_argument("--month",help="Example: April = '--month 04'",default="01")
    parser.add_argument("--barangay")
    parser.add_argument("--city",default="PAGADIAN CITY")
    parser.add_argument("--province",default="ZAMBOANGA DEL SUR")
    args = parser.parse_args()
    #000-456-123 to 000456123 
    tin = re.sub("[^0-9]+","",args.TIN)
    #Create file name
    tin = "".join([args.branch_code,args.branch_code])
    tin += "1601EQ"
    print(tin)
    
    
    logger.info("Args: ")
    with open(tin+".DAT","w") as file:
        file.write(args.month)