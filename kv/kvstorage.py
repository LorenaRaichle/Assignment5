from pysyncobj import SyncObj, SyncObjConf, replicated

class KVStorage(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        conf = SyncObjConf()
        super(KVStorage, self).__init__(selfAddress, partnerAddrs, conf)
        self.__data = {}

    @replicated
    def put(self, key, value):
        print("put key: ", key, " with value: ", value)
        #TODO: implement the Put operation, that sets the value of the key to be the provided value.
        self.__data[key] = value
        #self.sync()  # Trigger replication to other Raft servers

    @replicated        
    def append(self, key, value):
        print("append key: ", key, " with value: ", value)
        #TODO: implement the Append operation, that adds the provided value to the value of the key.
        current_values = self.__data.get(key, [])
        try:
            current_values.append(value)
            self.__data[key] = current_values
        except Exception:
            self.__data[key] = value
        #self.sync()  # Trigger replication to other Raft servers


    def get(self, key):
        print("get key: ", key)
        #TODO: implement the Get operation, that retrieves the value of the provided key.
        value = self.__data.get(key, None)
        print("value: ", value)
        return value
    def get_dumpfile(self):
        return self.dumpFile
