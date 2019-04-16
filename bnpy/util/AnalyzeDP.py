#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:44:02 2019

@author: crystal
"""

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

def acc_single_number(trueY, fitteY, clusterTrue, clusterFitted):
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