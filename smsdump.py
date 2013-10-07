#!/usr/bin/env python
from __future__ import print_function
import time, sqlite3, sys, os, pprint
from datetime import datetime
from optparse import OptionParser


def main():
	"""Read in an apple backup file as a SQL database, and save all messages in the database
	to text files, naming them after the reciever."""

	parser = OptionParser()
	parser.add_option("-d", "--db", dest="dbfile", help="SMS DB File [default: %default]")

	#Default name of the sms database file from the iTunes backup
	parser.set_defaults(dbfile="3d0d7e5fb2ce288813306e4d4636395e047a3d28.mddata")

	(options, args) = parser.parse_args()

	if not os.path.exists(options.dbfile):
		print("Error: file " + options.dbfile + " does not exist or cannot be found.")
		print("Please check the file name and try again.")
		print("See -h for help and all options.")
		sys.exit(2)

	print("Opening: " + options.dbfile)
	conn = sqlite3.connect(options.dbfile)
	
	msgs = ""
	with conn:
		#Get dict
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()

		#Query to get all records
		all_query = "SELECT * FROM message"

		#Get all messages
		try:
			cur.execute(all_query)
			msgs = cur.fetchall()
			
		except sqlite3.OperationalError, e:
			print("Error: Something is wrong or unexpected in the sms database file.")
			print("Are you sure this is a valid, unencrypted iPhone SMS sqlite database?")
			print("See -h for help and all options.")
			sys.exit(2)
	
	print(str(len(msgs)) + " message(s)")
	print("")
	
	for row in msgs:
		print(".", end="")
		if (row["address"] != None) and (row["text"] != None):
			#Open a text file with the reciever number without space and plus
			with open(trans_addr(row["address"]) + '.txt', 'a') as f:
				dir = ""
				if row["flags"] == 2:
					dir = "From: "
				if row["flags"] == 3:
					dir = "To: "
				
				f.write(dir + row["address"] + " ")
				f.write(str(datetime.fromtimestamp(row["date"])) + "\n\n")
				f.write(row["text"].encode('utf-8'))
				f.write("\n\n")
				
	
	print("")
	print("Done.")
	# Exit normally
	sys.exit()
	
def trans_addr(addr):
	"""This function takes an address and returns only alphanumeric charecters for use as a filename."""
	ret = ""
	for ch in addr:
		if ch.isalnum():
			ret += ch
			
	return(ret) 

if __name__ == "__main__":
	main()