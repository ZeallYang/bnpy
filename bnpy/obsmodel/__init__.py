from obsmodel.DiagGaussObsModel import DiagGaussObsModel
from obsmodel.GaussObsModel import GaussObsModel
from obsmodel.ZeroMeanGaussObsModel import ZeroMeanGaussObsModel
from obsmodel.AutoRegGaussObsModel import AutoRegGaussObsModel
from obsmodel.MultObsModel import MultObsModel
from obsmodel.BernObsModel import BernObsModel
from obsmodel.GaussRegressYFromFixedXObsModel \
	import GaussRegressYFromFixedXObsModel
from obsmodel.GaussRegressYFromDiagGaussXObsModel \
	import GaussRegressYFromDiagGaussXObsModel

ObsModelConstructorsByName = {
    'DiagGauss': DiagGaussObsModel,
    'Gauss': GaussObsModel,
    'ZeroMeanGauss': ZeroMeanGaussObsModel,
    'AutoRegGauss': AutoRegGaussObsModel,
    'GaussRegressYFromFixedX': GaussRegressYFromFixedXObsModel,
    'GaussRegressYFromDiagGaussX': GaussRegressYFromDiagGaussXObsModel,
    'Mult': MultObsModel,
    'Bern': BernObsModel,
}

# Make constructor accessible by nickname and fullname
# Nickname = 'Gauss'
# Fullname = 'GaussObsModel'
#for val in ObsModelConstructorsByName.values():
#   fullname = str(val.__name__)
#   ObsModelConstructorsByName[fullname] = val

ObsModelNameSet = set(ObsModelConstructorsByName.keys())
