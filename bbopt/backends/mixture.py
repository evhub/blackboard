#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x4564f16f

# Compiled with Coconut version 1.4.0-post_dev7 [Ernest Scribbler]

"""
The mixture backend. Lets you specify a distribution over different possible algorithms.
"""

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_addpattern, _coconut_sentinel
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------



import random

from bbopt.registry import alg_registry
from bbopt.registry import init_backend


class MixtureBackend(_coconut.object):
    """Mixture backend. Takes in a distribution over different possible algorithms
    of the form [(algorithm, weight)]."""

    def __init__(self, examples, params, distribution):
        total_weight = sum((weight for alg, weight in distribution))

# generate cutoff points
        cum_probs = []
        prev_cutoff = 0
        for alg, weight in distribution:
            cutoff = prev_cutoff + weight / total_weight
            cum_probs.append((alg, cutoff))
            prev_cutoff = cutoff

# randomly select algorithm
        rand_val = random.random()
        self.selected_alg = None
        for alg, cutoff in cum_probs:
            if rand_val <= cutoff:
                self.selected_alg = alg
                break

# initialize backend
        self.selected_backend, kwargs = alg_registry[self.selected_alg]
        self.backend = init_backend(self.selected_backend, examples, params, **kwargs)

    def param(self, name, **kwargs):
        return self.backend.param(name, **kwargs)