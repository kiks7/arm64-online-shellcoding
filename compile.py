#!/usr/bin/python
import requests
import urllib
from bs4 import BeautifulSoup
import sys
sys.path.append('./imports')
from logger import *
import argparse
proxs = {'http':'http://127.0.0.1:8080'}

def main(filename):
	# Read ASM from file
	print_info('Starting ')
	try:
		with open(filename) as f:
    			lines = f.readlines()
	except Exception as lol:
		print_error('Error opening your file :/')
		sys.exit()
	# Parse lines into a single string
	final_asm = ''
	for line in lines:
		final_asm += line

	# ALL NEEDED 
	raw = """<xjxobj><e><k>txtInput</k><v>S<![CDATA[Input your ARM Instruction(s) here. [Shift] + [Enter] for new lines.
	 CMP R0, R2
	 MOV R0, R7
	 NOP
	 BX LR]]></v></e><e><k>txtInput_64</k><v>S<![CDATA[
	{0}
	]]></v></e><e><k>txtInput_kt</k><v>S<![CDATA[mov ]]></v></e><e><k>txtInput2_kt</k><v>S</v></e><e><k>opt_arch</k><v>S1</v></e></xjxobj>""".format(final_asm)
	
	postData = {
		'xjxfun':'ajxRun4Command',
		'xjxr': '', # try EMPTY 
		'xjxargs[]': raw
	}

	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 77.77; rv:66.0)',
	}
	
	resp = requests.post('http://armconverter.com/index.php',headers=headers,data=postData)
	if 'No such file' in resp.text:
		print_error('Check your syntax ..... :/')
	#PARSE THE RESPONSE
	else:
		# may gOOd response :)		
		parsed_html = BeautifulSoup(resp.text,'lxml')

		# PARSE THE OBJDUMP OUTPUT
		try:
			objDump = parsed_html.body.find('cmd', attrs={'id':'txtRaw1'}).text.replace('S','').decode('utf-8')
		except Exception as lel:
			print_error('Error parsing response')
			print lol
			sys.exit()
		print '=' * 20 + ' OBJDUMP' + '=' * 20
		print objDump 
		print '=' * 20 + ' OBJDUMP' + '=' * 20
		# PARSE THE SHELLCODE
		try:
			retHex = parsed_html.body.find('cmd', attrs={'id':'txtTitle2_64'}).text.replace('S','').decode('utf-8').replace('\x0d','').replace('\x0a','')
		except Exception as lel:
			print_error('Error parsing response .. may be also empty')
			print lel
			sys.exit()
		shellcode = '\\x'+'\\x'.join(retHex[i:i+2] for i in range(0, len(retHex), 2))			
		print '=' * 20 + ' SHELLCODE' + '=' * 20
		print shellcode
		print '=' * 20 + 'SHELLCODE' + '=' * 20

		print '=' * 20 + ' RAW' + '=' * 20
		print retHex
		print '=' * 20 + ' RAW' + '=' * 20
		n = 8 
		dividedHex =  [retHex[i:i+n] for i in range(0, len(retHex), n)]

		print '=' * 20 + ' PYTHON' + '=' * 20
		print 'shellcode = \'\''
		for bytecode in dividedHex:
			formatted = '\\x'+'\\x'.join(bytecode[i:i+2] for i in range(0, len(bytecode), 2))
			print 'shellcode += \''+formatted+'\''
		print '=' * 20 + ' PYTHON' + '=' * 20
		print_ok('Done!')	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f','--file',required=True,help='File with asm')
	args = vars(parser.parse_args())
	main(args['file'])
