function getDetails(id) {
    $.getJSON('/jobs/' + id, function(data) {
       output=data.stdout;
       $(details).html(output).wrap('<pre />')
    })
}

$.getJSON('/jobs', function(data) {
    output="<table><th align='left'>Job</th><th>Status</th>"
    for (var i in data) {
        output+="<tr>"
        output+="<td><a href=javascript:getDetails("+i+")>"
        output+=data[i].command + "</a></td>"
        output+="<td>" + data[i].status + "</td>"
        output+="</tr>"
    }
    output+="</table>"
    $(jobs).html(output);
})
