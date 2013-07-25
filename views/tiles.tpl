<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>jQuery UI Sortable - Connect lists</title>
  <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
  <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
  <script src="/jquery.ui.touch-punch.min.js"></script>
  <link rel="stylesheet" href="/resources/demos/style.css" />
  <style>
      #sortable1, #sortable2 { list-style-type: none; margin: 0; padding: 0 0 2.5em; float: left; margin-right: 10px; }
      #sortable1 li, #sortable2 li { margin: 0 5px 5px 5px; padding: 5px; font-size: 1.2em; width: 360px; }
      #silFormHidden {visibility:hidden;}
  </style>
  <script>
  $(function() {
    $( "#sortable2" ).sortable({
      connectWith: "#sortable1",
   }).disableSelection();
    $( "#sortable1" ).sortable({
      receive: function(event, ui) {
          // The position where the new item was dropped
          var newIndex = ui.item.index();
          ui.item.children('#silFormHidden').css('visibility','visible');
          ui.item.children('#ekleForm').hide();
          //alert(ui.item.children('#silFormHidden').css());

          var yazi_url =ui.item.attr('url');
          // Do some ajax action...
          $.post('/koseyazisi/{{!user_name}}',{
            url: yazi_url
          });
      }
    }).disableSelection();
    $(".deleteButton").click(function() {
        var form = $(this).closest('form');
        var obj_id = form.find("#object_id").val()
        var url_id = form.find("#url").val()
        $.post('/koseyazisi/{{!user_name}}/sil',{
            object_id: obj_id,
            url: url_id
        });
        var item = $(this).closest('li');
        item.hide(1000);
        return false;
    });
  });

  </script>
</head>
<body>

<ul id="sortable2" class="connectedSortable">
Bugunku Yazilar
    %for row in rows_new:
      %url = row.pop()
      <li class="ui-state-default"  url="{{!url}}">
      %for col in row:
        <br>{{!col}}
      %end
      </li>
    %end
</ul>

<ul id="sortable1" class="connectedSortable">
Arisivim
    %for row in rows:
      <li class="ui-state-default" id="{{!row[0]}}">

      %for col in row:
        <br>{{!col}}
      %end
      </li>
    %end
</ul>
