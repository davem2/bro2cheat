#!/usr/bin/env python
#
# Scrapes bro command examples from http://bropages.org/browse and reformats them for use with the bro-like tool cheat (http://github.com/chrisallenlane/cheat).
#

from bs4 import BeautifulSoup
import requests
import os
import argparse


# Defaults 
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser('~'), '.cheat_bro/')
DEFAULT_MIN_UPVOTES = 1;
DEFAULT_MAX_DOWNVOTES = 0;

# Parse command line
parser = argparse.ArgumentParser(description='Scrapes bro command examples from http://bropages.org/browse and reformats them for use with the bro-like tool cheat (http://github.com/chrisallenlane/cheat).')
parser.add_argument("-o", "--outpath", help="Directory to output cheat files (defaults to "+DEFAULT_OUTPUT_DIR+")", default=DEFAULT_OUTPUT_DIR)
parser.add_argument("-u", "--upvotes", type=int, help="Ignore entries with upvotes less than given value (defaults to "+str(DEFAULT_MIN_UPVOTES)+")", default=DEFAULT_MIN_UPVOTES)
parser.add_argument("-d", "--downvotes", type=int, help="Ignore entries with downvotes greater than given value (defaults to "+str(DEFAULT_MAX_DOWNVOTES)+")", default=DEFAULT_MAX_DOWNVOTES)
args = parser.parse_args()

# If output path does not exist, create it
if not os.path.exists(args.outpath):
    os.makedirs(args.outpath)

# Soupify http://bropages.org/browse
htmldata = requests.get('http://bropages.org/browse')
soup = BeautifulSoup(htmldata.text)

# Process each command entry
totalEntries = 0;
totalEntriesExtracted = 0;
commands = soup.find_all('td', class_='command')
for command in commands:
	totalEntries += 1
	upvotes = int(command.find_next("span", class_="upvote").get_text())
	downvotes = int(command.find_next("span", class_="downvote").get_text())
	
	if upvotes >= args.upvotes and downvotes <= args.downvotes: 
		totalEntriesExtracted += 1
		example = command.find_next("td", class_="msgbody").pre.string

		f = open(args.outpath + command.string, 'a')
		print(example+'\n', file=f)
		f.close();

#DEBUG
#		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
#		print(command.string + ' U:' + str(upvotes) + ' D:'+ str(downvotes))
#		print(example)
		
print("Saved " + str(totalEntriesExtracted) + " of " + str(totalEntries) + " bro command entries to " + args.outpath)
