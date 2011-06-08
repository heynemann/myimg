var sys = require('sys'),
    fs = require('fs'),
    less = require('less'),
    path = require('path');

var toCss = function(filePath) {
    return path.join(path.dirname(filePath), path.basename(filePath, '.less') + '.css');
};

var writeCssFile = function(filePath) {
    var lessContents = fs.readFileSync(filePath);
    fs.readFile(filePath, 'utf-8', function (err, data) {
        if (err) throw err;

        var cssFilePath = toCss(filePath);
        less.render(data, function (e, css) {
            fs.writeFile(cssFilePath, css, function(err) {
                if(err) {
                    sys.puts(err);
                } else {
                    sys.puts("The file " + cssFilePath + " was saved!");
                }
            });
        });
    });
};

var rootDir = path.join(__dirname, 'thumby', 'static', 'css');
sys.puts(rootDir);
fs.readdir(rootDir, function(err, files) {
    for (var i=0; i<files.length; i++) {
        var file = path.join(rootDir, files[i]);
        if (path.extname(file) == '.less') {
            sys.puts('Converting ' + file);
            writeCssFile(file);
        }
    }
});

