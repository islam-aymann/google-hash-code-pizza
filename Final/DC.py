# -*- coding: utf-8 -*-


class Server:
    def __init__(self, key, size, capacity):
        self.id = key
        self.size = size
        self.capacity = capacity
        self.capTsize = self.capacity / self.size
        self.capVsize = self.capacity * self.size
        self.row = int()
        self.slot = int()
        self.pool = int()

    def getSize(self):
        return self.size

    def getCap(self):
        return self.capacity

    def getcapTsize(self):
        return self.capTsize

    def getcapVsize(self):
        return self.capVsize

    def get_row(self):
        return self.row

    def get_slot(self):
        return self.row

    def set_slot(self, value):
        self.slot = value

    def set_row(self, value):
        self.row = value
    
    def __lt__(self,other):
        return self.getCap() < other.getCap()

    def __str__(self):
        return "Server: " + str(self.id) + "," + "Cap: " + str(self.capacity) + "," + "size: " + str(self.size)

class Row(object):
    def __init__(self, number):
        self.id = number
        self.cap = int()
        self.servers = list()

    def get_cap(self):
        row_sum =0
        for server in self.servers:
            row_sum += server.getCap()
        return row_sum

    def __str__(self):
        return "Row: " + str(self.id) + ", Cap: " + str(self.get_cap())

    def __lt__(self,other):
        return self.get_cap() < other.get_cap()
    
class Pool(object):
    def __init__(self,number):
        self.id = number
        self.cap =int()
        self.servers =list()

    def get_cap(self):
        row_sum =0
        for server in self.servers:
            row_sum += server.getCap()
        return row_sum
 
    def __str__(self):
        return "Pool: " + str(self.id) + ", Cap: " + str(self.get_cap()) + "no of servers :"+str(len(self.servers))

    def __lt__(self,other):
        return self.get_cap() < other.get_cap()

class DataCenter:
    def __init__(self, ):
        self.checking = list()
        self.un_slots = list()
        self.servers = list()
        self.row_objects = list()
        self.used_severs = list()
        self.pool_objects =list()
        self.row_no = 5

    def set_piece(self, setter, row, y1, y2):
        for j in range(y1, y2 + 1):
#            print("row: " + str(row)+" Col:"+str(j))
            self.checking[row][j] = setter
        return True

    def readFile(self):
        data = open("dc.in")
        self.rows, self.slots, self.slots_Un, self.pools, self.numb_servers = (
            map(int, data.readline().strip().split()))
        
        for i in range(self.pools):
            new_pool = Pool(i)
            self.pool_objects.append(new_pool)

        for i in range(self.rows):
            self.checking.append([-1] * (self.slots + 1))
            new_row = Row(i)
            self.row_objects.append(new_row)

        for i in range(self.slots_Un):
            xy = list(map(int, data.readline().strip().split()))
            self.set_piece(-2, xy[0], xy[1], xy[1])
            self.un_slots.append(xy)

        for i in range(self.numb_servers):
            size, capacity = map(int, data.readline().strip().split())
            new_server = Server(i, size, capacity)
            self.servers.append(new_server)
        data.close()

    def sort(self, key, rev=True):
        return sorted(self.servers, key=key, reverse=rev)

    def put_servers(self):
        self.cap_sorted_servers = self.sort(Server.getCap)

        for row in range(self.rows):
            start = self.checking[row].index(-1)
            for server in self.cap_sorted_servers:
                end = start + server.getSize()
                if -2 in self.checking[row][start:end]:
                    continue
                else:
                    self.set_piece(server.id, row, start, end-1)
                    pop_index = self.cap_sorted_servers.index(server)
                    self.used_severs.append(self.cap_sorted_servers.pop(pop_index))
                    self.row_objects[row].servers.append(server)
                    break
        self.sorted_rows = sorted(self.row_objects, key=Row.get_cap, reverse=True)

    def put_servers_fair(self):

        if not self.sorted_rows:
            return
        max_row = max(self.sorted_rows)
        min_row = min(self.sorted_rows)

        try:
