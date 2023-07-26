import numpy as np
import itertools as it

from numpy.random import default_rng
from numpy.linalg import inv
from numpy.linalg import norm
from scipy.linalg import sqrtm


def er_dag(p, d=0.5, ad=None, rng=default_rng()):
    '''
    Randomly generates an Erdos-Renyi (lower triangular)
    direct acyclic graph given an ordering.

    p = |variables|
    d = |edges| / |possible edges|
    ad = average degree
    rng = random number generator
    '''

    # npe = |possible edges|
    npe = int(p * (p - 1) / 2)

    # ne = |edges|
    if ad is not None: d = ad / (p - 1)
    ne = int(d * npe)

    # generate edges
    e = np.append(np.zeros(npe - ne, np.uint8), np.ones(ne, np.uint8))
    rng.shuffle(e)

    # generate graph
    g = np.zeros([p, p], np.uint8)
    g.T[np.triu_indices(p, 1)] = e

    return g


def sf_rewire(g, rng=default_rng()):
    '''
    Rewire within rows so row sum (in degree) doesnt change.

    g = directed acyclic graph
    rng = random number generator
    '''

    # p = |variables|
    p = g.shape[0]

    for i in range(1, p):
        J = [[j] for j in range(i)]
        J += [[j] * int(np.sum(g[:i, j])) for j in range(i)]
        J = list(it.chain.from_iterable(J))
        rng.shuffle(J)

        in_deg = np.sum(g[i,:])
        g[i,:] = np.zeros(p)

        for j in J:
            if in_deg == 0: break
            if g[i,j] == 0:
                in_deg -= 1
                g[i,j] = 1


def cov(g, b=1, s=1, rng=default_rng()):
    '''
    Randomly generates a covariance matrix given a directed acyclic graph.

    g = directed acyclic graph
    b = bound for beta parameter
    s = bound for sigma parameter
    rng = random number generator
    '''

    # p = |variables|
    p = g.shape[0]

    # e = |edges|
    e = np.sum(g)

    # generate variance terms
    E = rng.uniform(1, s, p)
    O = np.diag(E)

    # generate edge weights
    B = np.zeros([p, p])
    B[np.where(g == 1)] = rng.uniform(0, b, e)
    # B[np.where(g == 1)] = rng.uniform(-b, b, e)

    # calculate covariance
    IB = inv(np.eye(p) - B)
    S = IB @ O @ IB.T

    return S, B, E


def corr(g, a=0, rng=default_rng()):
    '''
    Randomly generates a correlation matrix R ~ |R|^a given a direct acyclic graph.

    g = (lower triangluar) directed acyclic graph
    rng = random number generator
    '''

    # p = |variables|
    p = g.shape[0]

    # assert that g is lower triangular
    assert all([g[i,j] == 0 for j in range(p) for i in range(j)])

    # initialize correlation / coeffcient / error matrices
    R = np.eye(p)
    B = np.zeros([p, p])
    E = np.ones(p)

    # initialize beta parameter
    b = a + p / 2

    # update correlation / coeffcient / error matrices
    if g[1,0] > 0:
        r = 2 * rng.beta(b, b) - 1
        R[1, 0] = r
        R[0, 1] = r
        B[1, 0] = r
        E[1] -= r**2

    for i in range(2, p):

        # updated beta parameter
        b -= 0.5

        # initialize coefficients
        w = np.zeros(i)

        # k = |parents|
        k = np.sum(g[i, :])

        # update coefficients
        if k > 0:
            r = np.sqrt(rng.beta(k / 2, b))
            E[i] -= r**2
            w += g[i, :i] * rng.standard_normal(i)
            w *= r / norm(w)

        # update correlation / coeffcient matrices
        A = sqrtm(R[:i, :i]).real
        z = np.dot(A, w)
        R[i, :i] = z
        R[:i, i] = z
        B[i, :i] = g[i, :i] * np.dot(inv(A.T), w)

    return R, B, E


def simulate(B, E, n, err=None, rng=default_rng()):
    '''
    Randomly simulates data.

    B = (lower triangluar) beta matrix
    E = error matrix
    n = sample size
    err = additive error distribution
    rng = random number generator
    '''

    # p = |variables|
    p = B.shape[0]

    # assert that g is lower triangular
    assert all([B[i,j] == 0 for j in range(p) for i in range(j)])

    # set default additive error as normal
    if err is None: err = lambda *x: rng.normal(0, *x)

    # simulate data
    X = np.zeros([n, p])
    for i in range(p):
        # parents
        J = np.where(B[i,:] != 0)[0]

        # linear effect
        for j in J: X[:,i] += B[i,j] * X[:,j]

        # additive error
        X[:,i] += err(E[i], n)

        # standardize
        X[:,i] = (X[:,i] - np.mean(X[:,i])) / np.std(X[:,i])

    return X


def randomize(g, X, rng=default_rng()):
    '''
    Randomly permutes the graph and data.

    g = directed acyclic graph
    X = data
    rng = random number generator
    '''

    # p = |variables|
    p = g.shape[0]

    # random permutation
    pi = [i for i in range(p)]
    rng.shuffle(pi)

    return g[pi].T[pi].T, X[:,pi]
