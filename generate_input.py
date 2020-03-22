from data_utils import *
import sys

def main(window):
    input = classifierInputData()
    input.read_data()
    if window is None:
        input.get_input_data()
    else:
        input.get_input_data(window)
    input.df.to_csv('preprocessed_data/classifier_input.csv',index=False)


if __name__ == '__main__':
    try:
        window = int(sys.argv[1])
    except:
        window = None

    main(window)
