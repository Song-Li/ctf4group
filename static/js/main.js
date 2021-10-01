$(document).ready(function() {
  $('#formButton').on('click', function() {
    this.disabled = true;
    if ($('#black').css('opacity') == 0) $('#black').css('opacity', 1);
    else $('#black').css('opacity', 0);
    setTimeout(function(){
      $("#formButton").html("祝你好运");
    }, 2000);
    setTimeout(function(){
      window.location.replace("/challenges/q1.html");
    }, 4000);
  });
});
