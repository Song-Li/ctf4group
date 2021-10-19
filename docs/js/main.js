function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
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
  // for index html
  $('#formButton').on('click', function() {
    this.disabled = true;
    if ($('#black').css('opacity') == 0) $('#black').css('opacity', 1);
    else $('#black').css('opacity', 0);
    setTimeout(function(){
      $("#formButton").html("祝你好运");
      if ($("#username").val() == "") {
        alert("请告诉我们您的QQ号, 方便我们认识您");
        $("#formButton").prop('disabled', false);
      } else {
        submit("https://ctfapi.hackgroup.org/request", {'username': $('#username').val()}, function(data) {
          // set cookie
          document.cookie = "cookie=" + data['cookie'] + "; expires=Fri, 31 Dec 9999 23:59:59 GMT";
          window.location.href = "/challenges/q1.html";
        })
      }
    }, 2000);
  });

  // for challenges
  $("#submit_q1").on('click', function(e){
    e.preventDefault();

    submit("https://ctfapi.hackgroup.org/submit", getFormData($('#form_q1')), function(data) {
      if(data['res'] == "wrong") {
        alert("你确定这是md5加密后的公钥吗？好像不太对啊！")
        window.location.href = "/challenges/q1.html";
      } else {
        alert("答对啦！而且我们已经记录下来你的提交啦！")
        window.location.href = "/challenges/q2.html";
      }
    })
  });

  $("#submit_q2").on('click', function(e){
    e.preventDefault();
    submit("https://ctfapi.hackgroup.org/submit", getFormData($('#form')), function(data) {
      if(data['res'] == "wrong") {
        alert("你确定这是你的答案吗？好像不太对啊！")
        window.location.href = "/challenges/q2.html";
      } else {
        alert("答对啦！而且我们已经记录下来你的提交啦！")
        window.location.href = "/challenges/q3.html";
      }
    })
  });

});

function download(filename, text) {
  var element = document.getElementById('rsadownload');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  //element.click();
}

function getInfo_q1() {
  // get information from server
  submit("https://ctfapi.hackgroup.org/getinfo", {'cha_no': '1'}, function(data){
    cookie = data['cookie']
    username = data['username']
    $('#username').val(username);
    $('#username').prop('disabled', true);
    download('rsa', data['pri']);
  });
}

function getInfo_q2() {
  // get information from server
  submit("https://ctfapi.hackgroup.org/getinfo", {'cha_no': '2'}, function(data){
    cookie = data['cookie']
    username = data['username']
    $('#username').val(username);
    $('#username').prop('disabled', true);
  });
}
