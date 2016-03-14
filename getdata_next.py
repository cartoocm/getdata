#!/usr/bin/python
###########################
## --------------------- ##
#        getdata.py        #
# 
# creation date: 13.03.2016
# Last modified: 
#
## --------------------- ##
###########################
import os
import sys
import glob
from ftplib import FTP
import argparse
########################################################
parser = argparse.ArgumentParser(prog="getdata.py", description="getdata.py is a script that download the GPS RINEX files.\n" \
                                      " author: Giorgio Savastano - giorgio.savastano@uniroma1.it")

parser.add_argument("-nav", type=str, nargs=2, default=0, dest="navFiles", help="This argument determines the year and the day of the " \
									  "nav files that will be downloaded. The argument refers to the year and the doy (e.g. -nav 2015 260). ")

parser.add_argument("-stat", type=str, nargs='*', default='all', dest="listStat", help="This argument determines for which stations the "\
									  "nav files will be downloaded. By default will be downloaded the nav files for all the stations "\
									  " that are in the obs directory")

parser.add_argument("-igs", type=str, nargs=4, default=0, dest="igsFiles", help="This argument determines the igs and brdc files that will be downloaded." \
									  " The argument refers to the gps_week, day_of_week, year and doy (e.g. -igs 1712 0 2012 302 ). ")

########################################################
## PROGRAM STARTS ##
args = parser.parse_args()
print args 
path = os.getcwd()

if args.navFiles != 0:
	ftp = FTP('data-out.unavco.org')
	ftp.login()	
	year = args.navFiles[0]
	doy = args.navFiles[1]

	if args.listStat == 'all':
		os.chdir('obs')
		lista = glob.glob('*.??o')
		lista.sort()
		os.chdir('..')
	else:
		lista = [l + doy + "0." + year[2:4] + "o" for l in args.listStat]

	print year, doy, lista, os.getcwd()
	try:
		os.mkdir('rawdata/nav/'+year)
	except OSError: pass
	try:
		os.mkdir('rawdata/nav/'+year+'/'+doy)
	except OSError: pass

	# Setup first file
	for s in xrange( len(lista) ):
		# Download and unpack files
		try:
		    
			file1 = lista[s][:-1]  + 'n.Z'
			
			filepath1 = 'rawdata/nav/'+year+'/'+doy+'/'+file1 
			f1 = open(filepath1,'wb')
			filename1 = '/pub/rinex/nav/'+year+'/'+doy+'/'+file1
			# Get first file
			print('Retrieving: '+file1)
			ftp.retrbinary("RETR " + filename1,f1.write)
			f1.close()
			cmd = 'gunzip -f '+filepath1
			print(cmd)
			os.system(cmd)
			file1 = lista[s][:-1]  + 'n'
			filepath1 = 'rawdata/nav/'+year+'/'+doy+'/'+file1

		except Exception, e:
			print e
			f1.close()
			os.remove(filepath1)
			continue

	print 'Closing FTP conection...'	
	ftp.close()

if args.igsFiles != 0:

	ftp = FTP('cddis.gsfc.nasa.gov')
	ftp.login()	

	# Parse input
	gps_week = args.igsFiles[0] 
	day_of_week = args.igsFiles[1]
	year = args.igsFiles[2]
	doy = args.igsFiles[3]
	doy = doy[0:3]
	
	# Download and unpack files
	try:
		# Setup first file
		file1 = 'igs'+gps_week+day_of_week+'.sp3.Z'
		os.mkdir('rawdata/sp3/'+year)
		filepath1 = 'rawdata/sp3/'+year+'/'+file1 
		f1 = open(filepath1,'wb')
		filename1 = '/pub/gps/products/'+gps_week+'/'+file1
		# Setup second file
		file2 = 'brdc'+doy+'0.'+year[2:4]+'n.Z'
		os.mkdir('rawdata/brdc/'+year)
		filepath2 = 'rawdata/brdc/'+year+'/'+file2
		f2 = open(filepath2,'wb')
		filename2 = '/pub/gps/data/daily/'+year+'/'+doy+'/'+year[2:4]+'n/'+file2
		
		# Get first file
		print('Retrieving: '+file1)
		ftp.retrbinary("RETR " + filename1,f1.write)
		f1.close()
		cmd = 'gunzip -f '+filepath1
		print(cmd)
		os.system(cmd)
		file1 = 'igs'+gps_week+day_of_week+'.sp3'
		filepath1 = 'rawdata/sp3/'+year+'/'+file1
		# Get second file
		print('Retrieving: '+file2)
		ftp.retrbinary("RETR " + filename2,f2.write)
		f2.close()
		cmd = 'gunzip -f '+filepath2
		print(cmd)
		os.system(cmd)
		file2 = 'brdc'+doy+'0.'+year[2:4]+'n'
		filepath2 = 'rawdata/brdc/'+year+'/'+file2
	except Exception, e:
		print e
		f1.close()
		f2.close()
		os.remove(filepath1)
		os.remove(filepath2)
		
	
print 'Closing FTP conection...'	
ftp.close()
