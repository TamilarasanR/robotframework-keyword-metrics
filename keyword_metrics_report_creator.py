from bs4 import BeautifulSoup
import sys
import os
from robot.api import ExecutionResult, ResultVisitor

# Ignores following library keywords in metrics report
ignore_library = [
    'BuiltIn',
    'SeleniumLibrary',
    'String',
    'Collections',
    'DateTime',
    ]

# Ignores following type keywords in metrics report
ignore_type = [
    'foritem',
    'for',
    ]

rootdir = os.getcwd()

report_file="report.html"
output_file="output.xml"
log_file="log.html"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if 'output' in filepath and filepath.endswith(".xml"):
            output_file= str(filepath)

# output.xml file location
#text_file = os.path.join(os.path.curdir, 'output.xml')
# performance report result file location
result_file = os.path.join(os.path.curdir, 'keyword_metrics_result.html')

result = ExecutionResult(output_file)
result.configure(stat_config={'suite_stat_level': 2,
                              'tag_stat_combine': 'tagANDanother'})

head_content = """

<!DOCTYPE html>
<html>
<link rel="shortcut icon" href="https://png.icons8.com/windows/50/000000/bot.png" type="image/x-icon" />
<title>RF Keyword Metrics Report</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
<link href="https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap.min.css" rel="stylesheet" type="text/css"/>
<script src="https://code.jquery.com/jquery-3.3.1.js" type="text/javascript"></script>
<script type = "text/javascript" src = "https://www.gstatic.com/charts/loader.js"></script>
<script type = "text/javascript">google.charts.load('current', {packages: ['corechart']});</script>
<script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" type="text/javascript"></script>
<script src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js" type="text/javascript"></script>
<style>
.w3-row-padding img {margin-bottom: 12px}

/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 120px;background: #222;}

/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
#main {margin-left: 120px}

/* Remove margins from "page content" on small screens */
@media only screen and (max-width: 600px) {#main {margin-left: 0}}

* {box-sizing: border-box}

/* Set height of body and the document to 100% */
body, html {
    height: 100%;
    margin: 0;
    font-family:  Comic Sans MS;
}

/* Style tab links */
.tablink {
    color: white;
    cursor: pointer;
}

.tablink:hover {
    background-color: #777;
}

.loader,
.loader:after {
    border-radius: 50%;
    width: 10em;
    height: 10em;
    position: center;
}
.loader {
    margin: 60px auto;
    font-size: 10px;
    position: relative;
    text-indent: -9999em;
    border-top: 1.1em solid rgba(255, 255, 255, 0.2);
    border-right: 1.1em solid rgba(255, 255, 255, 0.2);
    border-bottom: 1.1em solid rgba(255, 255, 255, 0.2);
    border-left: 1.1em solid #ffffff;
    -webkit-transform: translateZ(0);
    -ms-transform: translateZ(0);
    transform: translateZ(0);
    -webkit-animation: load8 1.1s infinite linear;
    animation: load8 1.1s infinite linear;
}
@-webkit-keyframes load8 {
    0% {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(360deg);
        transform: rotate(360deg);
    }
}
@keyframes load8 {
    0% {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(360deg);
        transform: rotate(360deg);
    }
}
#loadingDiv {
    position:absolute;;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-color:grey;
}

#dashboard {background-color: white;}
#keywordMetrics {background-color: white;}
#emailStatistics {background-color: white;}

</style>
</head>
</html>
"""

soup = BeautifulSoup(head_content,"html.parser")

body = soup.new_tag('body')
soup.insert(20, body)

loadingDiv = soup.new_tag('div')
loadingDiv["id"] = "loadingDiv"
body.insert(1, loadingDiv)

spiner = soup.new_tag('div')
spiner["class"] = "loader"
loadingDiv.insert(0, spiner)

