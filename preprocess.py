from data_utils import *
import argparse, sys

def main(filter_flag,min,max):
    process = ProcessData()
    process.optimized_read()
    print("\nBefore Pre-processing (optimized data):")
    process.verify_preprocess()
    process.pre_process()
    print("\nAfter Pre-processing:")
    process.verify_preprocess()
    if filter_flag == True:
        process.filter_products(min,max)
        process.filtered_df.sort_values('event_time').to_csv('preprocessed_data/filtered_data.csv',index=False)
        print('"filtered_data.csv" successfully stored at "/preprocessed_data"')
    process.df.sort_values('event_time').to_csv('preprocessed_data/data.csv',index=False)
    print('"data.csv" successfully stored at "/preprocessed_data"')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--filter_flag", help="flag for filtering the dataset", action="store_true", default=False)
    parser.add_argument("--min", help="minimum number of user_sessions per product", type=int, default=100)
    parser.add_argument("--max", help="maximum number of user_sessions per product", type=int, default=1100)
    args=parser.parse_args()
    main(args.filter_flag,args.min,args.max)
