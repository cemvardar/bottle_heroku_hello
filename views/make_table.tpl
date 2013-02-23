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