# user.py
import os
from openpyxl import load_workbook, Workbook
from math import ceil
from dice import csno
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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


# if os.path.isfile("userDB.xlsx"):

# else:
#     ws.cell(row=1, column=c_name, value="name")
#     ws.cell(row=1, column=c_id, value="id")
#     ws.cell(row=1, column=c_money, value="money")
#     ws.cell(row=1, column=c_lvl, value="lvl")
#     ws.cell(row=1, column=5, value=csno())
#     ws.cell(row=1, column=6, value=default_csn)
#     ws.cell(row=1, column=7, value=default_maz)
#     wb.save("userDB.xlsx")


def readxls():
    if not os.path.isfile("userDB.xlsx"):
        dataget()
    wb = load_workbook('userDB.xlsx')
    ws = wb.active
    return wb, ws


def dataget():
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'dice-mazin-4b8be2be76c1.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1X-7ek4MVuDNevUjnK_AU0ZMo5FgMfwQSNlw8jOApL9E/edit#gid=0'
    wbg = gc.open_by_url(spreadsheet_url)
    wsg = wbg.worksheet('user')
    range_list = wsg.range('A1:I50')
    wb = Workbook()
    ws = wb.active
    for cel in range_list:
        ws.cell(cel.row, cel.col, cel.value)
    wb.save("userDB.xlsx")
    wb.close()


def datasave():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'dice-mazin-4b8be2be76c1.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1X-7ek4MVuDNevUjnK_AU0ZMo5FgMfwQSNlw8jOApL9E/edit#gid=0'
    wbg = gc.open_by_url(spreadsheet_url)
    wsg = wbg.worksheet('user')
    cel = []
    cels =[]
    wb, ws = readxls()
    cell_range = ws['A1:I50']
    for idx in cell_range:
        for idy in idx:
            cel.append(idy.value)
        cels.append(cel)
        cel = []
    wsg.update('A1:I50', cels)
    wb.close()
    print('save complete')


def checkrow():
    wb, ws = readxls()
    for row in range(3, 50):
        if ws.cell(row, 1).value is None:
            wb.close()
            return row
    wb.close()


def signup(_name, _id):
    wb, ws = readxls()
    _row = checkrow()
    ws.cell(_row, c_name, _name)
    ws.cell(_row, c_id, str(hex(_id)))
    ws.cell(_row, c_money, str(default_money))
    ws.cell(_row, c_lvl, str(default_lvl))
    ws.cell(_row, c_macnt, str(default_cnt))
    ws.cell(_row, c_casnk, str(default_cascnt))
    ws.cell(_row, c_mazk, str(default_mazk))
    wb.save("userDB.xlsx")
    wb.close()


def findid(_id):
    wb, ws = readxls()
    for row in range(3, 50):
        if ws.cell(row, c_name).value is not None:
            if ws.cell(row, c_id).value == str(hex(_id)):
                wb.close()
                return row
        else:
            break
    wb.close()
    return None


def edtlvl(_row, _lvl):
    wb, ws = readxls()
    if ws.cell(_row, c_name).value is not None:
        ws.cell(_row, c_lvl, str(_lvl))
        wb.save("userDB.xlsx")
        wb.close()


def edtmny(_row, _money):
    wb, ws = readxls()
    if ws.cell(_row, c_name).value is not None:
        ws.cell(_row, c_money, str(_money))
        wb.save("userDB.xlsx")
        wb.close()


def rdinf(_row):
    wb, ws = readxls()
    if ws.cell(_row, c_name).value is not None:
        return int(ws.cell(_row, c_money).value), int(ws.cell(_row, c_lvl).value), int(ws.cell(_row, c_macnt).value), \
               int(ws.cell(_row, c_casnk).value)


def rstdat():
    wb, ws = readxls()
    for row in range(3, 50):
        if ws.cell(row, 1).value is not None:
            ws.cell(row, c_money, str(default_money))
            ws.cell(row, c_lvl, str(default_lvl))
            ws.cell(row, c_macnt, str(default_cnt))
            ws.cell(row, c_casnk, str(default_cascnt))
            ws.cell(row, c_mazk, str(default_mazk))
        else:
            break
    ws.cell(1, 2, str(csno()))
    ws.cell(1, 4, str(default_csn))
    ws.cell(1, 6, str(default_maz))
    wb.save("userDB.xlsx")
    wb.close()


def calbotlvl():
    wb, ws = readxls()
    _row = checkrow()
    botlvl = 0
    if _row > 3:
        for row in range(3, _row):
            botlvl += int(ws.cell(row, c_lvl).value)
        return ceil(botlvl/(_row-2))


def csnonum():
    wb, ws = readxls()
    return int(ws.cell(1, 2).value)


def csnokin():
    wb, ws = readxls()
    return int(ws.cell(1, 4).value)


def csnokined(mny):
    wb, ws = readxls()
    ws.cell(1, 4, str(mny))
    wb.save("userDB.xlsx")
    wb.close()


def csnorst():
    wb, ws = readxls()
    ws.cell(1, 2, str(csno()))
    csnokined(10000)
    wb.save("userDB.xlsx")
    wb.close()


def mazinkin():
    wb, ws = readxls()
    return int(ws.cell(1, 6).value)


def mazinkined(mny):
    wb, ws = readxls()
    ws.cell(1, 6, str(mny))
    wb.save("userDB.xlsx")
    wb.close()


def macnted(row, cnt):
    wb, ws = readxls()
    ws.cell(row, c_macnt, str(cnt))
    wb.save("userDB.xlsx")
    wb.close()


def mazinki(row):
    wb, ws = readxls()
    return int(ws.cell(row, c_mazk).value)


def mazinkied(_row, kig):
    wb, ws = readxls()
    ws.cell(_row, c_mazk, str(kig))
    wb.save("userDB.xlsx")
    wb.close()


def cascnt(row):
    wb, ws = readxls()
    cscnt = int(ws.cell(row, c_casnk).value)
    ws.cell(row, c_casnk, str(cscnt+1))
    wb.save("userDB.xlsx")
    wb.close()
    return int(cscnt)


def rank():
    wb, ws = readxls()
    userrank = {}
    usernum = checkrow()
    for row in range(3, usernum):
        if ws.cell(row, c_id).value != "0x9e8818f3342007b":
            uslvl = int(ws.cell(row, c_lvl).value)
            usname = ws.cell(row, c_name).value
            usmny = int(ws.cell(row, c_money).value)
            userrank[usname] = uslvl, usmny
    result = sorted(userrank.items(), reverse=True, key=lambda item: item[1])
    return result