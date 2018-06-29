var spawn = require('child_process').spawn;
var compile = spawn('python', ['C:/Users/User/Desktop/temp.py']);
var fs = require('fs');
var inputFilePath = "C:\\Users\\User\\Desktop\\input.txt";
var filePath = "C:\\Users\\User\\Desktop\\output.txt";

var input_data = '';
var readStream = fs.createReadStream(inputFilePath, 'utf-8');
var writeStream = fs.createWriteStream(filePath);


//compile.stdin.write('4\n');

readStream.on('data', function (chunk) {
    input_data += chunk;
    compile.stdin.write(String(input_data));
});


compile.stdout.on('data', function (data) {
    //console.log(String(data));
    //compile.stdin.setEncoding = 'utf-8';

     writeStream.write(String(data), function () {
        //console.log("Cikti dosyasina yazildi");
     });

    /*
    fs.writeFile(filePath, String(data), function (err) {

        if(err){
            return console.log(err);
        }

        console.log("Dosya kaydedildi");
    });
    */

});

/*
readStream.on('data', function (chunk) {
    data += chunk;
    }).on('end', function () {
        compile.stdin.write(String(data));
        console.log('alperen');

    });
   */



compile.stderr.on('data', function (data) {
    console.log(String(data));

    writeStream.write(String(data), function () {
    });

});




/*
compile.on('close', function (data) {
    if (data === 0) {
        var run = spawn('./a.exe', []);

        run.stdout.on('data', function (output) {
            console.log(String(output));

            var filePath = "C:\\Users\\User\\Desktop\\output.txt";

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
*/