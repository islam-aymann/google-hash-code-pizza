# -*- coding: utf-8 -*-

class server:
    def __init__(self,key,size,capacity):
        self.id = key
        self.size = size
        self.capacity= capacity
        self.capTsize = self.capacity/self.size
        self.capVsize = self.capacity * self.size
    def getSize(self):
        return self.size
    def getCap(self):
        return self.capacity
    def capTsize(self):
        return self.capTsize
    def capVsize(self):
        return self.capVsize
    def __str__(self):
        return "Server: "+ str(self.id) + "," + "Cap: " + str(self.capacity) + "," + "size: " + str(self.size)  
    


class DataCenter:
    def __init__(self,):
        self.checking=list()
        
     
    def set_piece(self,setter, row, y1, y2):        
        for j in range(y1, y2+1):
            self.checking[row][j] = setter
        return True

    def readFile(self):
        data = open("dc.in")
        Un_slots_coo=list()
        self.servers=list()
        self.rows, self.slots, self.slots_Un, self.pools,self.numb_servers = (map(int, data.readline().strip().split()))
        for i in range(self.slots_Un):
            Un_slots_coo.append(list(map(int, data.readline().strip().split())))
           
        for i in range(self.numb_servers):            
            size,capacity=map(int, data.readline().strip().split())
            new_server=server(i,size,capacity)
            self.servers.append(new_server)
        data.close()
        
        for i in range(self.rows+1):
            self.checking.append([-1]*(self.slots+1))
            
    def sort(self,key,rev=True):
        return sorted(self.servers,key=key,reverse=rev)
    def put_servers(self):
        sortedLst=self.sort(server.getCap)
        print(sortedLst)
        row=0
        
        for server in sortedLst:    
            start=self.checking[row].index(-1)
            end=start+server.getSize
            self.set_piece(server.id,row,start,end)
            if row == self.rows:
                row=0
            row +=1
            
        
center=DataCenter()
center.readFile()
mysorted=center.sort(server.getCap)
center.put_servers()

#print(*mysorted)

    
    


        
