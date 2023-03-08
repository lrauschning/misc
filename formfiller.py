#!/bin/python3

## small script to fill out some annoying forms

import sys
from fillpdf import fillpdfs
# using fillpdf, installable via pypi
# https://fillpdf.readthedocs.io/en/latest/

form = sys.argv[1] # path to empty form
outdir = sys.argv[2] # dir to write filled forms to

# assuming no leap years
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
year = 2023

# track days instead of dates, dates are annoying
# transforms a day into a date
def daytodate(day: int):
    month = 1
    while day > months[month-1]:
        day -= months[month-1]
        month += 1
    return f"{day}.{month}.{year}"

# main loop, generate filled forms
for weekstart in range(1, sum(months[:3]), 7): # customize to first monday worked
    data_dict = {'Beschaeftigter':'<NAME>', 'KalenderwocheVom':daytodate(weekstart), 'KalenderwocheBis':daytodate(weekstart+7), 'Datum1':daytodate(weekstart+7)}
    data_dict.update({f'Tag DayRow{day}':daytodate(weekstart + day) for day in range(1, 6)})
    data_dict.update({f'von fromRow{day}':'10:00' for day in range(1, 6)})
    data_dict.update({f'bis toRow{day}':'16:00' for day in range(1, 6)})
    data_dict.update({f'Stunden HoursRow{day}':'6:00' for day in range(1, 6)})

    fillpdfs.write_fillable_pdf(form, outdir + "/" + form.split('/')[-1].split(".pdf")[0] + "-" + daytodate(weekstart) + ".pdf", data_dict, flatten=False)