icons_txt= """

<!-- Icon Bar (Sidebar - hidden on small screens) -->
<nav class="w3-sidebar w3-bar-block w3-small w3-hide-small w3-center">
  <a href="#" id="defaultOpen" onclick="openPage('dashboard', this, 'orange')" class="tablink w3-bar-item w3-button w3-padding-large">
    <i class="fa fa-dashboard w3-xxlarge"></i>
    <p>DASHBOARD</p>
  </a>
  <a href="#" onclick="openPage('keywordMetrics', this, 'orange');executeDataTable('#km',4)" class="tablink w3-bar-item w3-button w3-padding-large" >
    <i class="fa fa-table w3-xxlarge"></i>
    <p>KEYWORD METRICS</p>
  </a>
  <a href="#" onclick="openPage('statistics', this, 'orange');" class="tablink w3-bar-item w3-button w3-padding-large">
    <i class="fa fa-envelope-o w3-xxlarge"></i>
    <p> EMAIL STATISTICS</p>
  </a>
</nav>

<!-- Navbar on small screens (Hidden on medium and large screens) -->
<div class="w3-top w3-hide-large w3-hide-medium" id="myNavbar">
  <div class="w3-bar w3-black w3-opacity w3-hover-opacity-off w3-center w3-small">
    <a href="#" id="defaultOpen" onclick="openPage('dashboard', this, 'orange')" class="tablink w3-bar-item w3-button" style="width:25% !important">DASHBOARD</a>
    <a href="#" onclick="openPage('keywordMetrics', this, 'orange');executeDataTable('#km',4)" class="tablink w3-bar-item w3-button" style="width:25% !important">KEYWORD METRICS</a>
    <a href="#" onclick="openPage('statistics', this, 'orange');" class="tablink w3-bar-item w3-button" style="width:25% !important">EMAIL STATISTICS</a>
  </div>
</div>

"""

body.append(BeautifulSoup(icons_txt, 'html.parser'))


page_content_div = soup.new_tag('div')
page_content_div["id"] = "main"
page_content_div["class"] = "w3-padding-large"
body.insert(30, page_content_div)

# Keywords div
km_div = soup.new_tag('div')
km_div["id"] = "keywordMetrics"
km_div["class"] = "tabcontent"
page_content_div.insert(150, km_div)

# Statistics div
statisitcs_div = soup.new_tag('div')
statisitcs_div["id"] = "statistics"
statisitcs_div["class"] = "tabcontent"
page_content_div.insert(300, statisitcs_div)

### ============================ START OF DASHBOARD ======================================= ####
total_keywords = 0
passed_keywords = 0
failed_keywords = 0

class KeywordResults(ResultVisitor):
    
    def start_keyword(self,kw):
        # Ignore library keywords
        keyword_library = kw.libname

        if any (library in keyword_library for library in ignore_library):
            pass
        else:
            keyword_type = kw.type            
            if any (library in keyword_type for library in ignore_type):
                pass
            else:
                global total_keywords
                total_keywords+= 1
                if kw.status== "PASS":
                    global passed_keywords
                    passed_keywords+= 1
                else:
                    global failed_keywords
                    failed_keywords += 1

result.visit(KeywordResults())

