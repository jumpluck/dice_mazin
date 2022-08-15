# user.py
import os
from openpyxl import load_workbook, Workbook
from math import ceil
from dice import csno

c_name = 1
c_id = 2
c_money = 3
c_lvl = 4
c_macnt = 5
c_casnk = 6
c_mazk = 7

default_money = 10000
default_lvl = 0
default_cnt = 3
default_csn = 10000
default_maz = 10000
default_mazk = 0
default_cascnt = 0

if os.path.isfile("userDB.xlsx"):
    wb = load_workbook("userDB.xlsx")
    ws = wb.active

else:
    wb = Workbook()
    ws = wb.active
    ws.cell(row=1, column=c_name, value="name")
    ws.cell(row=1, column=c_id, value="id")
    ws.cell(row=1, column=c_money, value="money")
    ws.cell(row=1, column=c_lvl, value="lvl")
    ws.cell(row=1, column=5, value=csno())
    ws.cell(row=1, column=6, value=default_csn)
    ws.cell(row=1, column=7, value=default_maz)
    wb.save("userDB.xlsx")


def checkrow():
    for row in range(2, 100):
        if ws.cell(row, 1).value is None:
            wb.close()
            return row
    wb.close()


def signup(_name, _id):
    _row = checkrow()
    ws.cell(row=_row, column=c_name, value=_name)
    ws.cell(row=_row, column=c_id, value=hex(_id))
    ws.cell(row=_row, column=c_money, value=default_money)
    ws.cell(row=_row, column=c_lvl, value=default_lvl)
    ws.cell(row=_row, column=c_macnt, value=default_cnt)
    ws.cell(row=_row, column=c_casnk, value=default_cascnt)
    ws.cell(row=_row, column=c_mazk, value=default_mazk)
    wb.save("userDB.xlsx")
    wb.close()


def findid(_id):
    for row in range(2, 100):
        if ws.cell(row, c_name).value is not None:
            if ws.cell(row, c_id).value == hex(_id):
                wb.close()
                return row
        else:
            break
    wb.close()
    return None


def edtlvl(_row, _lvl):
    if ws.cell(_row, c_name).value is not None:
        ws.cell(row=_row, column=c_lvl, value=_lvl)
        wb.save("userDB.xlsx")
        wb.close()


def edtmny(_row, _money):
    if ws.cell(_row, c_name).value is not None:
        ws.cell(row=_row, column=c_money, value=_money)
        wb.save("userDB.xlsx")
        wb.close()


def rdinf(_row):
    if ws.cell(_row, c_name).value is not None:
        return ws.cell(_row, c_money).value, ws.cell(_row, c_lvl).value, ws.cell(_row, c_macnt).value, \
               ws.cell(_row, c_casnk).value


def rstdat():
    for row in range(2, 100):
        if ws.cell(row, 1).value is not None:
            ws.cell(row=row, column=c_money, value=default_money)
            ws.cell(row=row, column=c_lvl, value=default_lvl)
            ws.cell(row=row, column=c_macnt, value=default_cnt)
            ws.cell(row=row, column=c_casnk, value=default_cascnt)
            ws.cell(row=row, column=c_mazk, value=default_mazk)
        else:
            break
    wb.save("userDB.xlsx")
    wb.close()


def calbotlvl():
    _row = checkrow()
    botlvl = 0
    if _row > 2:
        for row in range(2, _row):
            botlvl += ws.cell(row, c_lvl).value
        return ceil(botlvl/(_row-2))


def csnonum():
    return ws.cell(1, 5).value


def csnokin():
    return ws.cell(1, 6).value


def csnokined(mny):
    ws.cell(row=1, column=6, value=mny)
    wb.save("userDB.xlsx")
    wb.close()


def csnorst():
    ws.cell(row=1, column=5, value=csno())
    csnokined(10000)
    wb.save("userDB.xlsx")
    wb.close()


def mazinkin():
    return ws.cell(1, 7).value


def mazinkined(mny):
    ws.cell(row=1, column=7, value=mny)
    wb.save("userDB.xlsx")
    wb.close()


def macnted(row, cnt):
    ws.cell(row=row, column=c_macnt, value=cnt)
    wb.save("userDB.xlsx")
    wb.close()


def mazinki(row):
    return ws.cell(row, c_mazk).value


def mazinkied(_row, kig):
    ws.cell(row=_row, column=c_mazk, value=kig)
    wb.save("userDB.xlsx")
    wb.close()


def cascnt(row):
    cscnt = ws.cell(row, c_casnk).value
    ws.cell(row=row, column=c_casnk, value=cscnt+1)
    wb.save("userDB.xlsx")
    wb.close()
    return cscnt


def rank():
    userrank = {}
    usernum = checkrow()
    for row in range(2, usernum):
        if ws.cell(row, c_id).value != "0x9e8818f3342007b":
            uslvl = ws.cell(row, c_lvl).value
            usname = ws.cell(row, c_name).value
            usmny = ws.cell(row, c_money).value
            userrank[usname] = uslvl, usmny
    result = sorted(userrank.items(), reverse=True, key=lambda item: item[1])
    return result
