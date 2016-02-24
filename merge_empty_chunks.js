/*
 * Move & merge empty chunks from a collection
 * Invoke using mergeEmptyChunks("dbname", "collection", true|false)
 */
function mergeEmptyChunks(dbn, collection, verbose) {
  namespace = dbn + "." + collection
  configDB  = db.getSiblingDB('config')
  sh.stopBalancer()

  var version = configDB.getCollection("version").findOne();
  if (version == null) {
    printjson({ok: 0, message: "not a shard db"});
    return;
  }

  collectioninfo = configDB.collections.find({_id: namespace}).next();
  shardKey       = collectioninfo.key;
  cursor         = configDB.chunks.find({ "ns" : namespace}).sort({min : 1});
  queue          = []


  while (cursor.hasNext()) {
    chunk = cursor.next()

    datasize = db.getSisterDB(dbn).runCommand({dataSize: namespace, keyPattern: shardKey, min: chunk.min, max: chunk.max, estimate: true})
    count = datasize.numObjects
    verbose && printjson({chunk: chunk._id, count: count})

    /*
     * Merge the queued chunks if:
     * . the current chunk is not empty; or
     * . this is the last chunk of the collection
     */
    if (count != 0 || (!cursor.hasNext())) {
      if (queue.length > 0) {
        /* 1. moving all empty chunks to the dest shards */
        queue.forEach(function(qchunk) {
          if (chunk.shard !== qchunk.shard) {
            command = {moveChunk: namespace, bounds: [qchunk.min, qchunk.max], to: chunk.shard}
            printjson(command)
            printjson(db.getSiblingDB("admin").runCommand(command))
          }
        });
        /* 2. merging chunks */
        min = queue[0].min
        max = chunk.max
        command = {mergeChunks: namespace, bounds: [min, max]}
        printjson(command)
        printjson(db.getSiblingDB("admin").runCommand(command))
      }
      queue = []
    } else if (count == 0) {
      queue.push(chunk)
    }
  }

  sh.startBalancer()
}
