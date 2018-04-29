#!/usr/bin/env python
#version 3.x
import sys
import re
import os
import argparse
import configparser
from gitlogparser import parseCommit, WriteCommitToTxt, WriteCommitToHtml
from subprocess import Popen, PIPE
import datetime

# From ini files
Project_Number = ''
Project_Name = ''
Project_Url = ''
Git_Url = ''
Release_Author = ''
Git_LogCommand = ''

# From Arguments parser
bCreateTxtFile = False
bCreateHtmlFile = False
# array to store dict of commit data
dCommits = []

def getArgument():
	global Project_Number
	global Project_Name
	global Project_Url
	global Git_Url
	global Release_Author
	global Git_LogCommand
	global bCreateTxtFile
	global bCreateHtmlFile

	parser = argparse.ArgumentParser()
	config = configparser.ConfigParser()

	parser.add_argument('-config', action='store', required=True, help='Config file')
	parser.add_argument('--createTxt', action='store_true', help='This option will create a txt file report')
	parser.add_argument('--createHtml', action='store_true', help='This option will create a html file report')

	# Parsed arguments
	parsed = parser.parse_args()
	bCreateTxtFile = parsed.createTxt
	bCreateHtmlFile = parsed.createHtml

	# Ini file
	config.read(parsed.config)

	Project_Number 	= config.get('Project','Project_Number')
	Project_Name 	= config.get('Project','Project_Name')
	Project_Url 	= config.get('Project','Project_Url')
	Git_Url 		= config.get('Project','Git_Url')
	Release_Author	= config.get('Project','Release_Author')
	Git_LogCommand	= config.get('Project','Git_LogCommand')


if __name__ == '__main__':

	getArgument()
	# Open a temporary files to retrieve the output of the git log commands
	with open('tmp.txt', 'w') as outputFile:
		with Popen(Git_LogCommand,stdout=PIPE) as p:
			output, errors = p.communicate()
			line = output.decode('utf-8')
			outputFile.write(line)

	# Read this files and send the lines to the commit parser
	with open('tmp.txt', 'r') as outputFile:
		dCommits = parseCommit(outputFile.readlines())

	# Delete the temporary file
	os.remove('tmp.txt')

	# Common parameters		
	date 	= datetime.datetime.now()

	strDate = "{:<15}: {:.90}\n".format("Date", date.strftime("%Y-%m-%d %H:%M"))
	strProjectNum = "{:<15}: {:.90}\n".format("Project Number", Project_Number)
	strProjectName = "{:<15}: {:.90}\n".format("Project Name", Project_Name)
	strProjectUrl = "{:<15}: {:.90}\n".format("Project URL", Project_Url)
	strGitUrl = "{:<15}: {:.90}\n".format("Git URL", Git_Url)
	strReleaseAuthor = "{:<15}: {:.90}\n".format("Release Author", Release_Author)

	# Create txt file
	if bCreateTxtFile == True:
		with open('Commits.txt','w') as txtFile:
			txtFile.write(strDate)
			txtFile.write(strProjectNum)
			txtFile.write(strProjectName)
			txtFile.write(strProjectUrl)
			txtFile.write(strGitUrl)
			txtFile.write(strReleaseAuthor)
			WriteCommitToTxt(dCommits, txtFile)

	# Create hmtl file if txt file exist or is given as parameter
	if( bCreateTxtFile == True) and (bCreateHtmlFile == True):
		with open('Commits.html','w') as htmlFile:

			htmlFile.write("<!DOCTYPE html>\n<html>\n<body>\n")
			htmlFile.write("<body style=\"font-family:Courier New;background-color:powderblue\">\n")
			htmlFile.write("<p>{}</p>".format(strDate))
			htmlFile.write("<p>{}</p>".format(strProjectNum))
			htmlFile.write("<p>{}</p>".format(strProjectName))
			htmlFile.write("<p>{}</p>".format(strProjectUrl))
			htmlFile.write("<p>{}</p>".format(strGitUrl))
			htmlFile.write("<p>{}</p>".format(strReleaseAuthor))

			WriteCommitToHtml(dCommits, htmlFile, Git_Url)
	