import argparse
from os import write
parser = argparse.ArgumentParser(description="A simple script with command-line arguments.")

if __name__ == "__main__":
    parser.add_argument("--sample",help="some sample")
    args = parser.parse_args()
    with open("nigga.DAT","w") as file:
        file.write(args.sample)