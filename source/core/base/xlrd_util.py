# coding: utf-8

import datetime
import xlrd

def cell_value(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        t = xlrd.xldate_as_tuple(cell.value, datemode)
        if t[3:] == (0, 0, 0):
            return datetime.date(t[0], t[1], t[2])
        return datetime.date(t[0], t[1], t[2], t[3], t[4], t[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:
        return cell.value == 1
    return cell.value    
