#!/usr/bin/python3

import sys
from abstractms import AbstractMultistate

class CSVBinaryDataset(AbstractMultistate):

    def getFeatures(self):
        '''Return a list of linguistic features (=map pages in Kettunen).'''
        features = list(self.__bm[list(self.__bm.keys())[0]].keys())
        features.sort(key=int)
        return features

    def getFeatureVariants(self,feature):
        '''Return a list of variants of the specified feature (=map page in Kettunen).'''
        variants = list(self.__bm[list(self.__bm.keys())[0]][feature].keys())
        variants.sort(key=int)
        return variants

    def getDatapoints(self):
        '''Return a list of all data points (e.g. municipalities in Kettunen)'''
        datapoints = list(self.__bm.keys())
        datapoints.sort()
        return datapoints
        
    def featureVariantPresentInDatapoint(self,datapoint,feature,variant):
        '''Return True if given feature variant is present in data point, or False if it is not. Meaningfully absent and missing both return False'''
        return(self.__bm[datapoint][feature][variant] == True)

    def featureVariantAbsentInDatapoint(self,datapoint,feature,variant):
        return(self.__bm[datapoint][feature][variant] == False)

    def featureVariantMissingInDatapoint(self,datapoint,feature,variant):
        return(self.__bm[datapoint][feature][variant] == None)

    def getAsciiDatapoint(self,datapoint):
        '''Return ASCII-safe name for datapoint'''
        return datapoint

    def getAsciiDatapoints(self):
        '''Return a list of ASCII-safe datapoint names in the same order as .name for datapoint'''
        return self.getDatapoints()

    def getName(self):
        '''Return the name of the dataset format.'''
        return 'CSV (binary representation)'
    
    def __init__(self, csv_dict, settings = {}):
        '''
        Create a matrix self.__bm[mun][map][vars][var]. For each var, the state may be:
        True  = present,
        False = meaningfully absent or
        None  = missing
        '''

        if settings == {}:
            print('Dataset settings not specified.')
            quit()

        self.__bm = {}    # main data store, dict[mun_id][map_page][char]. Equivalent for cognate data would be [language][meaning][cognate_set]

        # fill first level of datapoint IDs to self.__bm
        for i in range(len(csv_dict[settings["datapoint_id_column"]])):
            dp_id  = csv_dict[settings["datapoint_id_column"]][i]
            self.__bm[dp_id] = {}

        # fill second level of __bm = features
        # collect feature list
        features = []
        for i in csv_dict.keys():
            # feature columns are of format nnn_mmm where nnn is feature number and mmm is feature variant number
            split_key = i.split("_")
            if len(split_key) == 2:
                if split_key[0][0] in list("1234567890") and split_key[1][0] in list("1234567890"):
                    features.append(int(split_key[0]))

        # sort and remove duplicates
        features = sorted(set((features)))
        for i in range(len(features)):
            features[i] = str(features[i])

        # add features to each municipality of self.__bm
        for i in self.__bm.keys():
            for j in features:
                self.__bm[i][j] = {}

        # add characters to each feature of each data point
        counter = 0
        one_counter = 0
        current_chars = []
        for feature in features:
            chars = []
            # collect all valid variants for a feature from the header column. Essentially this is mmm in columns of the format nnn_mmm, where both are numbers.
            for j in csv_dict.keys():
                split_key = j.split("_")
                if (len(split_key) == 2 and split_key[0] == feature):
                    chars.append(split_key[1])

            # sort chars
            chars.sort(key=int)

            # print all relevant codes for a feature. Use this for sanity checks.
            print(feature + ":" + str(chars), file=sys.stderr)

            # add data to binary matrix
            fill_char = None
            for dp in self.__bm.keys():
                chars_in_dp = []
                row = None
                for j in range(len(csv_dict[settings["datapoint_id_column"]])):
                    if(csv_dict[settings["datapoint_id_column"]][j] == dp): # find correct datapoint row
                        row = j
                        break

                # find correct feature
                for j in csv_dict.keys():
                    split_key = j.split("_")
                    if (len(split_key) == 2 and split_key[0] == feature):

                        if csv_dict[j][row] == settings['meaningfully_empty_char']:
                            fill_char = False

                        if csv_dict[j][row] == settings['present_char']:
                            chars_in_dp.append(split_key[1])
                
                for char in chars:
                    if char in chars_in_dp:
                        self.__bm[dp][feature][char] = True
                        one_counter+=1
                    else:
                        self.__bm[dp][feature][char] = fill_char
                        counter += 1
        
    def __del__(self):
        pass
