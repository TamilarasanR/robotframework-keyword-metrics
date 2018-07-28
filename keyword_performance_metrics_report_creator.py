from bs4 import BeautifulSoup
import datetime
import sys
import os
from bs4 import UnicodeDammit

soup = BeautifulSoup('''<html><head><title>Keywords Performace Metrics Report</title></head></html>''',"html.parser")

# Convert output.html to "Keywords Performance Analysis Report"
# Ref Table Style: https://www.w3schools.com/w3js/tryit.asp?filename=tryw3js_sort_table

# Create html tag
html = soup.new_tag('html')
soup.insert(0, html)

# Create meta tag
metatag = soup.new_tag('meta')
metatag.attrs["charset"] = "utf-8"
soup.head.append(metatag)

# Create script tag - responsive table
script = soup.new_tag('script')
script.attrs["src"] = "https://www.w3schools.com/lib/w3.js"
soup.head.append(script)

script_text = """$(document).ready(function(){$('#myTable').dataTable();});"""
script = soup.new_tag('script')
script.string = script_text
soup.head.append(script)

# Create link tag - responsive table
link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "https://www.w3schools.com/w3css/4/w3.css"
soup.head.append(link)

# Create link tag - responsive table sort icon
link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
soup.head.append(link)

body = soup.new_tag('body')
body["class"] = "w3-container"
soup.insert(0, body)

# Create header tag and title
h1 = soup.new_tag('h1',style="display: block;font-size: 2em;padding: 10px;")
h1.string = "Keywords Performace Metrics Report"
soup.insert(0, h1)

# Get report result - OS independent
current_path = os.getcwd()
# output.xml file location
text_file = os.path.join(os.path.curdir, 'output.xml')
# performance report result file location
result_file = os.path.join(os.path.curdir, 'keyword_performace_metrics_result.html')

# Create table tag
# <table id="myTable">
table = soup.new_tag('table',style="font-family: Consolas,\"courier new\;")
table["id"] = "myTable"
table["class"] = "w3-table-all"
body.insert(0, table)

# Create following tags for table
# <tr>
#   <th onclick="w3.sortHTML('#myTable', '.item', 'td:nth-child(1)')" style="cursor:pointer">Name</th>
#   <th onclick="w3.sortHTML('#myTable', '.item', 'td:nth-child(2)')" style="cursor:pointer">Country</th>
# </tr>
  
tr = soup.new_tag('tr')
table.insert(0, tr)

th = soup.new_tag('th')
th["onclick"] = "w3.sortHTML('#myTable', '.item', 'td:nth-child(1)')"
th["style"] = "cursor:pointer"
th.string = "Test Case Name"
tr.insert(0, th)

span = soup.new_tag('span')
span["class"] = "glyphicon glyphicon-sort"
th.insert(1, span)

th = soup.new_tag('th')
th["onclick"] = "w3.sortHTML('#myTable', '.item', 'td:nth-child(2)')"
th["style"] = "cursor:pointer"
th.string = "Keyword Name"
tr.insert(1, th)

span = soup.new_tag('span')
span["class"] = "glyphicon glyphicon-sort"
th.insert(1, span)

th = soup.new_tag('th')
th["onclick"] = "w3.sortHTML('#myTable', '.item', 'td:nth-child(3)')"
th["style"] = "cursor:pointer"
th.string = "Keyword Duration"
tr.insert(2, th)

span = soup.new_tag('span')
span["class"] = "glyphicon glyphicon-sort"
th.insert(1, span)

with open('output.xml') as raw_resuls:
    results = BeautifulSoup(raw_resuls, 'lxml')

# List for test cases
for tests in results.find_all("test"):    

    # List for keywords
    for keywords in tests.find_all("kw"):

        table_tr = soup.new_tag('tr')
        table_tr["class"] = "item"
        table.insert(1, table_tr)    

        table_td = soup.new_tag('td')
        table_td.string = tests['name']
        table_tr.insert(0, table_td)

        table_td = soup.new_tag('td')
        table_td.string = keywords['name']
        table_tr.insert(1, table_td)

        for status in keywords.find_all("status"):
            # Get duration took by keyword 
            start_date = datetime.datetime.strptime(status['starttime'], "%Y%m%d %H:%M:%S.%f")
            end_date = datetime.datetime.strptime(status['endtime'], "%Y%m%d %H:%M:%S.%f")
            duration = end_date - start_date

        table_td = soup.new_tag('td')
        table_td.string = str(duration)
        table_tr.insert(2, table_td)                          

    # keyword duration
    #print duration

# Write output as html file
with open(result_file, 'w') as outfile:
    outfile.write(soup.prettify())