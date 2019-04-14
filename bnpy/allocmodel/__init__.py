from allocmodel.AllocModel import AllocModel

from allocmodel.mix.FiniteMixtureModel import FiniteMixtureModel
from allocmodel.mix.DPMixtureModel import DPMixtureModel
from allocmodel.mix.DPMixtureRestrictedLocalStep import make_xPiVec_and_emptyPi

from allocmodel.topics.FiniteTopicModel import FiniteTopicModel
from allocmodel.topics.HDPTopicModel import HDPTopicModel

from allocmodel.hmm.FiniteHMM import FiniteHMM
from allocmodel.hmm.HDPHMM import HDPHMM

from allocmodel.relational.FiniteSMSB import FiniteSMSB
from allocmodel.relational.FiniteMMSB import FiniteMMSB
from allocmodel.relational.FiniteAssortativeMMSB import FiniteAssortativeMMSB
from allocmodel.relational.HDPMMSB import HDPMMSB
from allocmodel.relational.HDPAssortativeMMSB import HDPAssortativeMMSB


AllocModelConstructorsByName = {
    'FiniteMixtureModel': FiniteMixtureModel,
    'DPMixtureModel': DPMixtureModel,
    'FiniteTopicModel': FiniteTopicModel,
    'HDPTopicModel': HDPTopicModel,
    'FiniteHMM': FiniteHMM,
    'HDPHMM': HDPHMM,
    'FiniteSMSB': FiniteSMSB,
    'FiniteMMSB': FiniteMMSB,
    'FiniteAssortativeMMSB': FiniteAssortativeMMSB,
    'HDPMMSB': HDPMMSB,
    'HDPAssortativeMMSB': HDPAssortativeMMSB,
}

AllocModelNameSet = set(AllocModelConstructorsByName.keys())

__all__ = ['AllocModel']
for name in AllocModelConstructorsByName:
    __all__.append(name)
