var fs = require("fs");
var file =  "nodedb.db";
var exists = fs.existsSync(file);

if(!exists) {
    // If the db does not exist, we are hosed.
    console.log("Database file is missing");
    exit();
}

var sqlite3 = require("sqlite3").verbose();
var express = require("express");
var app = express();

// Get info for all subscribers.
app.get("/subscriber/", function(req,res) {
	var db = new sqlite3.Database(file);
	res.setHeader('Content-Type','application/json');
	db.all("select * from table_subscriber", function(err, row) {
		if(err) {
			console.error(err);
			res.statusCode = 500;
			res.send({
				result: 'error',
				err: err.code
			});
            throw err;
		}
		res.statusCode = 200;
		res.send({
			result: 'success',
			err: '',
			json: row
		});
	});
	db.close();
});

// Get config info for a particular node.
// If the nodeid is bogus, an empty result set is returned.
app.get("/nodeconfig/:nodeid", function(req,res) {
        var db = new sqlite3.Database(file);
        res.setHeader('Content-Type','application/json');
        var stmt = db.prepare("select * from table_node_configuration where nodeid=? order by nodeID desc");
        stmt.all(req.params.nodeid, function(err, row) {
                if(err) {
                console.error(err);
                res.statusCode = 500;
                res.send({
                         result: 'error',
                         err: err.code
                         });
                }
                res.statusCode = 200;
                res.send({
                         result: 'success',
                         err: '',
                         json: row
                         });
                });
        stmt.finalize();
        db.close();
        });

// Get sensory data for a particular node.
// If the nodeid is bogus, an empty result set is returned.
app.get("/sensorydata/:nodeid", function(req,res) {
        var db = new sqlite3.Database(file);
        res.setHeader('Content-Type','application/json');
        var stmt = db.prepare("select * from table_sensory_data where nodeid = ? order by timestamp desc limit 1");
        stmt.all(req.params.nodeid, function(err, row) {
               if(err) {
               console.error(err);
               res.statusCode = 500;
               res.send({
                        result: 'error',
                        err: err.code
                        });
               }
               res.statusCode = 200;
               res.send({
                        result: 'success',
                        err: '',
                        json: row
                        });
               });
        stmt.finalize();
        db.close();
        });


app.listen(3000);
console.log("listening on port 3000");
