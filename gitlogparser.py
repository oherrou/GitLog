#!/usr/bin/env python

import sys
import re
import os

# Space constant for format printf
CHAR_MAX_AUTHOR 	= 25
CHAR_MAX_HASH		= 7
CHAR_MAX_DATE		= 10
CHAR_MAX_MESSAGE	= 120
FORMAT_AUTHOR  	= '{:.'+ '{}'.format(CHAR_MAX_AUTHOR) + '}'
FORMAT_HASH 	= '{:.' + '{}'.format(CHAR_MAX_HASH) + '}'
FORMAT_DATE 	= '{:.' + '{}'.format(CHAR_MAX_DATE) + '}'
FORMAT_MESSAGE 	= '{:.' + '{}'.format(CHAR_MAX_MESSAGE) + '}'


HTML_COLOR_AUTHOR 	= '#000000'
HTML_COLOR_HASH 	= '#8d0000'
HTML_COLOR_DATE 	= '#33a62c'
HTML_COLOR_MESSAGE	= '#1712af'
HTML_TAG_COLOR_AUTHOR 	= '<font color={}>'.format(HTML_COLOR_AUTHOR)
HTML_TAG_COLOR_HASH 	= '<font color={}>'.format(HTML_COLOR_HASH)
HTML_TAG_COLOR_DATE 	= '<font color={}>'.format(HTML_COLOR_DATE)
HTML_TAG_COLOR_MESSAGE 	= '<font color={}>'.format(HTML_COLOR_MESSAGE)
HTML_TAG_FONT_END		= '</font>'


def parseCommit(commitLines):
	# array to store dict of commit data
	dCommits = []
	# local dict to store commit data
	commit = {}
	# iterate lines and save
	for nextLine in commitLines:
		# ignore empty lines
		if nextLine == '' or nextLine == '\n':			
			pass

		# commit xxxx
		elif bool(re.match('commit', nextLine, re.IGNORECASE)):
			if len(commit) != 0:		## new commit, so re-initialize
				dCommits.append(commit)
				commit = {}
			commit = {'hash' : re.match('commit (.*)', nextLine, re.IGNORECASE).group(1) }

		# Merge: xxxx xxxx
		elif bool(re.match('merge:', nextLine, re.IGNORECASE)):
			pass

		# Author: xxxx <xxxx@xxxx.com>
		elif bool(re.match('author:', nextLine, re.IGNORECASE)):
			
			m = re.compile('Author: (.*) <(.*)>').match(nextLine)
			commit['author'] = m.group(1)
			commit['email'] = m.group(2)

		# Date: xxx
		elif bool(re.match('date:', nextLine, re.IGNORECASE)):
			commit['date'] = nextLine.strip()[8:]

		# (4 empty spaces)
		elif bool(re.match('    ', nextLine, re.IGNORECASE)):			
			if commit.get('message') is None:
				commit['message'] = nextLine.strip()

				# Parse specific tags
				if "[FIX]" in nextLine:
					commit['fix'] = nextLine.strip()
				elif "[FEA]" in nextLine:
					commit['fea'] = nextLine.strip()
				elif "[ADD]" in nextLine:
					commit['add'] = nextLine.strip()
				elif "[DOC]" in nextLine:
					commit['doc'] = nextLine.strip()
				elif "[WIP]" in nextLine:
					commit['wip'] = nextLine.strip()

			else:
				pass # just take the first line not the others

		#Unexpected lines
		else:
			pass# passprint ('ERROR: Unexpected Line: ' + nextLine)
	return dCommits

