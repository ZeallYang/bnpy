#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:44:02 2019

@author: crystal
"""
import numpy as np

## extract DP parameters and organize them into a function
def extractDPParam(model, dataset):
    LP = model.calc_local_params(dataset)
    LPMtx = LP['E_log_soft_ev']
    ## to obtain hard assignment of clusters for each observation
    Y = LPMtx.argmax(axis=1)
    
    ## obtain sufficient statistics from DP
    SS = model.get_global_suff_stats(dataset, LP, doPrecompEntropy=1)
    Nvec = SS.N
    
    ## get the number of clusters
    K = model.obsModel.Post.K
    
    m = model.obsModel.Post.m
    
    # get the posterior covariance matrix
    B = model.obsModel.Post.B
    
    # degree of freedom
    nu = model.obsModel.Post.nu
    
    # scale precision on parameter m, which is lambda parameter in wiki for Normal-Wishart dist
    kappa = model.obsModel.Post.kappa
    
    ## save the variables in a dictionary
    DPParam = dict()
    DPParam['LPMtx'] = LPMtx
    DPParam['Y'] = Y
    DPParam['Nvec'] = Nvec
    DPParam['K'] = K
    DPParam['m'] = m
    DPParam['B'] = B
    DPParam['nu'] = nu
    DPParam['kappa'] = kappa
    return DPParam

def obtainObsInd4Cluster(Y, clusterLabel):
    ind = np.where(Y == clusterLabel)[0]
    return ind
    

def obtainObsInd4MultiCluster(Y, multiClusterLabel):
    result = dict()
    for value in multiClusterLabel:
        result[value] = obtainObsInd4Cluster(Y, value)
    return result

def obtainTrueClusterLabel4FittedCluster(trueY, fittedY, fittedCluster):
    """
    This function returns the true cluster label for a fitted cluster given true 
    labels and fitted cluster labels. For example, if in a fitted cluster, there 
    are 10 data points, and 7 of them has comes from the true cluster with label
    5, this cluster should match with the true cluster label 5. 
    Args:
        trueY: true cluster label for each observation
        fittedY: the fitted cluster label for each observation
        fittedCluster: the given fitted cluster Label
    Returns:
        the true cluster label correspond to the majority of the observations 
        in the fitted cluster with label fittedCluster
    """
    ## this code has been tested
    ## find the observations in the fitted cluster with cluster label fittedCluster
    ind = obtainObsInd4Cluster(fittedY, fittedCluster)
    trueClusters = trueY[ind]
    uniqueTrueCluster, counts = np.unique(trueClusters, return_counts=True)
    ## find the true cluster label with the largest number of counts by 
    ## returning the index of counts with has the maximum value
    majorityInd = np.argmax(counts)
    ## obtain the proportion of the obs has the majority cluster label, 
    ## which is also the precision
    prec = counts[majorityInd]/len(ind)
    majorityCluster = uniqueTrueCluster[majorityInd]
    
    result = dict()
    result['prec'] = prec
    result['TrueCluster'] = majorityCluster
    result['recall'] = counts[majorityInd]/len(np.where(trueY==majorityCluster)[0])
    result['fittedCluster'] = fittedCluster
    return result

def obtainTrueClusterLabel4AllFittedCluster(trueY, fittedY):
    allFittedClasses, fittedCount = np.unique(fittedY, return_counts=True)
    allResult = dict()
    for fittedCluster in allFittedClasses:
        fittedClusterRes = obtainTrueClusterLabel4FittedCluster(trueY, fittedY, fittedCluster)
        allResult[fittedCluster] = fittedClusterRes
    return allResult
        

## create a function to obtain a dict with key as true cluster labels 
## and values to match to all the fitted cluster labels
acc_single_number(trueY, fittedY, 3, 1)





       


## create cluster functions to obtain cluster measures like rand index, F measure,
## purity and normalized mutual information    
    
    

    



def acc_single_number(trueY, fittedY, clusterTrue, clusterFitted):
    trueInd = np.where(trueY==clusterTrue)[0]
    numTrue = len(trueInd)
    fittedInd = np.where(fittedY==clusterFitted)[0]
    ## proportion of fittedInd in trueInd
    truePos = np.intersect1d(fittedInd, trueInd)
    
    precision = len(truePos)/len(fittedInd)
    recall = len(truePos)/len(trueInd)
    
    ## find the element in trueInd but not in fittedInd
    indDiff = np.setdiff1d(trueInd, fittedInd)
    otherCluster, counts = np.unique(fittedY[indDiff], return_counts=True)
    
    result = dict()
    result['prec'] = precision
    result['recall'] = recall
    result['trueInd'] = trueInd
    result['fittedInd'] = fittedInd
    result['indDiff'] = indDiff
    result['otherClusterOfFitted'] = otherCluster
    result['countsOfOtherCluster'] = counts
    return result