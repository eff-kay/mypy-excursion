##stub example to be placed inside db.provenance
def find_one(param)->Union[None, dict]:  ...

class MongoRepository(object):
    def byLocation(self, locationString):
        record:Union[None, dict] = self.db.provenance.find_one({'location':locationString})
        
        # inconsistent annotation 
        # record:dict = self.db.provenance.find_one({'location':locationString}) 
        return self.inflate(record)
    
    def inflate(self, record:dict):
        if 'duration' in record: 
            ...