dashboard_content="""
<div class="tabcontent" id="dashboard">
    <h4><b><i class="fa fa-dashboard"></i> Dashboard</b></h4>
  <hr>
        <div class="w3-row-padding w3-margin-bottom">
        <div class="w3-quarter col-sm-3">
        <div class="w3-container w3-dark-gray w3-padding-8">
            <div class="w3-clear">
            <h3 class="text-center" style="font-size:25px"><b>Keyword</b></h3>
            </div>
            <div class="w3-left"></div>
            <h4 style="font-size:13px" class="text-center">Statistics</h4>
            </div>
        </div>
        <div class="w3-quarter col-sm-3">
        <div class="w3-container w3-teal w3-padding-8">
            <div class="w3-clear">
            <h3 class="text-center" style="font-size:25px"><b>%s</b></h3>
            </div>
            <div class="w3-left"></div>
            <h4 style="font-size:13px" class="text-center">Total</h4>
            </div>
        </div>
        <div class="w3-quarter col-sm-3">
        <div class="w3-container w3-green w3-padding-8">
            <div class="w3-clear">
            <h3 class="text-center" style="font-size:25px"><b>%s</b></h3>
            </div>
            <div class="w3-left"></div>
            <h4 style="font-size:13px" class="text-center">Passed</h4>
            </div>
        </div>
        <div class="w3-quarter col-sm-3">
        <div class="w3-container w3-red w3-padding-8">
            <div class="w3-clear">
            <h3 class="text-center" style="font-size:25px"><b>%s</b></h3>
            </div>
            <div class="w3-left"></div>
            <h4 style="font-size:13px" class="text-center">Failed</h4>
            </div>
        </div>
    </div>

    <hr>
    <div class="col-md-12 chart-blo-1" id="keywordChartID" style="height: 400px;"></div>
    <div class="col-md-12 chart-blo-1" id="keywordsBarID" style="height: 400px;"></div>
   
   <script>
    window.onload = function(){
    executeDataTable('#km',5);
    createPieChart(%s,%s,'keywordChartID','Keywords Status:');
    createBarGraph('#km',1,5,10,'keywordsBarID','Top 10 Keywords Performance:','Keyword')
	};
   </script>
  </div>
""" % (total_keywords,passed_keywords,failed_keywords,passed_keywords,failed_keywords)
page_content_div.append(BeautifulSoup(dashboard_content, 'html.parser'))

### ============================ END OF DASHBOARD ============================================ ####

### ============================ START OF KEYWORD METRICS ======================================= ####

keyword_icon_txt="""
<h4><b><i class="fa fa-table"></i> Keyword Metrics</b></h4>
  <hr>
"""
km_div.append(BeautifulSoup(keyword_icon_txt, 'html.parser'))

# Create table tag
# <table id="myTable">
table = soup.new_tag('table')
table["id"] = "km"
table["class"] = "table table-striped table-bordered"
km_div.insert(10, table)

thead = soup.new_tag('thead')
table.insert(0, thead)

tr = soup.new_tag('tr')
thead.insert(0, tr)

th = soup.new_tag('th')
th.string = "Test Case"
tr.insert(1, th)

th = soup.new_tag('th')
th.string = "Keyword"
tr.insert(1, th)

th = soup.new_tag('th')
th.string = "Status"
tr.insert(2, th)

th = soup.new_tag('th')
th.string = "Start Time"
tr.insert(3, th)

th = soup.new_tag('th')
th.string = "End time"
tr.insert(4, th)

th = soup.new_tag('th')
th.string = "Elapsed Time(s)"
tr.insert(5, th)

tbody = soup.new_tag('tbody')
table.insert(1, tbody)

class KeywordResults(ResultVisitor):

    def __init__(self):
        self.test = None

    def start_test(self, test):
        self.test = test

    def end_test(self, test):
        self.test = None

    def start_keyword(self,kw):
        # Get test case name (Credits: Robotframework author - Pekke)
        test_name = self.test.name if self.test is not None else ''

         # Ignore library keywords
        keyword_library = kw.libname

        if any (library in keyword_library for library in ignore_library):
            pass
        else:
            keyword_type = kw.type            
            if any (library in keyword_type for library in ignore_type):
                pass
            else:
                table_tr = soup.new_tag('tr')
                tbody.insert(1, table_tr)

                table_td = soup.new_tag('td',style="word-wrap: break-word;max-width: 300px; white-space: normal")
                
                if keyword_type != "kw":
                    table_td.string = str(kw.parent)
                else:
                    table_td.string = str(test_name)
                table_tr.insert(0, table_td)

                table_td = soup.new_tag('td',style="word-wrap: break-word;max-width: 300px; white-space: normal")
                table_td.string = str(kw.kwname)
                table_tr.insert(1, table_td)

                table_td = soup.new_tag('td')
                table_td.string = str(kw.status)
                table_tr.insert(2, table_td)

                table_td = soup.new_tag('td')
                table_td.string = str(kw.starttime)
                table_tr.insert(3, table_td)

                table_td = soup.new_tag('td')
                table_td.string = str(kw.endtime)
                table_tr.insert(4, table_td)

                table_td = soup.new_tag('td')
                table_td.string =str(kw.elapsedtime/float(1000))
                table_tr.insert(5, table_td)

