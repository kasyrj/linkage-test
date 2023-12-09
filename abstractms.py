#!/usr/bin/python3
#
# Abstract base class for multistate dataset format. To add new file formats create a concrete implementation of the class

from abc import ABCMeta, abstractmethod

class AbstractMultistate(metaclass=ABCMeta):

    @abstractmethod
    def getFeatures(self):
        '''Return a list of features (such as map pages on Kettunen).'''
        pass

    @abstractmethod
    def getFeatureVariants(self,feature):
        '''Return variants of a feature, such as variants on one page of Kettunen.'''
        pass

    @abstractmethod
    def featureVariantPresentInDatapoint(self,datapoint,feature,variant):
        '''Return True if given feature variant is present in data point, False if it is meaningfully absent or missing'''
        pass
    
    def fetureVariantAbsentInDatapoint(self,datapoint,feature,variant):
        '''Return True if given feature variant is meaningfully absent in data point.'''
        pass

    def fetureVariantMissingInDatapoint(self,datapoint,feature,variant):
        '''Return True if given feature variant is missing in data point.'''
        pass
    
    @abstractmethod
    def getDatapoints(self):
        '''Return a list of all data points (municipalities in Kettunen, languages in phylogenetic data)'''
        pass

    @abstractmethod
    def getAsciiDatapoint(self,datapoint):
        '''Return ASCII-safe name for datapoint'''
        pass
    @abstractmethod

    def getName(self):
        '''Return the name of the dataset format.'''
        pass
