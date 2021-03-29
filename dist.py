#!/usr/bin/python3.7
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

from random import randint

def roll(times, val, mod=0, flags=[]):
    results = []
    for _ in range(times):
        randval = randint(1, val) + mod if 'per-roll' in flags else randint(1, val)
        results.append(randval)
    if 'per-roll' in flags:
        mod = 0
    return sum(results) + mod

def dist(num, die, mod=0, per_roll=False, sim=False):
    if sim:
        flags = ['per-roll'] if per_roll else []
        rolls = [roll(num, die, mod=mod, flags=flags) for i in range(10**6)]
        rolls.sort()
        return rolls
    d = [i+mod for i in range(1, die+1)]
    for i in range(num-1):
        temp = []
        for j in d:
            for k in range(1, die+1):
                if per_roll:
                    k = k + mod
                temp.append(j+k)
        d = temp
    d.sort()
    return d

def dist2(num, die, mod=0, per_roll=False, sim=False):
    if sim:
        flags = ['per-roll'] if per_roll else []
        rolls = [roll(num, die, mod=mod, flags=flags) for i in range(10**6)]
        rolls.sort()
        return rolls
    d = [i+mod for i in range(1, die+1)]
    for i in range(num-1):
        temp = []
        for j in d:
            for k in range(1, die+1):
                if per_roll:
                    k = k + mod
                temp.append(j+k)
        d = temp
    d.sort()
    return d[1:]


def export_plot(num, die, path, mod=0, per_roll=False, title_flair=''):
    sim = die**num > 10**7
    x = np.array(dist2(num, die, mod=mod, per_roll=per_roll, sim=sim))
    plt.hist(x, x[-1] - x[0] +1, density=True, facecolor='r', alpha=0.75)

    if sim:
        mn, mx = plt.xlim()
        plt.xlim(mn, mx)
        kde_xs = np.linspace(mn, mx, 301)
        kde = st.gaussian_kde(x)
        plt.plot(kde_xs, kde.pdf(kde_xs), color='b', label='PDF')

    mean = (mod*num) + (num + num*die)/2 if per_roll else mod + (num + num*die)/2
    plt.axvline(mean, 0, 1, label=str(mean))
    plt.legend()
    plt.xlabel('Roll value')
    plt.ylabel('Probability')
    if title_flair == '':
        title_flair = f'{num}d{die}+{mod} --per-roll={per_roll}'
    plt.title(f'Distribution of {title_flair}')
    plt.grid(True)
    plt.savefig(path)
    plt.close()


if __name__ == '__main__':
    num, die, mod, per_roll = 4, 6, 0, False
    export_plot(num, die, 'plot.png', mod=mod, per_roll=per_roll)

