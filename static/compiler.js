
var spawn = require('child_process').spawn;
var compile = spawn('gcc', ['static/temp_files/temp.c']);
var fs = require('fs');

var inputFilePath = "static/data_files/input.txt";
var filePath = "static/data_files/output.txt";

var readStream = fs.createReadStream(inputFilePath, 'utf-8');


compile.stdout.on('data', function (data) {
    console.log(String(data));
});

compile.stderr.on('data', function (data) {
    console.log(String(data));
});


compile.on('close', function (data) {
    if (data === 0) {
        var run = spawn('./a.exe', []);


        readStream.on('data', function (chunk) {
            run.stdin.write(String(chunk));
        });

        run.stdout.on('data', function (output) {
            console.log(String(output));

            fs.writeFile(filePath, String(output), function (err) {
                if(err){
                    return console.log(err);
                }

                console.log("The file was saved!");
            });
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