result.visit(KeywordResults())
### ============================ END OF KEYWORD METRICS ======================================= ####

### ============================ EMAIL STATISTICS ================================== ###

emailStatistics="""
<h4><b><i class="fa fa-envelope-o"></i> Email Statistics</b></h4>
<hr>
<button id="create" class="btn btn-primary active" role="button" onclick="updateTextArea();this.style.visibility= 'hidden';"><i class="fa fa-cogs"></i> Generate Statistics Email</button>
<a download="message.eml" class="btn btn-primary active" role="button" id="downloadlink" style="display: none; width: 300px;font-weight: bold;"><i class="fa fa-download"></i> Click Here To Download Email</a>

<script>
function updateTextArea() {
    var keyword ="<b>Top 10 Keyword Performance:</b><br><br>" + $("#keywordsBarID table")[0].outerHTML;
    var saluation="<pre><br>Please refer RF Keyword Metrics Report for detailed statistics.<br><br>Regards,<br>QA Team</pre></body></html>";
    document.getElementById("textbox").value += "<br>" + keyword + saluation;
    $("#create").click(function(){
    $(this).remove();
    });
}
</script>

<textarea id="textbox" class="col-md-12" style="height: 400px; padding:1em;">
To: myemail1234@email.com
Subject: Automation Execution Status
X-Unsent: 1
Content-Type: text/html

<html>
   <head>
      <style>
         body, html, table,pre,b {
			 font-family: Calibri, Arial, sans-serif;
			 font-size: 1em; 
         }
         .pastdue { color: crimson; }
         table {
			 border: 1px solid silver;
			 padding: 6px;
			 margin-left: 30px;
			 width: 600px;
         }
         thead {
			 text-align: center;
			 font-size: 1.1em;        
			 background-color: #B0C4DE;
			 font-weight: bold;
			 color: #2D2C2C;
         }
         tbody {
			text-align: center;
         }
         th {
            width: 25%%;
            word-wrap:break-word;
         }
      </style>
   </head>
   <body>
<pre>Hi Team,
Following are the last build execution keyword statistics.

<b>Metrics:<b>

</pre>
      <table>
         <thead>
            <th style="width: 25%%;">Statistics</th>
            <th style="width: 25%%;">Total</th>
            <th style="width: 25%%;">Pass</th>
            <th style="width: 25%%;">Fail</th>
         </thead>
         <tbody>
            <tr>
               <td style="text-align: left;font-weight: bold;"> KEYWORDS </td>
               <td style="background-color: #F5DEB3;text-align: center;">%s</td>
               <td style="background-color: #90EE90;text-align: center;">%s</td>
               <td style="background-color: #F08080;text-align: center;">%s</td>
            </tr>
         </tbody>
      </table>


</textarea>

""" % (total_keywords,passed_keywords,failed_keywords)
statisitcs_div.append(BeautifulSoup(emailStatistics, 'html.parser'))

### ============================ END OF EMAIL STATISTICS ================================== ###