def WriteCommitToTxt(commitDict, txtFile):

	# Complete history
	txtFile.write("\n-------------------------------------------------------\n")
	txtFile.write("Complet Commit History")	
	txtFile.write("\n-------------------------------------------------------\n")
	for item in commitDict:
		szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
		szMessage 	= '{}'.format(FORMAT_MESSAGE).format(item['message'])
		szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
		szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

		line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
		txtFile.write(line)

	# [FIX] Commit
	txtFile.write("\n-------------------------------------------------------\n")
	txtFile.write("Commits by tags")	
	txtFile.write("\n-------------------------------------------------------\n")
	txtFile.write("\n\n[FIX] Commit\n")
	for item in commitDict:
		if 'fix' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['fix'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
			txtFile.write(line)

	# [FEA] Commit
	txtFile.write("\n\n[FEA] Commit\n")
	for item in commitDict:
		if 'fea' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['fea'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
			txtFile.write(line)

	# [ADD] Commit
	txtFile.write("\n\n[ADD] Commit\n")
	for item in commitDict:
		if 'add' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['add'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
			txtFile.write(line)

	# [DOC] Commit
	txtFile.write("\n\n[DOC] Commit\n")
	for item in commitDict:
		if 'doc' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['doc'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])
			
			line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
			txtFile.write(line)

	# [WIP] Commit
	txtFile.write("\n\n[WIP] Commit\n")
	for item in commitDict:
		if 'wip' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['wip'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			line 		= '* {} - {}  ({})  ({})\n'.format(szHash, szMessage, szDate, szAuthor)
			txtFile.write(line)


def WriteCommitToHtml(commitDict, htmlFile, giturl):

	# Complete history
	htmlFile.write("<h1 style=\"text-align:center\">Complete Commits History</h1>\n")
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> Complete Commits History </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
		szMessage 	= '{}'.format(FORMAT_MESSAGE).format(item['message'])
		szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
		szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

		htmlFile.write('<li>')
		szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
		szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
		szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
		szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
		szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
		htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
		htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	# [FIX] Commit
	htmlFile.write("<br><br><h1 style=\"text-align:center\">Sorted commits</h1>\n")		
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> [FIX] Commits </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		if 'fix' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['fix'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])
			
			htmlFile.write('<li>')
			szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
			szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
			szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
			szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
			szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
			htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
			htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	# [FEA] Commit
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> [FEA] Commits </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		if 'fea' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['fea'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			htmlFile.write('<li>')
			szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
			szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
			szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
			szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
			szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
			htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
			htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	# [ADD] Commit
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> [ADD] Commits </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		if 'add' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['add'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			htmlFile.write('<li>')
			szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
			szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
			szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
			szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
			szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
			htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
			htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	# [DOC] Commit
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> [DOC] Commits </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		if 'doc' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['doc'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			htmlFile.write('<li>')
			szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
			szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
			szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
			szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
			szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
			htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
			htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	# [WIP] Commit
	htmlFile.write("<hr>\n")
	htmlFile.write("<h2> [WIP] Commits </h2>\n")
	htmlFile.write("<ul>\n")
	for item in commitDict:
		if 'wip' in item:
			szHash 		= '{}'.format(FORMAT_HASH).format(item['hash'][:CHAR_MAX_HASH])
			szMessage	= '{}'.format(FORMAT_MESSAGE).format(item['wip'])
			szDate 		= '{}'.format(FORMAT_DATE).format(item['date'])
			szAuthor 	= '{}'.format(FORMAT_AUTHOR).format(item['author'])

			htmlFile.write('<li>')
			szHtmlLink = "<a href=\"{}{}\">".format(giturl,item['hash'])
			szHtmlHash 		= '{}'.format(HTML_TAG_COLOR_HASH)  + '{}'.format(szHtmlLink) + szHash  + '</a>{}'.format(HTML_TAG_FONT_END)
			szHtmlMessage	= '{}'.format(HTML_TAG_COLOR_MESSAGE) + szMessage + '{}'.format(HTML_TAG_FONT_END)
			szHtmlDate 		= '{}'.format(HTML_TAG_COLOR_DATE) + '(' + szDate  + ')' + '{}'.format(HTML_TAG_FONT_END)
			szHtmlAuthor 	= '{}'.format(HTML_TAG_COLOR_AUTHOR) + '(' + szAuthor + ')' + '{}'.format(HTML_TAG_FONT_END)
			htmlFile.write('<i>{}</i> - <b>{}</b> <i>{}</i> <i>{}</i>\n'.format(szHtmlHash, szHtmlMessage, szHtmlDate, szHtmlAuthor))
			htmlFile.write('</li>\n')
	htmlFile.write("</ul>\n")

	htmlFile.write("</body>\n</html>\n")




if __name__ == '__main__':

	parseCommit(sys.stdin.readlines())

	with open('testFile.html', 'w') as htmlFile:
		htmlFile.write("<!DOCTYPE html>\n<html>\n<body>\n")
		htmlFile.write("<body style=\"font-family:Courier New;background-color:powderblue\">\n")


		# List every commits with author name, hash, and commit message

		htmlFile.write("<h1 style=\"text-align:center\">All commits</h1>\n")
		ListFullCommit(dCommits)
		
		htmlFile.write("<br><br><h1 style=\"text-align:center\">Sorted commits</h1>\n")		
		# List [FIX] Commits
		ListFixCommit(dCommits)

		# List [FEA] Commits
		ListFeaCommit(dCommits)

		# List [ADD] Commits
		ListAddCommit(dCommits)

		# List [Doc] Commits
		ListDocCommit(dCommits)

		# List [WIP] Commits
		ListWipCommit(dCommits)

		htmlFile.write("</body>\n</html>\n")

		print("\n\n\n HTML report generated")
