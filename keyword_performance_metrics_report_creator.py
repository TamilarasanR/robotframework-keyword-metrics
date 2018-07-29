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

soup = BeautifulSoup('''<html><head><title>Keywords Performace Metrics Report</title></head></html>''',"html.parser")

# Convert output.html to "Keywords Performance Analysis Report"
# Ref Table Style: http://tablesorter.com/docs/example-pager.html

# Create meta tag
metatag = soup.new_tag('meta')
metatag.attrs["charset"] = "utf-8"
soup.head.append(metatag)

# Create link tag - responsive table
link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "http://tablesorter.com/docs/css/jq.css"
link.attrs["type"] = "text/css"
soup.head.append(link)

link = soup.new_tag('link')
link.attrs["rel"] = "stylesheet"
link.attrs["href"] = "http://tablesorter.com/themes/blue/style.css"
link.attrs["type"] = "text/css"
soup.head.append(link)

#JQuery
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.min.js"
soup.head.append(script)

# Create script tag - responsive table sorter js
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.30.7/js/jquery.tablesorter.js"
soup.head.append(script)

# table pager js
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "http://tablesorter.com/addons/pager/jquery.tablesorter.pager.js"
soup.head.append(script)

# Selection highlighter js
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "js/chili/chili-1.8b.js"
soup.head.append(script)

script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.attrs["src"] = "js/docs.js"
soup.head.append(script)

# Sorting script js
script_text = """$(function() {
	$("table")
		.tablesorter({widthFixed: true, widgets: ['zebra']})
		.tablesorterPager({container: $("#pager")});
	});"""
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.string = script_text
soup.head.append(script)

# search script js
script_text = """$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});"""
script = soup.new_tag('script')
script.attrs["type"] = "text/javascript"
script.string = script_text
soup.head.append(script)

body = soup.new_tag('body',style="font-family: Consolas,\"courier new\";padding: 10px;")
soup.insert(1, body)

# Create header tag and title
h1 = soup.new_tag('h1',style="display: block;font-size: 2.5em;")
h1.string = "Keywords Performace Metrics Report"
body.insert(0, h1)

br = soup.new_tag('br')
body.insert(1, br)

# search in current page
input = soup.new_tag('input')
input["id"] = "myInput"
input["type"] = "text"
input["placeholder"] = "Search for text within page..."
body.insert(2, input)

br = soup.new_tag('br')
body.insert(3, br)

# Get report result - OS independent
current_path = os.getcwd()
# output.xml file location
text_file = os.path.join(os.path.curdir, 'output.xml')
# performance report result file location
result_file = os.path.join(os.path.curdir, 'keyword_performace_metrics_result.html')

# Create table tag
# <table id="myTable">
table = soup.new_tag('table',style="padding: 10px")
table["id"] = "myTable"
table["class"] = "tablesorter"
body.insert(4, table)

thead = soup.new_tag('thead')
table.insert(0, thead)

tr = soup.new_tag('tr')
thead.insert(0, tr)

th = soup.new_tag('th')
th["class"] = "header"
th.string = "Test Case"
tr.insert(0, th)

th = soup.new_tag('th')
th["class"] = "header"
th.string = "Keyword"
tr.insert(1, th)

th = soup.new_tag('th')
th["class"] = "header"
th.string = "Keyword Duration"
tr.insert(2, th)

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
                    start_date = datetime.datetime.strptime(status['starttime'], "%Y%m%d %H:%M:%S.%f")
                    end_date = datetime.datetime.strptime(status['endtime'], "%Y%m%d %H:%M:%S.%f")
                    duration = end_date - start_date

                table_td = soup.new_tag('td')
                table_td.string = str(duration)
                table_tr.insert(2, table_td)


div = soup.new_tag('div',style="padding:25px;")
div["id"] = "pager"
div["class"] = "pager"
body.insert(5, div)

form = soup.new_tag('form')
div.insert(0, form)

img = soup.new_tag('img')
img["src"] = "http://tablesorter.com/addons/pager/icons/first.png"
img["class"] = "first"
form.insert(0, img)

img = soup.new_tag('img')
img["src"] = "http://tablesorter.com/addons/pager/icons/prev.png"
img["class"] = "prev"
form.insert(1, img)

input = soup.new_tag('input')
input["type"] = "text"
input["class"] = "pagedisplay"
form.insert(2, input)

img = soup.new_tag('img')
img["src"] = "http://tablesorter.com/addons/pager/icons/next.png"
img["class"] = "next"
form.insert(3, img)

img = soup.new_tag('img')
img["src"] = "http://tablesorter.com/addons/pager/icons/last.png"
img["class"] = "last"
form.insert(4, img)

select = soup.new_tag('select')
select["class"] = "pagesize"
form.insert(5, select)

option = soup.new_tag('option')
option["selected"] = "selected"
option["value"] = "10"
option.string = "10"
select.insert(0, option)

option = soup.new_tag('option')
option["value"] = "25"
option.string = "25"
select.insert(1, option)

option = soup.new_tag('option')
option["value"] = "50"
option.string = "50"
select.insert(2, option)

option = soup.new_tag('option')
option["value"] = "75"
option.string = "75"
select.insert(3, option)

option = soup.new_tag('option')
option["value"] = "100"
option.string = "100"
select.insert(4, option)

option = soup.new_tag('option')
option["value"] = "500"
option.string = "500"
select.insert(5, option)

option = soup.new_tag('option')
option["value"] = "1000"
option.string = "1000"
select.insert(6, option)

# Write output as html file
with open(result_file, 'w') as outfile:
    outfile.write(soup.prettify())