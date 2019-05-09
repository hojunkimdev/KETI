#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 11:18:33 2018

@author: root
"""

import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import numpy as np
import skcuda.linalg as linalg
import skcuda.misc as misc

linalg.init()
a = np.asarray(np.random.rand(4,2), np.float32)
b = np.asarray(np.random.rand(2,2), np.ffloat32)
a_gpu = gpuarray.to_gpu(a)
b_gpu = gpuarray.to_gpu(b)
c_gpu = linalg.dot(a_gpu,b_gpu)
np.allclose(np.dot(a,b), c_gpu.get())
