<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.2/themes/smoothness/jquery-ui.css" />
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
<script src="http://code.jquery.com/ui/1.10.2/jquery-ui.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css" />
<script>
$(function() {
    $( "#datepicker" ).datepicker();
});
</script>

<p>
<form action="/commutes" method="POST">
    Date : <input name="date"     type="text" id="datepicker" />
    Duration (in minutes): <input name="duration" type="text" />
    <input type="submit" value="AddCommute"/>
</form>
</p>

    <script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages: ['corechart']});
    </script>
    <script type="text/javascript">
      function drawVisualization() {
            var jsonData = $.ajax({
                url: "/commutedata",
                dataType:"json",
                async: false
                }).responseText;
        // Create and populate the data table.
        var data = new google.visualization.DataTable(jsonData);

        // Create and draw the visualization.
        new google.visualization.LineChart(document.getElementById('visualization')).
            draw(data,
                 {title:"Yearly Coffee Consumption by Country",
                  width:600, height:400,
                  vAxis: {title: "Year"},
                  hAxis: {title: "Cups"}}
            );
      }
      google.setOnLoadCallback(drawVisualization);
    </script>


<div id="visualization" style="width: 600px; height: 400px;"></div>

%include table titles=titles, rows=rows