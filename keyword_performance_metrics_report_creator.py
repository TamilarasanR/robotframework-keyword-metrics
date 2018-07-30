from bs4 import BeautifulSoup
import datetime
import sys
import os

# Ignores following library keywords in metrics report
ignore_library = [
    'BuiltIn',
    'SeleniumLibrary',
    'String',
    'Collections',
    'DateTime',
    ]

soup = BeautifulSoup('''<html><head><title>Keywords Performance Metrics Report</title></head></html>''',"html.parser")

# Convert output.html to "Keywords Performance Analysis Report"
# Ref Table Style: https://datatables.net/examples/styling/bootstrap

# Create meta tag
metatag = soup.new_tag('meta')
metatag.attrs["charset"] = "utf-8"
soup.head.append(metatag)

# Create link tag - responsive table
link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
link.attrs["type"] = "text/css"
soup.head.append(link)

link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap.min.css"
link.attrs["type"] = "text/css"
soup.head.append(link)

#JQuery
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "https://code.jquery.com/jquery-3.3.1.js"
soup.head.append(script)

# Create script tag - Data Table Js
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"
soup.head.append(script)

script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js"
soup.head.append(script)

# datatable script js
script_text = """ $(document).ready(function() {
    $('#example').DataTable();
} );"""
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.string = script_text
soup.head.append(script)

body = soup.new_tag('body',style="font-family: Consolas,\"courier new\";padding: 10px;")
soup.insert(1, body)

# Create header tag and title
h1 = soup.new_tag('h1',style="font-size: 2em;font-weight:bold")
h1.string = "Keywords Performance Metrics Report"
body.insert(0, h1)

br = soup.new_tag('br')
body.insert(1,br)

# Get report result - OS independent
current_path = os.getcwd()
# output.xml file location
text_file = os.path.join(os.path.curdir, 'output.xml')
# performance report result file location
result_file = os.path.join(os.path.curdir, 'keyword_performance_metrics_result.html')

# Create table tag
# <table id="myTable">
table = soup.new_tag('table',style="padding: 5px;font-size: 13px;")
table["id"] = "example"
table["class"] = "table table-striped table-bordered"
body.insert(2, table)

thead = soup.new_tag('thead')
table.insert(0, thead)

tr = soup.new_tag('tr')
thead.insert(0, tr)

th = soup.new_tag('th')
th.string = "Test Case"
tr.insert(0, th)

th = soup.new_tag('th')
th.string = "Keyword"
tr.insert(1, th)

th = soup.new_tag('th')
th.string = "Start Time"
tr.insert(2, th)

th = soup.new_tag('th')
th.string = "End time"
tr.insert(3, th)

th = soup.new_tag('th')
th.string = "Elapsed Time"
tr.insert(4, th)

tbody = soup.new_tag('tbody')
table.insert(1, tbody)

with open('output.xml') as raw_resuls:
    results = BeautifulSoup(raw_resuls, 'lxml')

# List for test cases
for tests in results.find_all("test"):    

    # List for keywords
    for keywords in tests.find_all("kw"):

        try:
            keyword_type = keywords['type']
            if  str(keyword_type) == "for" or str(keyword_type) == "foritem":
                continue

        except Exception :

            try:
                # Ignore library keywords
                keyword_library = keywords['library']

                if any (library in keyword_library for library in ignore_library):
                    continue

                else:
                    # Keywords which are not ignored
                    valid_keyword = True

            except Exception :
                # In output.xml library attribute will not be included for Local keywords
                local_keyword = True

            if valid_keyword or local_keyword:

                table_tr = soup.new_tag('tr')
                tbody.insert(1, table_tr)

                table_td = soup.new_tag('td')
                table_td.string = tests['name']
                table_tr.insert(0, table_td)

                table_td = soup.new_tag('td')
                table_td.string = keywords['name']
                table_tr.insert(1, table_td)

                for status in keywords.find_all("status"):
                    # Get duration took by keyword
                    start_time = datetime.datetime.strptime(status['starttime'], "%Y%m%d %H:%M:%S.%f")
                    end_time = datetime.datetime.strptime(status['endtime'], "%Y%m%d %H:%M:%S.%f")
                    
                table_td = soup.new_tag('td')
                table_td.string = str(start_time)
                table_tr.insert(2, table_td)

                table_td = soup.new_tag('td')
                table_td.string = str(end_time)
                table_tr.insert(3, table_td)

                duration = end_time - start_time

                table_td = soup.new_tag('td')
                table_td.string = str(duration)
                table_tr.insert(4, table_td)

# Write output as html file
with open(result_file, 'w') as outfile:
    outfile.write(soup.prettify())