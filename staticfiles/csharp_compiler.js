var exec = require('child_process').exec;
var compile = exec('csc C:/Users/User/Desktop/temp.cs', ['']);
var fs = require('fs');

compile.stdout.on('data', function (data) {
    console.log(String(data));

    var filePath = "C:\\Users\\User\\Desktop\\output.txt";

    fs.writeFile(filePath, String(data), function (err) {
        if(err){
            return console.log(err);
        }

        console.log("The file was saved!");
    });


});

compile.stderr.on('data', function (data) {
    console.log(String(data));
});
