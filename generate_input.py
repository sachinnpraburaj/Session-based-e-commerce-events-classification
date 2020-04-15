from data_utils import *
import argparse, sys

def main(window):
    input = classifierInputData()
    input.read_data()
    if (window <= 0):
        print("Demand window cannot be <= 0")
        sys.exit()
    else:
        input.get_input_data(window)
    input.df.to_csv('preprocessed_data/classifier_input.csv',index=False)
    print('"classifier_input.csv" successfully stored at "/preprocessed_data"')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("-w", "--demand_window", help='number of days to calculate average product demand', type=int, default=1)
    args=parser.parse_args()
    main(args.demand_window)
