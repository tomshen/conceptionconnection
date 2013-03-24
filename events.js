function getEvents() {
    var url = '/conception'
    var req = new XMLHttpRequest()
    var birthdate = document.getElementById('birthdate').value
    var delta = document.getElementById('delta').value
    var params = ''
    if(delta) {
        var params = {
            'birthdate': birthdate,
            'delta': delta,
            'type': 'html' // leave out for JSON
        }
    }
    else { // delta has a default value of 5
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
    console.log(url)
    req.open('GET', url, false)
    req.send(null)
    document.getElementById('events').innerHTML = req.responseText
}