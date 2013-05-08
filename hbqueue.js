function getDetails(id) {
    $.getJSON('/jobs/' + id, function(data) {
       output=data.stdout;
       $(details).html(output).wrap('<pre />')
    })
}

$.getJSON('/jobs', function(data) {
    var j=0
    output="<table><th align='left'>Job</th><th>Is running</th>"
    for (var i in data) {
        output+="<tr>"
        output+="<td><a href=javascript:getDetails("+j+")>"
        output+=data[i].command + "</a></td>"
        output+="<td>" + data[i].alive + "</td>"
        output+="</tr>"
        j++
    }
    output+="</table>"
    $(jobs).html(output);
})
