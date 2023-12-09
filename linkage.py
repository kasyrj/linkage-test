#!/usr/bin/python3
# -*- coding=utf-8 -*-
#

import sys

class LinkageTest():
    def __init__(self):
        pass

    
    def __createPairwiseMatrix(self, x):
        '''Return a two-dimensional dict of the form data[x][x], where x is a list of keys. The endpoints have None as their value.

        :param x: List of items to use as keys.
        :type x: list of str

        :return: A dict of the form data[x][x]
        :rtype: dict of dict
        '''

        out = {}
        for item in x:
            out[item] = {}
            for item2 in x:
                out[item][item2] = None
        return out


    def run(self,data):
        '''Identify data point pairs with identical variants for each feature.
        Calculate the number of identical data point pairs between two features.
        Calculate linkage as the number of shared identical data point pairs between two features
        divided by the total number of identical data point pairs across two features (excluding data empty data point pairs among either feature.
        '''
        csv = []
        csv.append('"' + "feature_a"                + '"' + "," +
                   '"' + "feature_b"                + '"' + "," +
                   '"' + "potential_linkage"        + '"' + "," +
                   '"' + "actual_linkage"           + '"' + "," +
                   '"' + "linkage_percentage"       + '"' + "\n")
        
        # step 1: collect potentially linked data point pairs of each feature

        linked_pairs = {}                        # matching pairs of each feature
        feature_counter = 0                      # for bookkeeping
        feature_length = len(data.getFeatures()) # for bookkeeping
        for feature in data.getFeatures():
            empty_pairs = 0
            linked_pairs[feature] = {}             # dict to collect all linked datapoint pairs of a feature
            linked_pairs[feature]["empty"] = []    # for filtering
            linked_pairs[feature]["nonempty"] = [] # actual data
            feature_counter += 1
            print("Collecting potential linkage pairs for feature "
                  + str(feature)
                  + " (" + str(feature_counter) + "/" + str(feature_length) + ")", file=sys.stderr)
            datapoint_cache = self.__createPairwiseMatrix(data.getDatapoints())
            for x in data.getDatapoints():
                for y in data.getDatapoints():
                    if x == y:
                        # identical points; they are always linked and non-informative
                        datapoint_cache[x][y] = 1
                        continue
                        
                    if datapoint_cache[x][y] != None:
                        # symmetric pair already filled; not added to linked pairs
                        continue

                    x_features_present = []
                    x_features_absent  = []
                    y_features_present = []
                    y_features_absent  = []

                    for variant in data.getFeatureVariants(feature):

                        # presence in x and y
                        if data.featureVariantPresentInDatapoint(x,feature,variant):
                            x_features_present.append(variant)

                        if data.featureVariantPresentInDatapoint(y,feature,variant):
                            y_features_present.append(variant)

                        # meaningful absence in x and y
                        if data.featureVariantAbsentInDatapoint(x,feature,variant):
                            x_features_absent.append(variant)

                        if data.featureVariantAbsentInDatapoint(y,feature,variant):
                            y_features_absent.append(variant)

                    x_features = [x_features_present,x_features_absent]
                    y_features = [y_features_present,y_features_absent]
                    
                    if (x_features == y_features):
			# in case of missing data the present and absent lists are both empty
                        if (x_features == [[],[]]):
                            empty_pairs += 1
                            linked_pairs[feature]["empty"].append((x,y))
                        else:
                            linked_pairs[feature]["nonempty"].append((x,y))

                        datapoint_cache[x][y] = 1
                        datapoint_cache[y][x] = 1
            print("Empty pairs: " + str(empty_pairs), file=sys.stderr)
            print("Potentially linked pairs:" + str(len(linked_pairs[feature]["nonempty"])), file=sys.stderr)
        # step 2: calculate linkage between each map pair (after filtering one-sided empty pairs)

        feature_pairs = self.__createPairwiseMatrix(data.getFeatures())
        for x in data.getFeatures():
            print("Calculating linkage pairs for feature " + str(x) + ":", file=sys.stderr)
            counter = 0
            total_count = 0
            for y in data.getFeatures():
                if counter == 50:
                    print(str(total_count) + " feature pairs calculated.", file=sys.stderr)
                    counter = 0
                if x == y:
                    # identical features; for the sake of completion we can add 1.0
                    feature_pairs[x][y] = 1.0
                    continue

                if feature_pairs[x][y] != None:
                    # symmetric pair already filled and calculated
                    continue

                potential_pairs = set(linked_pairs[x]["nonempty"] + linked_pairs[y]["nonempty"])      # union of nonempties
                empty_pairs  = set(linked_pairs[x]["empty"] + linked_pairs[y]["empty"])               # union of empties
                pruned_potential_pairs = potential_pairs - empty_pairs                                # difference of nonempty and empty
                shared_pairs    = set(linked_pairs[x]["nonempty"]) & set(linked_pairs[y]["nonempty"]) # intersection of nonempties
                
                if len(pruned_potential_pairs) == 0:
                    # 0 potential linkage pairs. As this causes a divide by zero error, it has to be accounted for manually.
                    linkage = 0.0
                else:
                    linkage = float(len(shared_pairs)) / len(pruned_potential_pairs)
                
                feature_pairs[x][y] = linkage
                feature_pairs[y][x] = linkage
                    
                csv.append('"' + str(x)                    + '"' + "," +
                           '"' + str(y)                    + '"' + "," +
                           '"' + str(len(pruned_potential_pairs)) + '"' + "," +
                           '"' + str(len(shared_pairs))    + '"' + "," +
                           '"' + str(linkage)              + '"' + "\n")
                counter += 1
                total_count += 1
            print(str(total_count) + " feature pairs calculated. Done.", file=sys.stderr)
        return(csv)
