#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:44:02 2019

@author: crystal
"""
import numpy as np
from bnpy.data.XData import XData

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
    DPParam['model'] = model
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
    result['trueCluster'] = majorityCluster
    count_trueY = len(np.where(trueY==majorityCluster)[0])
    result['recall'] = counts[majorityInd]/count_trueY
    result['count_trueY4trueCluster'] = count_trueY 
    result['overallRecallCount'] = counts[majorityInd]
    result['fittedCluster'] = fittedCluster
    return result

def obtainTrueClusterLabel4AllFittedCluster(trueY, fittedY):
    allFittedClasses, fittedCount = np.unique(fittedY, return_counts=True)
    allResult = dict()
    for fittedCluster in allFittedClasses:
        fittedClusterRes = obtainTrueClusterLabel4FittedCluster(trueY, fittedY, fittedCluster)
        allResult[fittedCluster] = fittedClusterRes
    return allResult
        

def obtainDictFromTrueToFitted(dictFitted2True):
    """
    This function returns the dictionary from a given true class label to 
    the cluster label in the fitted clusters, predicted given the model
    dictFitted2True = obtainTrueClusterLabel4AllFittedCluster(trueY, fittedY)
    Args:
        dictFittedToTrue should be a result from obtainTrueClusterLabel4AllFittedCluster
    Returns:
        a dictionary with each key as the true cluslter label
        and the values to each key as the label of the fitted cluster to this true label
    """
    ## obtain all the fitted cluster labels, which is all the keys to dictFitted2True
    ## correctness of this function has been tested
    allFClusters = dictFitted2True.keys()
    resultTrue2Fitted = dict()
    
    for fittedCluster in allFClusters:
        trueCluster = dictFitted2True[fittedCluster]['trueCluster']
        fittedCluster = dictFitted2True[fittedCluster]['fittedCluster']
        ## check if trueCluster exists in the keys of resultTrue2Fitted
        if not trueCluster in resultTrue2Fitted.keys():
            resultTrue2Fitted[trueCluster] = list()
            resultTrue2Fitted[trueCluster].append(fittedCluster)
        else:
            if not fittedCluster in resultTrue2Fitted[trueCluster]:
                resultTrue2Fitted[trueCluster].append(fittedCluster)
    ## ToDo: sort the keys in an increasing order
    return resultTrue2Fitted



################################################################################################
    


## add metrics calculation function for clusters
from sklearn.metrics import accuracy_score, normalized_mutual_info_score, adjusted_rand_score,silhouette_score
from sklearn.metrics.cluster import homogeneity_score, completeness_score,v_measure_score

def clusterEvaluation(trueY, fittedY):
    result = dict()
    ## NMI denotes normalized mutual information
    ## ARS denotes adjusted rand score
    ## HS stands for homogeneity_score, 1 means perfect
    ## VM represents v_measure_score ranging [0, 1], 1.0 is perfectly complete labeling
    ## SS represents silhouette_score
    result['NMI'] = normalized_mutual_info_score(trueY, fittedY)
    result['ARS'] = adjusted_rand_score(trueY, fittedY)
    result['HS'] = homogeneity_score(trueY, fittedY)
    result['CS'] = completeness_score(trueY, fittedY)
    result['VM'] = v_measure_score(trueY, fittedY)
    return result

def clusterAccuracy(trueY, fittedY):
    dictFitted2True = obtainTrueClusterLabel4AllFittedCluster(trueY, fittedY)
    total_count = len(trueY)
    count = 0
    for key in dictFitted2True.keys():
        values = dictFitted2True[key]
        if values['prec'] >0.5 or values['recall'] >0.5:
            count += values['overallRecallCount']
    acc = count/total_count
    clusterMatch = obtainDictFromTrueToFitted(dictFitted2True)
    result = dict()
    result['overallRecall'] = acc
    result['match'] = clusterMatch
    result['details'] = dictFitted2True 
    result['moreEvaluation'] = clusterEvaluation(trueY, fittedY)
    return result



def obtainSilhouetteScore(X, fittedY):
    ## this score can be used to select the number of clusters
    ## a value closer to 1 is better
    ## A value of 0 indicates that the sample is on or very close to the decision 
    ## boundary between two neighboring clusters and negative values indicate that 
    ## those samples might have been assigned to the wrong cluster.
    """
    Args: X is the original sample data used for clustering
          fittedY represents the fitted cluster label
    Returns: silhouette_score, a score close to 0 indicates good clustering
    """
    result = silhouette_score(X, fittedY)
    return result

##################################################
def obtainFittedYFromDP(DPParam, z_fit):
    """
    Given the fitted dp model saved in DPParam and the observation, in the 
    VAE case, z_fit represents the latent representation, this function
    return the fittedY cluster label from the DP model for all observations
    in z_fit
    Args:
        DPParam: the object saves the fitted DP_model
        z_fit: the observation to be fit into the DP_model, it should be of 
        XData class in bnpy, if not, convert it to XData type
    Return:
        the fitted cluster label for each observation in z_fit
    """
    dp_model = DPParam['model']
    ## transform z_fit to XData
    if not isinstance(z_fit, XData):
        z_fit = XData(z_fit)
    LP = dp_model.calc_local_params(z_fit)
    LPMtx = LP['E_log_soft_ev']
    ## to obtain hard assignment of clusters for each observation
    fittedY = LPMtx.argmax(axis=1)
    return fittedY
    


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