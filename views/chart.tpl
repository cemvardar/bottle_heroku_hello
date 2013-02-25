<!--
You are free to copy and use this sample in accordance with the terms of the
Apache license (http://www.apache.org/licenses/LICENSE-2.0.html)
-->

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>
      Google Visualization API Sample
    </title>
    <script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages: ['corechart']});
    </script>
    <script type="text/javascript">
      function getData() {


        return [
                         ['Year', 'Austria', 'Bulgaria', 'Denmark', 'Greece'],
                         ['2003',  1336060,    400361,    1001582,   997974],
                         ['2004',  1538156,    366849,    1119450,   941795],
                         ['2005',  1576579,    440514,    993360,    930593],
                         ['2006',  1600652,    434552,    1004163,   897127],
                         ['2007',  1968113,    393032,    979198,    1080887],
                         ['2008',  1901067,    517206,    916965,    1056036]
                       ];
      }
      function drawVisualization() {
            var jsonData = $.ajax({
                url: "/chartdata",
                dataType:"json",
                async: false
                }).responseText;
        document.getElementById("ajaxData").innerHTML = jsonData;
        // Create and populate the data table.
        //var data = jsonData.getDataTable();
        var data = new google.visualization.DataTable(jsonData);

        // Create and draw the visualization.
        new google.visualization.BarChart(document.getElementById('visualization')).
            draw(data,
                 {title:"Yearly Coffee Consumption by Country",
                  width:600, height:400,
                  vAxis: {title: "Year"},
                  hAxis: {title: "Cups"}}
            );
      }
      google.setOnLoadCallback(drawVisualization);
    </script>
  </head>
  <body style="font-family: Arial;border: 0 none;">
    <div id="visualization" style="width: 600px; height: 400px;"></div>

    <p>Result from function call2</p>
    <div id="raw"></div>
    <br />

    <p>Result from ajax call2</p>
    <div id="ajaxData"></div>
    <br />
  </body>
  <script type="text/javascript">
    function changeText() {
      document.getElementById("raw").innerHTML = '5';
    }
    changeText();
  </script>
</html>