from __future__ import absolute_import, division, print_function
import numpy as np
from NuRadioMC.utilities import units
import logging
logger = logging.getLogger("EvtGen.weight")

R_earth = 6357390 * units.m
DensityCRUST = 2900 * units.kg / units.m ** 3
AMU = 1.66e-27 * units.kg


def get_weight(theta_nu, pnu, mode='simple'):
    """
    calculates neutrino weight due to Earth absorption for different models

    Parameters
    ----------
    theta_nu: float or array of floats
        the zenith angle of the neutrino direction (where it came from, i.e., opposite to the direction of propagation)
    pnu: float or array of floats
        the momentum of the neutrino
    """
    if(mode == 'simple'):
        return get_simple_weight(theta_nu, pnu)
    else:
        logger.error('mode {} not supported'.format(mode))
        raise NotImplementedError


def get_simple_weight(theta_nu, pnu):
    """
    calculates neutrino weight due to Earth absorption, i.e. probability of the
    neutrino to reach the detector

    simple parametrization using only momentum and zenith angle information
    of the neutrino, adapted from ShelfMC

    Parameters
    ----------
    theta_nu: float or array of floats
        the zenith angle of the neutrino direction (where it came from, i.e., opposite to the direction of propagation)
    pnu: float or array of floats
        the momentum of the neutrino
    """
    if(theta_nu <= 0.5 * np.pi):  # coming from above
        return np.ones_like(theta_nu)
    else:  # coming from below
        sigma = (7.84e-40) * units.m2 * (pnu / units.GeV) ** 0.363
        d = - 2 * R_earth * np.cos(theta_nu)
        return np.exp(-d * sigma * DensityCRUST / AMU)