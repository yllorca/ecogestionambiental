!function(e){"use strict";var t='<link id="style-switcher" href="" rel="stylesheet" type="text/css">\t\t<div class="custom-panel">\t\t\t<div class="panel-header">\t\t\t\t<span>Style Switcher</span>\t\t\t</div>\t\t\t<div class="panel-options">\t\t\t\t<ul class="accent color-picker clearfix">\t\t\t\t</ul>\t\t\t\t<p>These color skins are included inside the template, and also you can easily create your own one!</p>\t\t\t</div>\t\t\t<div class="panel-toggle">\t\t\t\t<i class="fa fa-cog"></i>\t\t\t</div>\t\t</div>',l="assets/css/template-",c=[{colorCode:"#3498db",fileName:"blue.css"},{colorCode:"#47b475",fileName:"green.css"},{colorCode:"#e74c3c",fileName:"alizarin.css"},{colorCode:"#95a5a6",fileName:"concrete.css"},{colorCode:"#2ecc71",fileName:"emerald.css"},{colorCode:"#CDDC39",fileName:"lime.css"},{colorCode:"#00BCD4",fileName:"cyan.css"},{colorCode:"#673AB7",fileName:"deep-purple.css"},{colorCode:"#FF9800",fileName:"orange.css"},{colorCode:"#795548",fileName:"brown.css"}];e(document).ready(function(){e(".wrapper").after(t),c.forEach(function(t){var l='style="background-color: '+t.colorCode+"; border: 2px solid "+t.colorCode+';"';e("ul.accent.color-picker").append("<li><a "+l+' data-file-name="'+t.fileName+'" href="#"></a></li>')});var a=e(".custom-panel").innerWidth(),o=e(".panel-header").outerHeight(),s=-1*a;e(".custom-panel").css({left:s+"px"}),e(".panel-toggle").css({left:a+"px",top:o+"px"}),e("ul.accent.color-picker a").click(function(t){t.preventDefault(),e("ul.accent.color-picker a").removeClass("selected-color"),e(this).addClass("selected-color");var c=e(this).data("file-name");e("#style-switcher").attr("href",l+c)}),e(".panel-toggle").on("click",function(){var t=e(".custom-panel");parseInt(t.css("left"))==s?t.animate({left:"0px"},250):0==parseInt(t.css("left"))&&t.animate({left:s},250)})})}(jQuery);