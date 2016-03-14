# Getdata
Download GPS RINEX files.

To download the nav files, write the year, doy and the name of the stations:

## LINUX

$ ./getdata_next.py -nav 2015 260 -stat ahup ainp

## OS

$ python getdata_next.py -nav 2015 260 -stat ahup ainp

To download the igs and brdc files, write the gps_week, day_of_week, year and doy

## LINUX

$ ./python getdata_next.py -igs 1712 0 2012 302

## OS

$ python getdata_next.py -igs 1712 0 2012 302

