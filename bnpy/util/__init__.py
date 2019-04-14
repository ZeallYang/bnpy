"""
The :mod:`util` module gathers utility functions
"""

import util.RandUtil
import util.OptimizerForPi

from util.PrettyPrintUtil import np2flatstr, flatstr2np
from util.PrettyPrintUtil import split_str_into_fixed_width_lines
from util.MatMultUtil import dotATA, dotATB, dotABT
from util.MemoryUtil import getMemUsageOfCurProcess_MiB, calcObjSize_MiB
from util.RandUtil import choice, multinomial
from util.SpecialFuncUtil import MVgammaln, MVdigamma, digamma, gammaln
from util.SpecialFuncUtil import LOGTWO, LOGPI, LOGTWOPI, EPS
from util.SpecialFuncUtil import logsumexp
from util.VerificationUtil import isEvenlyDivisibleFloat, assert_allclose
from util.ShapeUtil import as1D, as2D, as3D, toCArray
from util.ShapeUtil import argsort_bigtosmall_stable, is_sorted_bigtosmall
from util.ShapeUtil import argsortBigToSmallByTiers
from util.ParallelUtil import numpyToSharedMemArray, sharedMemToNumpyArray
from util.ParallelUtil import sharedMemDictToNumpy, fillSharedMemArray

__all__ = ['RandUtil', 'OptimizerForPi',
           'split_str_into_fixed_width_lines',
           'np2flatstr', 'flatstr2np',
           'dotATA', 'dotATB', 'dotABT',
           'choice', 'multinomial',
           'MVgammaln', 'MVdigamma', 'logsumexp', 'digamma', 'gammaln',
           'isEvenlyDivisibleFloat', 'assert_allclose',
           'LOGTWO', 'LOGTWOPI', 'LOGPI', 'EPS',
           'as1D', 'as2D', 'as3D', 'toCArray',
           'argsort_bigtosmall_stable', 'is_sorted_bigtosmall',
           'argsortBigToSmallByTiers',
           'numpyToSharedMemArray', 'sharedMemToNumpyArray',
           'sharedMemDictToNumpy', 'fillSharedMemArray',
           'getMemUsageOfCurProcess', 'calcObjSize_MiB',
           ]
