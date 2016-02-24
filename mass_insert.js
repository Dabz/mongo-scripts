function massInsert(collection) {
  db  = db.getSiblingDB("test")
  txt = ""

  for (i = 1; i < 100; i++) {
    txt = txt + i
  }

  bulk = []
  while (true) {
    bulk.push({createdAt: ISODate(), lng: txt.toString()})
    if (bulk.length >= 1000) {
      collection.insert(bulk, {ordered: false})
      bulk = []
    }
  }
}
