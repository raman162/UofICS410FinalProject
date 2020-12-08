import numpy as np
import math
import pandas as pd


class TelehealthMiner(object):
    def __init__(self, data_path):
        """
        This is init function
        """
        print('This is init function')
        self.data_path = data_path

        self.pos_en_path = data_path + 'positive_encounters.res-sample-50.res.csv'
        self.no_pos_en_path = data_path + 'no_positive_encounters.res-sample-50.res.csv'

        self.pos_note_path = data_path + 'positive_notes.txt'
        self.no_pos_note_path = data_path + 'no_positive_notes.txt'

        self.pos_purpose_path = data_path + 'positive_purpose.txt'
        self.no_pos_purpose_path = data_path + 'no_positive_purpose.txt'

    def topic_miner(self):
        """
        This is topic miner function
        :return:
        """
        print('This is topic_miner')

    def extract_purpose_notes(self):
        """
        This function is to extract notes from the encounters CSV file
        :return:
        """
        pos_encounters = pd.read_csv(self.pos_en_path, sep=',', header='infer')
        no_pos_encounters = pd.read_csv(self.no_pos_en_path, sep=',', header='infer')

        with open(self.pos_note_path, 'w') as f:
            f.write(pos_encounters['note'].str.cat(sep='\n'))

        with open(self.no_pos_note_path, 'w') as f:
            f.write(no_pos_encounters['note'].str.cat(sep='\n'))

        with open(self.pos_purpose_path, 'w') as f:
            f.write(pos_encounters['purpose'].str.cat(sep='\n'))

        with open(self.no_pos_purpose_path, 'w') as f:
            f.write(no_pos_encounters['purpose'].str.cat(sep='\n'))

def main():
    """
    This is the main function
    :return:
    """
    data_path = '../data/'
    # Write the main code here
    miner = TelehealthMiner(data_path)
    miner.extract_purpose_notes()
    miner.topic_miner()


if __name__ == '__main__':
    main()
