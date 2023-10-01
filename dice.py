# dice.py
from random import randrange, choices
# 1: 성공, 2: -1, 0: 유지, 3: 리셋

def roll(ko, men):
    result = [0 for i in range(ko)]
    for i in range(ko):
        result[i] = randrange(1, men+1)
    return result

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
    elif (botlvl)+dcbt == (lvl)+dcpl:
        return 0, dcpl, dcbt
    elif (botlvl)+dcbt < (lvl)+dcpl:
        return 1, dcpl, dcbt
    else:
        return 2, dcpl, dcbt

def setdeck():
    arr = [0 for i in range(3)]
    for i in range(5):
        arr[randrange(3)] += 1
    return arr

def calwin(player,mazin):
    win = [0 for i in range(3)]
    if (player[0] == 0 and player[1] == 0 and mazin[1] > 0):
        m_p = 1
    elif (player[0] == 0 and player[2] == 0 and mazin[0] > 0):
        m_p = 0
    elif (player[1] == 0 and player[2] == 0 and mazin[2] > 0):
        m_p = 2
    elif player[0] == 0 and player[1] > 0 and player[2] > 0 and mazin[0] > 0:
        if mazin[1] > 0:
            ans = choices([0,1],[1+player[1]*0.2,1+player[2]*0.5])
            m_p = ans[0]
        elif mazin[2] > 0:
            ans = choices([0,2],[1+player[1]*0.5,1+player[2]*0.1])
            m_p = ans[0]
        else:
            m_p = 0
    elif player[2] == 0 and player[1] > 0 and player[0] > 0  and mazin[2] > 0:
        if mazin[0] > 0:
            ans = choices([2,0],[1+player[0]*0.2,1+player[1]*0.5])
            m_p = ans[0]
        elif mazin[1] > 0:
            ans = choices([2,1],[1+player[0]*0.5,1+player[1]*0.1])
            m_p = ans[0]
        else:
            m_p = 2     
    elif player[1] == 0 and player[0] > 0 and player[2] > 0  and mazin[1] > 0:
        if mazin[2] > 0:
            ans = choices([1,2],[1+player[2]*0.2,1+player[0]*0.5])
            m_p = ans[0]
        elif mazin[0] > 0:
            ans = choices([1,0],[1+player[2]*0.5,1+player[0]*0.1])
            m_p = ans[0]
        else:
            m_p = 1        
    elif (mazin[0] == 0 and player[1] > 0 and mazin[1] > 0):
        if player[0] > 0 and mazin[2] > 0:
            ans = choices([1,2],[2,1])
            m_p = ans[0]
        else:
            m_p = 1
    elif (mazin[2] == 0 and player[0] > 0 and mazin[0] > 0):
        if player[2] > 0 and mazin[1] > 0:
            ans = choices([0,1],[2,1])
            m_p = ans[0]
        else:
            m_p = 0        
    elif (mazin[1] == 0 and player[2] > 0 and mazin[2] > 0):
        if player[1] > 0 and mazin[0] > 0:
            ans = choices([2,0],[2,1])
            m_p = ans[0]
        else:
            m_p = 2                  
    else:
        for i in range(3):
            if mazin[i] > 0:
                win[i] = max(player[(i+1)%3]-player[(i+2)%3],player[i]*0.5-player[(i+2)%3],0)
            else:
                win[i] = 0
        if sum(win) == 0:
            for i in range(3):
                if mazin[i] > 0:
                    win[i] = max(player[i]-player[(i+2)%3]*0.5,0)
                else:
                    win[i] = 0
        if sum(win) == 0:
            win = mazin
        # print(win)
        ans = choices([0,1,2],win)
        m_p = ans[0]
        if player[(m_p+2)%3] > 0:
            n = choices([0,1,2,3,4],[10,10,5,2,1])
            for i in range(n[0]):
                if mazin[(m_p+1)%3] > 0:
                    m_p_r = choices([m_p,(m_p+1)%3],[0.6, 0.4])
                elif mazin[(m_p+2)%3] > 0:
                    m_p_r = choices([m_p,(m_p+2)%3],[0.7, 0.3])
                else:
                    m_p_r = [m_p]
                m_p = m_p_r[0]
    return m_p

def csno():
    return randrange(1, 1001)


def batdice(maxn):
    return randrange(1, maxn+1)


def dihyaku():
    return randrange(1, 101)


def trmpset():
    trump = []
    mark = ['◇', '♤', '♡', '♧']
    for m in mark:
        for n in range(1, 13):
            trump.append([m, n])
    return trump


def bacrst(pcs, bcs):
    if sum(pcs) % 10 == sum(bcs) % 10:
        result = 't'
    elif sum(pcs) % 10 < sum(bcs) % 10:
        result = 'b'
    else:
        result = 'p'
    return result


def bac():
    trump = trmpset()
    pc = []
    pcs = []
    bc = []
    bcs = []
    pick = []
    for x in range(1, 5):
        idx = randrange(0, len(trump))
        pick.append(trump.pop(idx))
    pc.append(pick[0])
    pc.append(pick[3])
    bc.append(pick[1])
    bc.append(pick[2])
    for card in pc:
        if card[1] >= 10:
            pcs.append(0)
        else:
            pcs.append(card[1])
    for card in bc:
        if card[1] >= 10:
            bcs.append(0)
        else:
            bcs.append(card[1])
    if sum(pcs) % 10 >= 8 or sum(bcs) % 10 >= 8:
        result = bacrst(pcs, bcs)
    elif sum(pcs) % 10 >= 6:
        if sum(bcs) % 10 >= 6:
            result = bacrst(pcs, bcs)
        else:
            idx = randrange(0, len(trump))
            bc.append(trump.pop(idx))
            if bc[2][1] >= 10:
                bcs.append(0)
            else:
                bcs.append(bc[2][1])
            result = bacrst(pcs, bcs)
    else:
        idx = randrange(0, len(trump))
        pc.append(trump.pop(idx))
        if pc[2][1] >= 10:
            pcs.append(0)
        else:
            pcs.append(pc[2][1])
        if 6 >= sum(bcs) % 10 >= 3:
            mn = 8-((7-(sum(bcs) % 10))*2)
            if 7 >= pcs[2] >= mn or (sum(bcs) % 10 == 3 and pcs[2] == 9):
                idx = randrange(0, len(trump))
                bc.append(trump.pop(idx))
                if bc[2][1] >= 10:
                    bcs.append(0)
                else:
                    bcs.append(bc[2][1])
        if sum(bcs) % 10 <= 2:
            idx = randrange(0, len(trump))
            bc.append(trump.pop(idx))
            if bc[2][1] >= 10:
                bcs.append(0)
            else:
                bcs.append(bc[2][1])
        result = bacrst(pcs, bcs)
    pce = sum(pcs) % 10
    bce = sum(bcs) % 10
    for idx in range(0, len(pc)):
        if pc[idx][1] == 11:
            pc[idx][1] = 'J'
        elif pc[idx][1] == 12:
            pc[idx][1] = 'Q'
        elif pc[idx][1] == 13:
            pc[idx][1] = 'K'
    for idx in range(0, len(bc)):
        if bc[idx][1] == 11:
            bc[idx][1] = 'J'
        elif bc[idx][1] == 12:
            bc[idx][1] = 'Q'
        elif bc[idx][1] == 13:
            bc[idx][1] = 'K'
    return pc, bc, result, pce, bce
