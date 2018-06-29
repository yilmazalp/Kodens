var spawn = require('child_process').spawn;
var exec = require('child_process').exec;
//var javac_app = "C:\\Program Files\\Java\\jdk1.8.0_05\\bin\\javac.exe";
var compile = exec('javac static/temp_files/JavaTest/Temp.java', ['']);

var fs = require('fs');

var inputFilePath = "static/data_files/input.txt";
var filePath = "static/data_files/output.txt";

var input_data = '';
var readStream = fs.createReadStream(inputFilePath, 'utf-8');
var writeStream = fs.createWriteStream(filePath);


//compile.stdout.setEncoding('utf8');


compile.stdout.on('data', function (data) {
    console.log(String(data));

});

compile.stderr.on('data', function (data) {
    console.log(String(data));
});


compile.on('close', function (data) {
    if (data === 0) {

        var run = spawn('java', ['-cp', 'static/temp_files/JavaTest', 'Temp']);

        readStream.on('data', function (chunk) {
            input_data = chunk;
            run.stdin.write(String(input_data));
        });


        run.stdout.on('data', function (output) {
            console.log(String(output));

            writeStream.write(String(output), function () {
                console.log("Cikti dosyasina yazildi");
            })

            /*
            fs.writeFile(filePath, String(output), function (err) {
                if(err){
                    return console.log(err);
                }

                console.log("The file was saved!");
            });
            */


        });

        run.stderr.on('data', function (output) {
            console.log(String(output));
        });

        run.on('close', function (output) {
            console.log('stdout: ' + output);
        });
    }

    //outputFile.close();
});