#            print('b')
            free = self.checking[min_row.id].index(-1)
        except ValueError:
            row_index = self.sorted_rows.index(min_row)
            self.sorted_rows.pop(row_index)
            self.put_servers_fair()
            return

        while min_row.get_cap() < max_row.get_cap():
            try:
#                print('a')
#                print(len(self.cap_sorted_servers))
                start = self.checking[min_row.id].index(-1)
                
            except ValueError:
                break
            for server in self.cap_sorted_servers:
                end = start + server.getSize()
                if end > self.slots+1:
#                    print("out")
#                    print(end)
                    continue
                if -2 in self.checking[min_row.id][start:end]:
                    continue
                else:
#                    print(str(start)+"----------"+str(end))
                    self.set_piece(server.id, min_row.id, start, end-1)
                    pop_index = self.cap_sorted_servers.index(server)
                    self.used_severs.append(self.cap_sorted_servers.pop(pop_index))
                    self.row_objects[min_row.id].servers.append(server)
                    break
        self.put_servers_fair()
        return



    def build_row_matrix(self):
        self.row_matrix = list()
        for i in  self.row_objects:
            self.row_matrix.append(i.servers)
            
    def assign_pools(self):
        row = 0
        server_index = 0
        for i in range(self.pools):
            server = self.row_matrix[row][server_index]
            self.pool_objects[i].servers.append(server)
            self.row_matrix[row].pop(server_index)
            
            if row == self.rows-1:
                row =0                
            else:
                row +=1


    def assign_pools_fair(self):
        if not self.row_matrix:
            return
        
        max_pool = max(self.pool_objects)
        min_pool = min(self.pool_objects)
        
#        print("min bf: " + str(min_pool.get_cap())+"max bf: " + str(max_pool.get_cap()))
        while min_pool.get_cap() < max_pool.get_cap():
            try:               
                server = min(self.row_matrix[self.row_no])
            except:
#                print(self.row_no)
                self.row_matrix.pop(self.row_no)
                self.rows -=1
                self.row_no -=1
                self.assign_pools_fair()
                return
                
            min_pool.servers.append(server)
            self.row_matrix[self.row_no].pop(self.row_matrix[self.row_no].index(server))
            
            if self.row_no == self.rows-1:
                self.row_no =0                
            else:
                self.row_no +=1
#        print("min af: " + str(min_pool.get_cap())+"max af: " + str(max_pool.get_cap()))
        
        self.assign_pools_fair()
        return
                
#        self.sorted_pools = sorted(self.pool_objects, key=Pool.get_cap, reverse=True)
    
#    def assign_pools_fair(self):
#        if not self.row_matrix:
#            return
#        row = 0
#        server_index = 0
#        max_pool = max(self.pool_objects)
#        min_pool = min(self.pool_objects)
#        
#        print("min bf: " + str(min_pool.get_cap())+"max bf: " + str(max_pool.get_cap()))
#        while min_pool.get_cap() < max_pool.get_cap():
#            try:               
#                server = self.row_matrix[row][0]
#            except:
##                print(row)
#                self.row_matrix.pop(row)
#                self.rows -=1
#                self.assign_pools_fair()
#                return
#                
#            min_pool.servers.append(server)
#            self.row_matrix[row].pop(server_index)
#            
#            if row == self.rows-1:
#                row =0                
#            else:
#                row +=1
#        print("min af: " + str(min_pool.get_cap())+"max af: " + str(max_pool.get_cap()))
#        
#        self.assign_pools_fair()
#        return

            
            
        
    



    
        
def main():
    data_center = DataCenter()
    data_center.readFile()
#    print(data_center.slots)
    data_center.put_servers()
    data_center.put_servers_fair()
#    print(data_center.checking)
#    for i in data_center.cap_sorted_servers:
#        print(i)
        
    for i in  data_center.row_objects:
        print(i)
        
    data_center.build_row_matrix()
    data_center.assign_pools()
    data_center.assign_pools_fair()
    
    for i in data_center.pool_objects:
        print(i)

if __name__ == '__main__':
    main()
