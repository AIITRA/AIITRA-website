$(document).ready(function () {
  $("ul.navbar-nav > li").click(function (e) {
   $("ul.navbar-nav > li").removeClass("active");
   $(this).addClass("active");
    });
  // $(".contact .icon").hover(function(e){
  // 	$(".contact .fa-stack-1x").addClass("fa-inverse");
  // });
});