# dice.py
from random import randrange
# 1: 성공, 2: -1, 0: 유지, 3: 리셋


def enchnt(lvl):
    dc = randrange(1, 101)
    if lvl < 9:
        if dc <= (100-((lvl+1)*10)):
            return 1
        elif dc <= (90-(lvl*5)):
            return 2
        else:
            return 0
    elif lvl < 18:
        if dc <= 10:
            return 1
        elif dc <= 50:
            return 2
        elif dc <= (50+((lvl-8)*5)):
            return 3
        else:
            return 0
    elif lvl < 26:
        if dc <= 10:
            return 1
        elif dc <= (50-((lvl-18)*5)):
            return 2
        else:
            return 3
    elif lvl < 27:
        if dc <= 10:
            return 1
        else:
            return 3
    else:
        if dc <= 5:
            return 1
        else:
            return 3


def vsbt(lvl, botlvl):
    dcpl = randrange(1, 101)
    dcbt = randrange(1, 101)
    if (dcpl == 1 and dcbt == 1) or (dcpl == 100 and dcbt == 100):
        return 3, dcpl, dcbt
    elif dcpl == 1 or dcbt == 100:
        return 4, dcpl, dcbt
    elif dcpl == 100 or dcbt == 1:
        return 5, dcpl, dcbt
    elif (botlvl**2)+dcbt == (lvl**2)+dcpl:
        return 0, dcpl, dcbt
    elif (botlvl**2)+dcbt < (lvl**2)+dcpl:
        return 1, dcpl, dcbt
    else:
        return 2, dcpl, dcbt


def csno():
    return randrange(1, 1001)


def batdice(maxn):
    return randrange(1, maxn+1)


def dihyaku():
    return randrange(1, 101)
