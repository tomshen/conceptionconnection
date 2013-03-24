function getEvents() {
    var url = '/conception'
    var req = new XMLHttpRequest()
    var birthdate = "" + 
                    document.getElementById('year').value + "-" + 
                    document.getElementById('month').value + "-" + 
                    document.getElementById('day').value;
    var delta = document.getElementById('delta').value
    var params = ''
    if(delta) {
        var params = {
            'birthdate': birthdate,
            'delta': delta,
            'type': 'html' // leave out for JSON
        }
    }
    else {
        var params = {
            'birthdate': birthdate,
            'type': 'html'
        }
    }
    function toQueryString(obj) {
        var parts = [];
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                parts.push(encodeURIComponent(i) + "=" + encodeURIComponent(obj[i]));
            }
        }
        return parts.join("&");
    }
    url += '?' + toQueryString(params)
    req.open('GET', url, false)
    req.send(null)
    document.getElementById('events').innerHTML = req.responseText
}