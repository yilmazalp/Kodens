 var editor = null;
//input: $('#stdin').val(),

function submitCode() {

	/*
	$.ajax({
		type: 'POST',
		url: $('#submit').val(),
        dataType: 'json',
		data: {
            language: $('#language').val(),
            /*code: "#include <stdio.h>\n" +
			      "void main(){\n" +
                  "    int i;\n" +
                  "    printf(\"Merhaba Dunya\\n\");\n" +
                  "}",*/
            //code: editor.getValue(),
        //},

		/*
		success: function (jsondata) {
			//JSON.stringify(jsondata);
			$('#output').append('Basarili');
			//CompileCode(jsondata);
        },
		error: function(data) {
			submitError(data);
		},


	});
	*/
	//pleaseWait();
}




function selectTheme() {
	//var theme = this.options[this.selectedIndex].innerHTML;
	var theme = this.value;
	editor.setOption("theme", theme);
}

/*
$(document).ready(function() {
	$('#submit').click(submitCode);
	//$('input[type="radio"]').click(selectTheme);
	editor = decorateCodeMirror($('#language').val());
});
*/
