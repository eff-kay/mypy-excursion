class MongoRepository(object):
    def byLocation(self, locationString):
        record = self.db.provenance.find_one({'location':locationString})

### fix patch
#++     if record is None:
#++         self.listener.unknownFile('id: '+str(uid))
#++         return

        return self.inflate(record)

    def inflate(self, record):
        if 'duration' in record: 
            ...
