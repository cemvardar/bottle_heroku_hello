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
<form action="/" method="POST">
    Date : <input name="date"     type="text" id="datepicker" />
    Duration: <input name="duration in minutes" type="text" />
    <input type="submit" value="AddCommute"/>
</from>
</p>
%include table titles=['date','durations'], rows=[['a','b'],['b','a']]