import random as rd
import math


def exponentielle(lam):
    t = rd.random()
    return (-math.log(1-t)/lam)


def simule_N(lam,t):
    N = 0
    T = 0
    while T <= t:
        N += 1
        T += exponentielle(lam)
    return N


def simule_delta(lam,s):
    T1 = 0
    T2 = exponentielle(lam)
    while T2 < s:
        T1 = T2
        T2 += exponentielle(lam)
    delta = T2 - T1
    return delta