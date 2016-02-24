function updateProfil(collectionSrc,collectionDest, threadNumber, totalNumberOfThread) {
	 log ("Starting updating: " + collectionDest);
	 var bulk   = db[collectionDest].initializeUnorderedBulkOp();
   var cursor = db[collectionSrc].find({_id: {$mod: [totalNumberOfThread, threadNumber]}}).batchSize(10000);
   var i      = 0;
   res        = [];
   while (cursor.hasNext())
	 {
     var my_doc      = cursor.next();
		 var updates     = {};
		 updates["data"] = my_doc.data
		 bulk.find({_id: my_doc._id}).update({ $set: updates });
     i += 1;

     if ((i % 10000) == 0) {
       res.push(bulk.execute());
       var bulk = db[collectionDest].initializeUnorderedBulkOp();
     }
	 }

   res.push(bulk.execute());
   log ("Finished");
}

function throwErr(mssg){
    throw new Error(mssg);
}
