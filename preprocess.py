from data_utils import *
import sys

def main(filter_flag,min,max):
    process = ProcessData()
    process.optimized_read()
    print("\nBefore Pre-processing (optimized data):")
    process.verify_preprocess()
    process.pre_process()
    print("\nAfter Pre-processing:")
    process.verify_preprocess()
    if filter_flag == 1:
        if min is None:
            if max is None:
                process.filter_products(min,max)
            else:
                process.filter_products(min)
        else:
            process.filter_products()
        process.filtered_df.to_csv('preprocessed_data/filtered_data.csv',index=False)
    process.df.to_csv('preprocessed_data/data.csv',index=False)


if __name__ == '__main__':
    try:
        filter_flag = int(sys.argv[1])
    except:
        filter_flag = 0

    if filter_flag == 1:
        try:
            min = int(sys.argv[2])
        except:
            min = None
        try:
            max = int(sys.argv[3])
        except:
            max = None
    else:
        min = None
        max = None

    main(filter_flag,min,max)
