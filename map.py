#!/usr/bin/python

import math

def update(priors, data): # returns posteriors
    # posterior = N(A, B)
    sample = normal.fromdata(data)
    return normal(
        (sample.var*priors.mu + priors.var*sample.mu)/(priors.var + sample.var), # A
        math.sqrt((priors.var * sample.var)/(priors.var + sample.var)) # B
        )

def iterate(priors, data):
    i = 0
    while True:
        i += 1
        ppriors = priors
        priors = update(priors, data)
        print(i, ': ', priors.mu, ', ', priors.sigma, sep='')
        #print(i, priors.mu, priors.sigma, sep='\t')
#        if abs((ppriors.mu-priors.mu) < 0.01: # converged
        if priors.sigma < 2: # high certainty
            return priors

class normal:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma
        self.var = sigma**2
    
    def fromdata(data):
        mean = sum(data)/len(data) # == expectation value of data
        variance = sum([(x - mean)**2 for x in data])/len(data)
        return normal(mean, math.sqrt(variance))

    # outputs the probability density at location x
    def density(x):
        return math.exp(-(x-mu)**2/(2*sigma**2))/(sigma*math.sqrt(2*math.pi))

    def logdensity(x):
        return log(density(x))

if __name__ == "__main__":
    import sys

    priors = normal(0, 10)
    data = []
    with open(sys.argv[1], 'r') as f:
        data = [float(x) for x in f]

    posteriors = iterate(priors, data)
