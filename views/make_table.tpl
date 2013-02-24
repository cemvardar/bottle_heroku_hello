<table border="1">
  <tr>
  %for title in titles:
    <td>{{title}}</td>
  %end
  </tr>

%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>

<form action="/" method="POST">
    <input name="name"     type="text" />
    <input name="lastname" type="text" />
    <input type="submit" value="Add"/>
</from>