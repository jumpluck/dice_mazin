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
    ##난수판 셔플
    #행 섞기
    for x in range(2):
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
        for i in [0,3,6]:
            ord = []
            ord.append(list(np.random.choice(range(i, i+2+1), 2, replace = False)))
            ord.append([i*3 - ord[0][0] - ord[0][1] + 3, ord[0][randrange(2)]])
            for j in range(2):
                for x in range(4):
                    shf_idx = []
                    shf_idx.append(randrange(0,2+1))
                    First_N = tb[ord[j][0]][shf_idx[0]]
                    k = 0
                    while(tmp != First_N):
                        tmp = tb[ord[j][1]][shf_idx[k]]
                        shf_idx.append(tb[ord[j][0]].index(tmp))
                        k += 1
                    shf_idx.pop()
                    for k in shf_idx:
                        tmp = tb[ord[j][0]][k]
                        tb[ord[j][0]][k] = tb[ord[j][1]][k]
                        tb[ord[j][1]][k] = tmp
                    tb = list(map(list, zip(*tb)))
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
    for i in range((_row//3)*3,(_row//3)*3+3):
        for j in range((_col//3)*3,(_col//3)*3+3):
            rec_data.append(table[i][j])
    return rec_data

def get_rec_cord(_row,_col):
    cord = []
    for i in range((_row//3)*3,(_row//3)*3+3):
        for j in range((_col//3)*3,(_col//3)*3+3):
            cord.append([i,j])
    return cord
  
def cel_set(table, cel):
    if table[cel[0]][cel[1]] == ' ':
        table[cel[0]][cel[1]] = []
    row_chk = get_row(table,cel[0])
    col_chk = get_col(table,cel[1])
    rec_chk = get_rec(table,cel[0],cel[1])
    for i in range(1,10):
        if type(table[cel[0]][cel[1]]) == list:
            if i not in row_chk and i not in col_chk and i not in rec_chk:
                if i not in  table[cel[0]][cel[1]]:
                    table[cel[0]][cel[1]].append(i)
                    return True
    return False

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
        cel_clr(table, cel, num)
        return True
    row_chk = get_row(table,cel[0])
    col_chk = get_col(table,cel[1])
    rec_chk = get_rec(table,cel[0],cel[1])
    for i in table[cel[0]][cel[1]]:
        if list_chk(row_chk, i) == 1 or list_chk(col_chk, i) == 1 or list_chk(rec_chk, i) == 1:
            table[cel[0]][cel[1]] = i
            cel_clr(table, cel, i)
            return True
    return False

def cel_clr_row(table, cel, num):
    row_chk = get_row(table,cel[0])
    for i in range(len(row_chk)):
        if type(row_chk[i]) == list:
            if num in row_chk[i]:
                table[cel[0]][i].remove(num)

def cel_clr_col(table, cel, num):
    col_chk = get_col(table,cel[1])
    for i in range(len(col_chk)):
        if type(col_chk[i]) == list:
            if num in col_chk[i]:
                table[i][cel[1]].remove(num)

def cel_clr_rec(table, cel, num):
    rec_chk = get_rec(table,cel[0],cel[1])
    rec_cord = get_rec_cord(cel[0],cel[1])
    for i in range(len(rec_chk)):
        if type(rec_chk[i]) == list:
            if num in rec_chk[i]:
                table[rec_cord[i][0]][rec_cord[i][1]].remove(num)

def cel_clr(table, cel, num):
    cel_clr_row(table, cel, num)
    cel_clr_col(table, cel, num)
    cel_clr_rec(table, cel, num)

def cel_chk_roof(chk_list, del_cord):
    setting = True
    while(setting):
        setting = False
        for delc in del_cord:
            if type(chk_list[delc[0]][delc[1]]) == list:
                val = cel_chk(chk_list, delc)
                # test_list_str = saveload(chk_list)
                # list_str = sudoku_prt_str(test_list_str)
                # print(list_str)
                setting = setting or val

def ans_chk(chk_list):
    for i in range(9):
        for j in range(9):
            if type(chk_list[i][j]) == list:
                return True
    return False

"""def two_way(ori_cel, delc, cel_chk_list, chk_list):
    for i in range(len(cel_chk_list)):
        if type(cel_chk_list[i]) == list:
            if ((ori_cel == cel_chk_list[i]) or (ori_cel == cel_chk_list[i][::-1])) and (delc[1] != i):
                cel_way=[]
                for j in range(2):
                    tmp_list = copy.deepcopy(chk_list)
                    tmp_list[delc[0]][delc[1]] = ori_cel[j]
                    cel_clr(tmp_list, delc, ori_cel[j])
                    cel_chk_roof(tmp_list, del_cord)
                    cel_way.append(ans_chk(tmp_list))
                if (cel_way[0] != cel_way[1]) and (cel_way[0] or cel_way[1]):
                    if cel_way[0]:
                        chk_list[delc[0]][delc[1]] = ori_cel[0]
                        cel_clr(chk_list, delc, ori_cel[0])
                    else:
                        chk_list[delc[0]][delc[1]] = ori_cel[1]
                        cel_clr(chk_list, delc, ori_cel[1])
                    return True
    return False 
"""

def make_problem(test_list, mxn):
    cordinate = [[i,j] for i in range(9) for j in range(9)]
    del_cord = []
    np.random.shuffle(cordinate)
    while(len(cordinate)>0 and len(del_cord)<mxn):
        chk_list = copy.deepcopy(test_list)
        del_cord.append(cordinate.pop())
        for delc in del_cord:
            chk_list[delc[0]][delc[1]] = ' '
            
        setting = True
        while(setting):
            setting = False
            for delc in del_cord:
                val = cel_set(chk_list, delc)
                setting = setting or val
                
        cel_chk_roof(chk_list, del_cord)

        """setting = True
        while(setting):
            setting = False       
            for delc in del_cord:
                ori_cel = chk_list[delc[0]][delc[1]]
                if type(ori_cel) == list:
                    if len(ori_cel) == 2:
                        row_chk = get_row(chk_list,delc[0])
                        val = two_way(ori_cel, delc, row_chk, chk_list)
                        setting = setting or val
                        col_chk = get_col(chk_list,delc[1])
                        val = two_way(ori_cel, delc, col_chk, chk_list)
                        setting = setting or val
                        rec_chk = get_rec(chk_list,delc[0],delc[1])
                        val = two_way(ori_cel, delc, rec_chk, chk_list)
                        setting = setting or val
            cel_chk_roof(chk_list, del_cord)           
        """          
        
        if ans_chk(chk_list):
            del_cord.pop()
            
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
