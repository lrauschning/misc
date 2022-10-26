#!/bin/python3

#TODO put this on github somewhere, send around link

import numpy as np
import math
import itertools
from scipy.spatial import ConvexHull
from tqdm import tqdm
import matplotlib.pyplot as plt

TRAIN_RES = 30


def l1_norm(V):
    return np.sum(np.abs(V))

def l2_norm(V):
    return np.sqrt(np.sum(np.square(V)))

def gen_lpnorm(p):
    return lambda V: np.power(np.sum(np.power(V, p)), 1/p)

def linf_norm(V):
    return np.max(np.abs(V))

# norms can be combined by any linear transform
l2_max_norm = lambda V: 2*l2_norm(V) + linf_norm(V)
weird_norm = lambda V: l2_max_norm(V) + np.power(np.power(l1_norm(V), 3) + np.power(linf_norm(V), 3), 1/3)

# implementing support for arbitrary norm approximation using convex hulls as described in
# https://math.stackexchange.com/questions/2663321/examples-of-norms-essentially-different-from-p-norms

#eps = np.finfo(np.float32).eps
eps = 0.01

# from https://stackoverflow.com/a/69485899
def contains(hull, x):
    A, b = hull.equations[:, :-1], hull.equations[:, -1:]
    return np.all(x @ A.T + b.T < eps, axis=1)
 
EXP = 2
# generate a hull-based norm function
def gen_hull_norm(hull, nsteps = 20):
    def hull_norm(V):
        # perform an exponential search for the initial interval
        inf, sup = 0, 1
        for _ in range(nsteps):
            if contains(hull, sup*V):
                break
            inf = sup
            sup = sup*EXP

        # now assume the value to be between inf and sup and do binary search
        for _ in range(nsteps):
            mid = (inf + sup)/2
            if contains(hull, mid*V): # value <= mid
                sup = mid
            else:
                inf = mid
        return (inf + sup)/2 # return middle of the interval to avoid systematic bias

    return hull_norm

# generates a hull norm from the convex hull of a symmetrized, optionally centered set of points
def from_points(points, center=False):
    if center: # centers the points first, optional
        points = points - np.mean(points, axis=0)
    # make symmetric
    points = np.concatenate((points, -points))
    hull = ConvexHull(points)
    return gen_hull_norm(hull)

# small class to define a linear model, cleaner than tuple
class lm:
    def __init__(self, m, t):
        self.m = m
        self.t = t

    def predict(self, X):
        return (self.m*X) + self.t

    def train(X, Y, norm=l2_norm, rngs=[np.linspace(-3, 3, num=TRAIN_RES), np.linspace(-3, 3, num=TRAIN_RES)]):
        loss, params = find_min(fn=lambda x: eval(lm(*x), X, Y, norm=norm), *rngs)
        print("model loss:", loss)
        return lm(params[0], params[1])

    def __repr__(self):
        return f"lm(m: {self.m}, t: {self.t})"

# compute the loss of a model
def eval(model, X, Y, norm=l2_norm):
    return norm(Y - model.predict(X))

# small function to brute force the maximum value of a function with arguments in certain bounds
def find_min(*rngs, fn=None):
    argsmin = np.zeros(len(rngs))
    minval = math.inf

    print("brute-forcing minimum, progress:")
    for X in tqdm(map(np.array, itertools.product(*rngs))):
        val = fn(X)
        if fn(X) < minval:
            minval = val
            argsmin = X

    return minval, argsmin


if __name__ == '__main__':
    # init a test dataset to perform regression on, hide a real effect in Y_eff, just use noise in Y_cnt
    vals = 8
    rng = np.random.default_rng()
    X = np.arange(vals) + rng.standard_normal(vals)
    X = X/2
    m = rng.uniform(low=0, high=3)/2
    t = rng.uniform(low=0, high=3)/2
    print(f"real m: {m}, t: {t}")
    Y_eff = m*X + t + rng.standard_normal(vals)
    Y_cnt = rng.standard_normal(vals)
    Y_het = m*X + t + np.sqrt(m*X)*rng.standard_normal(vals)
    print(Y_het)
    # TODO also generade Y_sin with heteroskedastidicity
    figeff, axeff = plt.subplots()
    axeff.plot(X, Y_eff, '.')
    figcnt, axcnt = plt.subplots()
    axcnt.plot(X, Y_cnt, '.')
    fighet, axhet = plt.subplots()
    axhet.plot(X, Y_het, '.')

    border = np.array([np.min(X)-5, np.max(X)+5])

    def eval_model(norm, label):
        model_eff = lm.train(X, Y_eff, norm=norm)
        axeff.plot(border, model_eff.predict(border), linewidth=4, label=label)
        model_cnt = lm.train(X, Y_cnt, norm=norm)
        axcnt.plot(border, model_cnt.predict(border), linewidth=4, label=label)
        model_het = lm.train(X, Y_het, norm=norm)
        axhet.plot(border, model_het.predict(border), linewidth=4, label=label)
        print(label, "eff:", model_eff, "\trand:", model_cnt, "\thetero:", model_het)

    norms = [l2_norm, gen_lpnorm(5), linf_norm, weird_norm]
    norms.append(from_points(rng.random((int(1.2*vals), vals)), center=True))
    normlabels = ['l2', 'l5', 'linf', 'composite', 'random']
    print("INFO: Evaling now")
    for norm, label in zip(norms, normlabels):
        eval_model(norm, label)

    plt.show()

    #print("X:", X)
    #print("Ŷ:", model.predict(X))
    #print("Y:", Y)


## code graveyard
#class plane:
#    def __init__(self, norm, shift):
#        self.norm = norm
#        self.shift = shift
#
#    def isin(self, x):
#        return np.scalarproduct(self.norm, np.subtract(x, self.shift)) <= 0 # oder so
#
## TODO find a way to generate convex hull of a set of points
#def make_polytope(*planes):
#    return lambda x: all([plane.isin(x) for plane in planes])
#
