import numpy as np
from random import randrange

num = [1,2,3,4,5,6,7,8,9]
df_row = ['A','B','C','D','E','F','G','H','I']

def sudoku_create():
    ##기본 난수판 생성
    tb = [[0 for j in range(9)] for i in range(9)]
    tb[0] = num[:]
    np.random.shuffle(tb[0])
    for i in range(1, 9):
        for j in range(9):
            tb[i][j] = tb[0][(((i)%3)*3 + (i)//3 + j) % 9]
    ##난수판 셔플
    #행 섞기
    for x in range(20):
        ord = [0,1,2]
        for i in range(3):
            np.random.shuffle(ord)
            ord = list(ord)
            tmp = tb[ord[0]]
            for j in range(2):
                tb[ord[j]] = tb[ord[j+1]]
            tb[ord[2]] = tmp
            ord = np.add(ord,3)
        #열 섞기
        ord = [0,1,2]
        for i in range(3):
            np.random.shuffle(ord)
            ord = list(ord)
            for j in range(9):
                tmp = tb[j][ord[0]]
                for k in range(2):
                    tb[j][ord[k]] = tb[j][ord[k+1]]
                tb[j][ord[2]] = tmp
            ord = np.add(ord,3)
        #행 덩어리 섞기
        ord = [0, 3, 6]
        np.random.shuffle(ord)
        ord = list(ord)
        for i in range(3):
            tmp = tb[ord[0]+i]
            for j in range(2):
                tb[ord[j]+i] = tb[ord[j+1]+i]
            tb[ord[2]+i] = tmp  
        #열 덩어리 섞기
        ord = [0, 3, 6]
        np.random.shuffle(ord)
        ord = list(ord)
        for i in range(3):
            for j in range(9):
                tmp = tb[j][ord[0]+i]
                for k in range(2):
                    tb[j][ord[k]+i] = tb[j][ord[k+1]+i]
                tb[j][ord[2]+i] = tmp
        #가로세로조합 숫자 섞기
        for j in [0,3,6]:
            ord = list(np.random.choice(range(j, j+2+1), 2, replace = False))
            shf_idx = []
            shf_idx.append(randrange(0,2+1))
            First_N = tb[ord[0]][shf_idx[0]]
            k = 0
            while(tmp != First_N):
                tmp = tb[ord[1]][shf_idx[k]]
                shf_idx.append(tb[ord[0]].index(tmp))
                k += 1
                # if len(shf_idx)>9:
                #     raise
            shf_idx.pop()
            for k in shf_idx:
                tmp = tb[ord[0]][k]
                tb[ord[0]][k] = tb[ord[1]][k]
                tb[ord[1]][k] = tmp
        tb = list(map(list, zip(*tb)))
    return tb

def chk_sudoku(table):
    ## True 정답 False 오답
    #str 2 int 작업, 빈칸은 바로 오답처리
    for i in range(9):
        for j in range(9):
            if len(table[i][j])==3:
                table[i][j] = int(table[i][j][1])
            else:
                try:
                    table[i][j] = int(table[i][j])
                except:
                    return False
    #행 확인
    for i in range(9):
        for j in range(1, 9):
            if j not in table[i]:
                return False
    #열 확인
    for i in range(9):
        for j in range(1,9):
            if j not in np.array(table).T[i]:
                return False
    #덩어리 확인
    for x in range(0,9,3):
        for y in range(0,9,3):
            tmp = []
            for i in range(3):
                for j in range(3):
                    tmp.append(table[i+x][j+y])
            for i in range(1,9):
                if i not in tmp:
                    return False
    return True

def sudoku_make_problem(table, minN, maxN):
    table1 = table[:]
    delsum = 0
    for i in range(9):
    
        delnum = randrange(minN,maxN)
        dellist = list(np.random.choice(range(1, 9+1), delnum, replace = False))
        for j in dellist:
            table1[i][table[i].index(j)] = ' '
        delsum += delnum
    return table1, delsum

def sudoku_prt_str(table, prize, name):
    msg = f"```\nプレイヤー : {name}     賞金 : {prize}\n    1   2   3   4   5   6   7   8   9\n  +===+===+===+===+===+===+===+===+===+\n"
    for i in range(9):
        msg += f"{df_row[i]} |"
        for j in range(9):
            if len(table[i][j])==3:
                msg += f"{table[i][j]}"
            else:
                msg += f" {table[i][j]} "
            if (j+1)%3==0 and j != 8:
                msg += "|"
            elif j == 8:
                msg += "|\n"
            else:
                msg += ":"
        if (i+1)%3==0:
            msg += "  +===+===+===+===+===+===+===+===+===+\n"
        else:
            msg += "  +---+---+---+---+---+---+---+---+---+\n"
    msg += "```"
    return msg
    
def sudoku_ans_set(table, _row, _col, ans):
    if table[df_row.index(_row)][int(_col)-1] == ' ' or len(table[df_row.index(_row)][int(_col)-1]) == 3:
        if int(ans) != 0:
            table[df_row.index(_row)][int(_col)-1] = "'"+ans+"'"
        else:
            table[df_row.index(_row)][int(_col)-1] = ' '
        return table, False
    else:
        return table, True
    
    

# tb3 = sudoku_create()
# # #보드판 출력
# brd = '  '
# for l in range(9):
#     brd += str(num[l]) + ' '
# brd += '\n'
# for l in range(9):
#     brd += df_row[l] 
#     for k in range(9):
#         brd += ' ' + str(tb3[l][k])
#     brd += '\n'
# print(brd)

# if chk_sudoku(tb3):
#     print("ok")
