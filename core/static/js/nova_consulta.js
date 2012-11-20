 function validate(value) {
        var url = value;
        var pattern = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        if (pattern.test(url)) {
            return true;
        }
            return false;
    }

$(document).ready(function() {
	$('.a-dia, .agendar').live('click', function(event){
		$.get($(this).attr('data-url'),
			function(data){
				if (validate(data)) {
					window.location.replace(data);
					window.location.href(data);
				}
				$("#agenda").html(data);
			}
		);
	});
	$('.nav-calendar').live('click', function(event){
		$.get($(this).attr('data-url'),
			function(data){
				$("#calendario").html(data);
			}
		);
	});
	$('.delete a').live('click', function(event){
		if (confirm("Confirma o cancelamento da consulta?")){
			$.post($(this).attr('data-url'),
				{'next': $(this).attr('data-next')},
				function(data){
					$("#agenda").html($(data).find(".tablewrapper"));
					$("#agenda").append($(data).children().last());
				}
			);
		}
	});
});
