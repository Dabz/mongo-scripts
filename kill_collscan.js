function killCollscan() {
  cols = db.currentOp({"planSummary" : /^COLLSCAN/});
  cols.inprog.forEach(function(col) {
      printjson({kill: col.opid});
      db.killOp(col.opid)
    }
  );
}
