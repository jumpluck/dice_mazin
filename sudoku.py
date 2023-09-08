import numpy as np
from random import randrange
import copy

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
    ##난수판 셔플 각 20회
    for x in range(2):
        #행 섞기
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

def get_row(table,_row):
    return table[_row]

def get_col(table,_col):
    col_data = []
    for i in range(9):
        col_data.append(table[i][_col])
    return col_data

def get_rec(table,_row,_col):
    rec_data = []
    cord = []
    for i in range((_row//3)*3,(_row//3)*3+3):
        for j in range((_col//3)*3,(_col//3)*3+3):
            rec_data.append(table[i][j])
            cord.append([i,j])
    return rec_data, cord
  
def cel_set(table, cel):
    if table[cel[0]][cel[1]] == ' ':
        table[cel[0]][cel[1]] = []
    row_chk = get_row(table,cel[0])
    col_chk = get_col(table,cel[1])
    rec_chk, rec_cord = get_rec(table,cel[0],cel[1])
    for i in range(1,10):
        if type(table[cel[0]][cel[1]]) == list:
            if i not in row_chk and i not in col_chk and i not in rec_chk:
                if i not in  table[cel[0]][cel[1]]:
                    table[cel[0]][cel[1]].append(i)
                    return True , table
    return False, table

def list_chk(lists, num):
    cnt = 0
    for x in lists:
        if type(x) == list:
            if num in x:
                cnt += 1
    return cnt

def cel_chk(table, cel):
    if len(table[cel[0]][cel[1]]) == 1:
        num = table[cel[0]][cel[1]][0]
        table[cel[0]][cel[1]] = num
        table = cel_clr_row(table, cel, num)
        table = cel_clr_col(table, cel, num)
        table = cel_clr_rec(table, cel, num)
        return True, table
    row_chk = get_row(table,cel[0])
    col_chk = get_col(table,cel[1])
    rec_chk, rec_cord = get_rec(table,cel[0],cel[1])
    for i in table[cel[0]][cel[1]]:
        if list_chk(row_chk, i) == 1 or list_chk(col_chk, i) == 1 or list_chk(rec_chk, i) == 1:
            table[cel[0]][cel[1]] = i
            table = cel_clr_row(table, cel, i)
            table = cel_clr_col(table, cel, i)
            table = cel_clr_rec(table, cel, i)
            return True, table
    return False, table

def cel_clr_row(table, cel, num):
    row_chk = get_row(table,cel[0])
    for i in range(len(row_chk)):
        if type(row_chk[i]) == list:
            if num in row_chk[i]:
                table[cel[0]][i].remove(num)
    return table

def cel_clr_col(table, cel, num):
    col_chk = get_col(table,cel[1])
    for i in range(len(col_chk)):
        if type(col_chk[i]) == list:
            if num in col_chk[i]:
                table[i][cel[1]].remove(num)
    return table

def cel_clr_rec(table, cel, num):
    rec_chk, rec_cord = get_rec(table,cel[0],cel[1])
    for i in range(len(rec_chk)):
        if type(rec_chk[i]) == list:
            if num in rec_chk[i]:
                table[rec_cord[i][0]][rec_cord[i][1]].remove(num)  
    return table

def sudoku_make_problem(test_list, mxn):
    cordinate = [[i,j] for i in range(9) for j in range(9)]
    del_cord = []
    np.random.shuffle(cordinate)
    while(len(cordinate)>0 and len(del_cord)<mxn):
        chk_list = copy.deepcopy(test_list)
        del_cord.append(cordinate.pop())
        # print('pop', del_cord[::-1])
        for delc in del_cord:
            chk_list[delc[0]][delc[1]] = ' '
        setting = True
        while(setting):
            setting = False
            for delc in del_cord:
                val, chk_list = cel_set(chk_list, delc)
                setting = setting or val

        setting = True
        while(setting):
            setting = False
            for delc in del_cord:
                if type(chk_list[delc[0]][delc[1]]) == list:
                    val, chk_list = cel_chk(chk_list, delc)
                    setting = setting or val
        it_fail = False
        for i in range(9):
            for j in range(9):
                if type(chk_list[i][j]) == list:
                    # print('old', del_cord[::-1])
                    # test_list_str1 = saveload(chk_list)
                    # list_str1 = sudoku_prt_str(test_list_str1)
                    # print(list_str1)
                    del_cord.pop()
                    # print('new', del_cord[::-1])
                    it_fail = True
                    break
            if it_fail:
                break
        # if not it_fail:
        #     ans_list = copy.deepcopy(chk_list)
    pro_list = copy.deepcopy(test_list)
    for dc in del_cord:
        pro_list[dc[0]][dc[1]] = ' '
    deln = len(del_cord)
    return pro_list, deln

    

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
