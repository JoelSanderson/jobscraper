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
python pnetjobextract_sa.py

To run with debugging print lines:
python pnetjobextract_sa.py --verbose
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
cntry = 'SA'
upsql = "No"
title = ''
date_posted = ''
location = ''
desc = ''

#Number of jobs to extract change this to get more jobs
num_jobs = 100
job_counter = 0

#Define the csv file name
FileName = time.strftime("%Y%m%d") + ' job_results_PNet.csv'

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

#loop over i amount of pages change this to go through more Pnet pages
	#Note: Pages on Pnet go up in 25s
	#Page 2 ends link with =25
	#Page 3 ends link with =50
	#Add 25 to i each iteration instead of looping through each number
for i in range(0, 200, 25):
	if job_counter >= num_jobs:
		print('num_jobs limit reached, ending script')
		print('Page: {}'.format(i))
		break
		
	#print some new lines and the current page to separate from previous
	debug_print()
	debug_print('page {}'.format(i))
	debug_print()
	

	#quote_page = str(sys.argv)
	
	#loop over the pages to be scraped
	#change this link if you want a different Pnet page
	#Note: If changing search page url, {}.format(i) must be appended to the end to allow searching past page 1
	quote_page = 'https://www.pnet.co.za/5/job-search-detailed.html?ke=computer%20security%20forensics&of={}'.format(i)
	
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
	name_box = soup.find('h2')
	
	
	#loop over the articles in the page
	for article in soup.find_all('div', class_='job-element__body word-wrap'):		
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
		individual_page_url = (individual_page[0])
		
		#Ensure the page will not return a 404 or 410 error
		request = requests.get(individual_page_url)
		if request.status_code == 200:
			pass
		else:
			continue
		
		
		new_individual_page = urllib.request.urlopen(individual_page_url)
		new_soup = BeautifulSoup(new_individual_page, 'html.parser')
		new_name_box = soup.find('article')
		
		#Get the job title
		template_title = new_soup.find('title')
		if template_title:
			item_title = template_title.text
			title_split = item_title.split('- ')
			debug_print('Getting title: \n')
			#debug_print(title[0])	
			debug_print()
			title = title_split[0];
			debug_print(title)
			
		
		#Get the job location
		template_location = new_soup.find('li', class_='listing-list at-listing__list-icons_location')
		if template_location:
			debug_print('Attempting location')
			location = template_location.text
			location = location.splitlines()
			location = location[2]
			debug_print(location)
			debug_print()

				
		#Get the job description		
		template_descriptions = new_soup.find('div', class_='listingContent')
		if template_descriptions:
			desc = template_descriptions.getText(separator=" ")
			debug_print()
			debug_print('Getting Description: \n')
			debug_print(desc)
			debug_print()

			
		#Get the date posted
		template_date = new_soup.find(class_='date-time-ago')
		if template_date:
			#date_posted = template_date[0].text
			#location = template_date_location[1].text
			
			#Turn template_date into a writable string and strip off unwanted data
			date_posted = str(template_date)
			date_posted = date_posted.split()
			
			date_posted = date_posted[2]
			date_posted = date_posted.split('"')

			date_posted = date_posted[1]	
			
			#split off the time posted from date
			date_posted = date_posted.split("T")
			
			debug_print(date_posted[0])
			debug_print(date_posted[1])
			
			#split the year/month/day format and rewrite as day/month/year
			date_posted = date_posted[0].split("-")
			date_posted = date_posted[2]+'/'+date_posted[1]+'/'+date_posted[0]

			debug_print('printing date_posted')
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
FileName = time.strftime("%Y%m%d") + ' job_results_PNet.csv'
#FileName = 'job_results_pnet_au.csv'
#FileName = 'job_results_pnet.csv'
		
#Write the job class to csv
with open(FileName, 'a+', newline='', encoding='utf-8') as f:

	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
		
	for job in jobs:
		debug_print(job.title)
		debug_print(job.location)
		debug_print(date_posted)
		debug_print(date_posted)


		writer.writerow([job.upsql, job.cntry, job.title, job.date_downloaded, job.date_posted, job.location, job.desc])

'''