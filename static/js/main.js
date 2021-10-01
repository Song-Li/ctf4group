function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function submit(target_url, content, cb) {
  // submit a dict to a target url in json format
  // add cookie to the content
  var cookie = getCookie("cookie")
  content['cookie'] = cookie;
  $.ajax({
    url: target_url,
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    cache: false,
    processData: false,
    data: JSON.stringify(content),
    success: (data) => {
      cb(data);
    }
  });
}

$(document).ready(function() {
  $('#formButton').on('click', function() {
    this.disabled = true;
    if ($('#black').css('opacity') == 0) $('#black').css('opacity', 1);
    else $('#black').css('opacity', 0);
    setTimeout(function(){
      $("#formButton").html("祝你好运");

      submit("/request", {'username': $('#username').val()}, function(data) {
        console.log(data);
        // set cookie
        document.cookie = "cookie=" + data['cookie'] + "; expires=Fri, 31 Dec 9999 23:59:59 GMT";
        window.location.href = "/challenges/q1.html";
      })
    }, 2000);
  });
});

function download(filename, text) {
  var element = document.getElementById('rsadownload');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  element.click();
}

function getInfo_q1() {
  // get information from server
  submit("/getinfo", {'cha_no': '1'}, function(data){
    cookie = data['cookie']
    username = data['username']
    $('#username').val(username);
    $('#username').prop('disabled', true);
    download('rsa', data['pri']);
  });
}
