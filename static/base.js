/*function pleaseWait() {
	$.msg({
		content      : 'Please wait...',
		bgPath	     : $('#jqueryimages').val(),
		autoUnblock  : false,
		clickUnblock : false,
		center       : {
			topPercentage : 0.5
		}
	});
}
*/

/*
function waitingOver() {
	$.msg('unblock');
}
*/

(function($) {
	var events = $({
		onmaxlength: function() {}
	});
	$.fn.maxlength = function(options) {
		// register event callbacks
		if (options) {
			$.each(options, function(event, fn) {
				if (typeof(fn) == 'function') {
					events.unbind(event);
					events.bind(event, fn);
				}
			});
		}
		this.keypress(function(event) {
			var key = event.which;
			//all keys including return.
			if (key >= 33 || key == 13) {
				var maxLength = $(this).attr("maxlength");
				if (maxLength >= 0) {
					var length = this.value.length;
					if (length >= maxLength) {
						event.preventDefault();
						events.trigger('onmaxlength');
					}
				}
			}
		});
		return this;
	}
})(jQuery);


/*
function selectTab(tabview, index) {
	if (tabview.tabs('option', 'selected') != index) {
		tabview.tabs('select', index);
	}
}
*/

/*
function submitSuccess(data, textstatus, jqXHR) {
	console.log(data);

	var output = $('#output');
	output.html('');
	//data = JSON.parse(data);

	lines = data[1].split('\n');

	for (var i=0; i < lines.length; i++) {
		if (lines[i].indexOf('error') != -1) {
			output.append('<p><span class="error">' + lines[i] + '</span></p>')
		} else if (lines[i].indexOf('warning') != -1) {
			output.append('<p><span class="warning">' + lines[i] + '</span></p>')
		} else {
			output.append('<p><span>' + lines[i] + '</span></p>')
		}
	}
	if (data[0] == 0) {
		output.append('<p><span class="success">Execution Successful!</span></p>');
	} else {
		output.append('<p><span class="failed">Execution Failed!</span></p>');
	}


	//output.append('<p><span class="failed">' + data.responseText + '</span></p>');
	output.append('<p><span class="failed">Derleme Başarılı</span></p>');
}
*/




function submitError(data) {
	 console.log(data);
	 var output = $('#output');
	 output.html('');
	 output.append('<p><span class="error">' + data.responseText + '</span></p>');
	 output.append('<p><span class="failed">Execution!</span></p>');
}


$(document).ready(function() {
	//$('input[type="button"]').button();
	//$('input[type="submit"]').button();
	//$( ".radio" ).buttonset();
	/*$( ".tabview" ).tabs({
		collapsible: true
	});*/
	//$('textarea[maxlength]').maxlength();
});


function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			// Only send the token to relative URLs i.e. locally.
			xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
		}
	}
});
