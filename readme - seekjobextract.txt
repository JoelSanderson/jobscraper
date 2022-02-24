The seekjobextract python script uses the python library BeautifulSoup

To install open command prompt enter: 
pip install beautifulsoup4
pip install lxml

To run in command prompt enter:
python seekjobextract.py

To run with debugging print lines:
python seekjobextract.py --verbose

-----------------------------------------

To get more jobs in the output:
On line 44 change num_jobs to desired amount

On line 57 change the loop to go over more than the initial 1 page

-----------------------------------------

Reading the output:

There is an issue with excel not displaying a cell correctly if the data has a newline character.

Because the description column has multiple new lines in the data, when opening  the csv file in excel it appears blank.

Open the file in a text editor to display the job descriptions.