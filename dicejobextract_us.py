# import libraries
import urllib.request
from bs4 import BeautifulSoup
import time
import datetime
import sys
import csv
import requests
import argparse

'''
This program uses the python library BeautifulSoup
To install open command prompt enter: 

pip install beautifulsoup4
pip install lxml
pip install requests

To run in command prompt enter:
python dicejobextract_us.py

The initial search page is on line 80.  If changing, keep 
&p={}.format(i) on the end to allow script to navigate past page 1.

To run with debugging print lines:
python seekjobextract.py --verbose
'''


#Create a job class for holding the job information
class Job:
	def __init__(self, upsql, cntry, title, date_downloaded, date_posted, location, desc):
		self.upsql = upsql
		self.cntry = cntry
		self.title = title
		self.date_downloaded = date_downloaded
		self.date_posted = date_posted
		self.location = location
		self.desc = desc
		
jobs = []

#globals
date_downloaded = datetime.date.today()
cntry = 'US'
upsql = "No"
title = ''
date_posted = ''
location = ''
desc = ''

#Number of jobs to extract change this to get more jobs
num_jobs = 100
job_counter = 0

#Define the csv file name
FileName = time.strftime("%Y%m%d") + ' job_results_dice.csv'

#Debug function for testing
def debug_print(x = ''):
	if args.verbose:
		print(x)

parser = argparse.ArgumentParser(description='Skill scraper')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()	
	
with open(FileName, 'a+', newline='', encoding='utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
	
#loop over i amount of pages change this to go through more seek pages
for i in range(1, 20):
	if job_counter >= num_jobs:
		print('num_jobs limit reached, ending script')
		print('Page: {}'.format(i))
		break
		
	#print some new lines and the current page to separate from previous
	debug_print()
	debug_print('page {}'.format(i))
	debug_print()
	
	#loop over the pages to be scraped
	#change this link if you want a different seek page
	#quote_page = str(sys.argv)	
	quote_page = 'https://www.dice.com/jobs/advancedResult?q=%28forensic+OR+security+OR+project+OR+management&p={}'.format(i)
	
	#Ensure the page will not return a 404 or 410 error
	request = requests.get(quote_page)
	if request.status_code == 200:
		pass
	else:
		continue
	
	page = urllib.request.urlopen(quote_page)
	#debug_print(page.read())
	#sys.exit(0)


	soup = BeautifulSoup(page, 'html.parser')
	name_box = soup.find('article')
	
	
	#loop over the articles in the page
	for article in soup.find_all('div', class_='serp-result-content'):
		#exit after x successes
		#if len(jobs) >= num_jobs:
		if job_counter >= num_jobs:
			break
			
		debug_print('date downloaded: \n')
		debug_print(date_downloaded)
		debug_print()
		
		individual_page = []

		for url in article.find_all('a'):

			individual_page.append(url.get('href'))
		debug_print(individual_page[0])
		
		debug_print('https://www.dice.com{}'.format(individual_page[0]))
		individual_page_url = 'https://www.dice.com{}'.format(individual_page[0])
		
		#Ensure the page will not return a 404 or 410 error
		request = requests.get(individual_page_url)
		if request.status_code == 200:
			pass
		else:
			continue
		
		new_individual_page = urllib.request.urlopen(individual_page_url)
		new_soup = BeautifulSoup(new_individual_page, 'html.parser')
		new_name_box = soup.find('article')
		
		
		#Get the job description	
		debug_print('attempting desc')
		template_descriptions = new_soup.find('div', class_='highlight-black')
		if template_descriptions:
			debug_print('made it into desc')
			desc = template_descriptions.getText(separator=" ")			
			#Remove the leading whitespace
			desc = desc.lstrip()
			debug_print('Getting Description: \n')
			debug_print(desc)
			debug_print()
		
		
		#Get the title
		template_title = new_soup.find('h1', class_='jobTitle')
		if template_title:
			#title_tag = template_title.find('h1', {'class': 'jobTitle'})
			#if title_tag:
			#title = title_tag.text
			title = template_title.text
			debug_print('Getting Title: \n')
			debug_print(title)
		
		
		#Get the location
		template_location = new_soup.find('li', class_='location')
		if template_location:
			location_tag = template_location.find('span')
			if location_tag:
				location = location_tag.text
				debug_print('Getting Location: \n')
				debug_print(location)
				
			
		#Get the date posted
		template_date = new_soup.find('li', class_='posted hidden-xs')
		if template_date:		
			template_date = template_date.text			
			days_ago = template_date.split()
			
			debug_print(days_ago[0])
			debug_print(days_ago[1])
			debug_print(days_ago[2])

			if days_ago[2] == 'months':
				days_ago[1] = '30'
			
			if days_ago[2] == 'hours':
				days_ago[1] = '0'
			
			if days_ago[2] == 'save':
				days_ago[1] = '0'
				
			if days_ago[1] == 'moments':
				days_ago[1] = '0'
		
			#Convert days_ago to an actual date			
			date_posted = date_downloaded - datetime.timedelta(days=int(days_ago[1]))
			debug_print('printing date posted')
			debug_print(date_posted)
			debug_print()

		with open(FileName, 'a+', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow([upsql, cntry, title, date_downloaded, date_posted, location, desc])
		
		job_counter += 1
		#jobs.append(Job(upsql, cntry, title, date_downloaded, date_posted, location, desc))
		

'''
	file = open('filename.csv', 'a')
	file.write('{}, {}, {}, {}, {}\n'.format(title,date_downloaded,date_posted,location,desc))
'''		
	#sleep to look less like a bot
	#time.sleep(3)
		
'''
FileName = time.strftime("%Y%m%d") + ' job_results_dice.csv'
#FileName = 'job_results_seek_au.csv'
#FileName = 'job_results_seek.csv'
		
#Write the job class to csv
with open(FileName, 'a+', newline='', encoding='utf-8') as f:

	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
		
	for job in jobs:
	
		writer.writerow([job.upsql, job.cntry, job.title, job.date_downloaded, job.date_posted, job.location, job.desc])
'''