script_text="""
 <script>
(function () {
var textFile = null,
  makeTextFile = function (text) {
    var data = new Blob([text], {type: 'text/plain'});
    if (textFile !== null) {
      window.URL.revokeObjectURL(textFile);
    }
    textFile = window.URL.createObjectURL(data);
    return textFile;
  };

  var create = document.getElementById('create'),
    textbox = document.getElementById('textbox');
  create.addEventListener('click', function () {
    var link = document.getElementById('downloadlink');
    link.href = makeTextFile(textbox.value);
    link.style.display = 'block';
  }, false);
})();
</script>
 <script>
  function createPieChart(passed_count,failed_count,ChartID,ChartName){
	var status = [];
	status.push(['Status', 'Percentage']);
	status.push(['PASS',parseInt(passed_count)],['FAIL',parseInt(failed_count)]);
	var data = google.visualization.arrayToDataTable(status);

	var options = {
      title: ChartName,
        titleTextStyle: {
            fontName: 'Comic Sans MS',
            fontSize: 15,
            bold: true,
        },
	  pieHole: 0.7,
	  legend: 'none',
      chartArea: {width: "90%",height: "75%"},
	  colors: ['green', 'red'],
      annotations: {
            alwaysOutside: true,
            textStyle: {
                fontName: 'Comic Sans MS',
                fontSize: 13,
                bold: true,
                italic: true,
                color: "black",     // The color of the text.
            },
        },
	};

	var chart = new google.visualization.PieChart(document.getElementById(ChartID));
	chart.draw(data, options);
  }
 </script>
 <script>
  function createBarGraph(tableID,keyword_column,time_column,limit,ChartID,ChartName,type){
		var status = [];
		css_selector_locator = tableID + ' tbody >tr'
		var rows = $(css_selector_locator);
		var columns;
		var myColors = [
			'#4F81BC',
            '#C0504E',
            '#9BBB58',
            '#24BEAA',
            '#8064A1',
            '#4AACC5',
            '#F79647',
            '#815E86',
            '#76A032',
            '#34558B'
		];
		status.push([type, 'Elapsed Time(s)',{ role: 'annotation'}, {role: 'style'}]);
		for (var i = 0; i < rows.length; i++) {
			if (i == Number(limit)){
				break;
			}
			//status = [];
			name_value = $(rows[i]).find('td'); 
		  
			time=($(name_value[Number(time_column)]).html()).trim();
			keyword=($(name_value[Number(keyword_column)]).html()).trim();
			status.push([keyword,parseFloat(time),parseFloat(time),myColors[i]]);
		  }
		  var data = google.visualization.arrayToDataTable(status);

		  var options = {            
            title: ChartName,
            titleTextStyle: {
                    fontName: 'Comic Sans MS',
                    fontSize: 15,
            },
            legend: 'none',
            chartArea: {width: "92%",height: "75%"},
            bar: {
                groupWidth: '90%'
            },
			annotations: {
				alwaysOutside: true,
                textStyle: {
                fontName: 'Comic Sans MS',
                fontSize: 13,
                bold: true,
                italic: true,
                color: "black",     // The color of the text.
                },
			},
            hAxis: {
                textStyle: {
                    fontName: 'Arial',
                    fontSize: 10,
                }
            },
            vAxis: {
                format: 'decimal',
                title: "Seconds",
                gridlines: { count: 10 },
                textStyle: {                    
                    fontName: 'Comic Sans MS',
                    fontSize: 10,
                }
            },
		  };  

            // Instantiate and draw the chart.
            var chart = new google.visualization.ColumnChart(document.getElementById(ChartID));
            chart.draw(data, options);
         }
         google.charts.setOnLoadCallback(drawChart);
</script>

 <script>
  function executeDataTable(tabname,sortCol) {
    $(tabname).DataTable(
        {
        retrieve: true,
        "order": [[ Number(sortCol), "desc" ]]
        } 
    );
}
 </script>
 <script>
  function openPage(pageName,elmnt,color) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = color;

}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
 </script>
 <script>
  //$('body').append('<div style="" id="loadingDiv"><div class="loader"></div></div>');
$(window).on('load', function(){
  setTimeout(removeLoader, 0); //wait for page load PLUS zero seconds.
});
function removeLoader(){
    $( "#loadingDiv" ).fadeOut(50, function() {
      // fadeOut complete. Remove the loading div
      $( "#loadingDiv" ).remove(); //makes page more lightweight
  });
}
</script>
"""

body.append(BeautifulSoup(script_text, 'html.parser'))

### ====== WRITE TO RF_METRICS_REPORT.HTML ===== ###

# Write output as html file
with open(result_file, 'w') as outfile:
    outfile.write(soup.prettify())