%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The results are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
  %for k, v in row.items():
    <td>{{v}}</td>
  %end
  </tr>
%end
</table>
