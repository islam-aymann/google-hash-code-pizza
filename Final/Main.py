# -*- coding: utf-8 -*-
class sumRange:
    def __init__(self, A=list()):
        self.A = A
        self.s = []
        self.x = []
        self.t = []
        

    def cumSum(self):
        if type(self.A[0]) == list:
            self.s = []
            self.t = []
            self.z = [0] * len(self.A[0])
            # turn into zero based
            self.A.insert(0, self.z)
            for i in range(len(self.A)):
                self.A[i].insert(0, 0)
            for i in range(len(self.A)):
                for j in range(len(self.A[i])):
                    if j == 0:
                        self.t.append(self.A[i][j])
                    else:
                        self.t.append(self.A[i][j] + self.t[j - 1])
                self.s.append(self.t)
                self.t = []

            self.s = list(map(list, zip(*self.s)))
            self.x = self.s
            self.s = []

            for i in range(len(self.x)):
                for j in range(len(self.x[i])):
                    if j == 0:
                        self.t.append(self.x[i][j])
                    else:
                        self.t.append(self.x[i][j] + self.t[j - 1])
                self.s.append(self.t)
                self.t = []
            self.s = list(map(list, zip(*self.s)))
            return self.s

        else:
            self.s = []
            for i in range(len(self.A)):
                if i == 0:
                    self.s.append(self.A[i])
                else:
                    self.s.append(self.s[i - 1] + self.A[i])
            return self.s

    def getS(self):
        return self.s

    def sr(self, i, j, k=0, l=0):
        if type(self.A[0]) == list:
            i += 1
            j += 1
            k += 1
            l += 1

            A = self.s[i - 1][j - 1]
            B = self.s[i - 1][l]
            D = self.s[k][j - 1]
            C = self.s[k][l]
            return C - B - D + A
        else:
            if i == 0:
                return self.s[i]
            else:
                return self.s[j] - self.s[i - 1]


class Pizza():
    def __init__(self,filename):
        self.filename = filename
        self.rows = int()
        self.cls = int()
        self.L = int()
        self.H = int()
        self.maxCells = int()
        self.checking = list()
        self.enum_file=list()
        self.step= 0
    def printM(self,x):
        for i in x:
            print(i)
    def enum(self):
        data = open(self.filename)
        self.rows, self.cls, self.L, self.H = (map(int, data.readline().strip().split()))
        self.rows -=1
        self.cls -=1
        for line in data.readlines():
            self.st = list(str(line.strip()))
            print(self.st)
            self.enum_file.append(self.st)
            for i in range(len(self.enum_file)):
                for j in range(len(self.enum_file[i])):
                    if self.enum_file[i][j] == 'T':
                        self.enum_file[i][j] = 1
                    elif self.enum_file[i][j] == 'M':
                        self.enum_file[i][j] = -1
        data.close()
        # Generating the chekcing Matrix
        for i in range(self.rows+1):
            self.checking.append([0]*(self.cls+1))
#        self.printM(self.enum_file)
    def facts(self):
        sol = list()
        sol.append([self.maxCells, 1])
        sol.append([1, self.maxCells])

        for i in range(2, self.maxCells):
            if self.maxCells % i == 0:
                sol.append([i, self.maxCells / i])
        return sol
    
    def nextStart(self):
        print(self.step)
        #there is a cell that could be the new start for a new slice
        if 0 in self.checking[self.step]:
            #update the start after checking if the new slice overlaps with the last ones         
            self.start[1]= self.checking[self.step].index(0)
            self.start[0]=self.step #update the current row
            return self.start
        
        else:
            self.step += 1
            if self.step > self.rows:
                self.start = False
                return False # pizza has been finished 
            else:
                self.nextStart() # search for the cell that could start from it without overlap


    

    def end_points(self):
        facts_list = self.facts()
        edges = list()
        for x, y in facts_list:
            edges.append([self.start[0] + x - 1, self.start[1] + y-1])
            
        self.endPoints = edges
        print(self.endPoints)
        print(self.cls)
        self.checkEdge()
        print(self.endPoints)
#        print("HEre" + " " +str(self.endPoints))
        if len(self.endPoints) == 0:
            self.maxCells = self.maxCells - 1
            if self.maxCells >= self.minCells:
                self.end_points()
                
                
            else:
                self.checking[self.start[0]][self.start[1]]=2
                self.start = self.nextStart()
                return
            return
        
        if self.start != self.temp:
            return  
#        self.printM(self.enumFile.getS())
        self.temp_areas = list()
        remove_in = list()
        for i in self.endPoints:
            area = self.enumFile.sr(self.start[0], self.start[1], i[0], i[1])
            self.temp_areas.append(area)
        # all tomatoos condition   
        self.temp_areas_abs = list(map(abs,self.temp_areas))

        # All Tomattos Condition
#        print("la2 la2a" + str(self.temp_areas_abs))
        while self.maxCells in self.temp_areas_abs:
            index = self.temp_areas_abs.index(self.maxCells)
            self.temp_areas.pop(index)
            self.temp_areas_abs.pop(index)
            self.endPoints.pop(index)
#        print("we" + str(self.endPoints))            
#        print("area" + str(self.temp_areas_abs)) 
#        print("start" + str(self.start))
        # range l condition
        print("endPoints " + str(self.endPoints))
        print("Max "+ str(self.maxCells))
        print("Min "+ str(self.minCells))
        if len(self.endPoints) == 0:
            self.maxCells = self.maxCells - 1
            if self.maxCells >= self.minCells:
                print("yes")
                self.end_points()
                print("out")
                return
            else:
                print("here")
                self.checking[self.start[0]][self.start[1]]=2
                self.start = self.nextStart()
                self.printM(self.checking)
                print(self.start)
                return
        print("start = " + str(self.start) + "Temp " + str(self.temp))
        if self.start != self.temp:
            return          
        k =0
        for i in self.temp_areas_abs:
            if i > (self.maxCells-self.minCells):
                remove_in.append(k)
            k = k+1
        for i in sorted(remove_in,reverse=True):
            del self.temp_areas[i]
            del self.temp_areas_abs[i]
            del self.endPoints[i]
        
#        print("are" + str(self.endPoints))            
            
        while not self.overlapCondition():
            self.end_points()
            
#        maximum = self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))]
#        
#        # overlap Condition            
#        for i in range(self.start[0], self.maximum[0]+1):
#                for j in range(self.start[1], maximum[1]+1):
#                    if Pizza.CHECKING[i][j] == 1:
                        
                    
        if len(self.endPoints)>0:       
            return(self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))])
        else:
            return False                            
        return
     
    def checkEdge(self):
        remove_in=list()
        k=0
        for i in self.endPoints:            
            if i[0] > (self.rows) or i[1] > (self.cls):
                remove_in.append(k)
            k = k+1
#                self.endPoints.remove(i)
#        print(remove_in)
        for i in sorted(remove_in,reverse=True):
            del self.endPoints[i]
    def overlapCondition(self):
        maximum = self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))]
        print(maximum)
        # overlap Condition
        for i in range(self.start[0], maximum[0]+1):
                for j in range(self.start[1], maximum[1]+1):
                    if self.checking[i][j] == 1:
                            if len(self.endPoints) == 0:
                                self.maxCells = self.maxCells - 1
                                return False
                            self.endPoints.pop(self.endPoints.index(maximum))
                            self.temp_areas_abs.pop(self.endPoints.index(maximum))
                            self.overlapCondition()
                            
                    else:
                        return True
    
#    def compare_areas(self):
#        temp_areas = list()
#        remove_in = list()
#        for i in self.endPoints:
#            area = self.enumFile.sr(self.start[0], self.start[1], i[0], i[1])
#            self.temp_areas.append(area)
#        # all tomatoos condition   
#        self.temp_areas_abs = list(map(abs,temp_areas))
#        # All Tomattos Condition
#        while self.maxCells in self.temp_areas_abs:
#            index = self.temp_areas_abs.index(self.maxCells)
#            self.temp_areas.pop(index)
#            self.temp_areas_abs.pop(index)
#            self.endPoints.pop(index)
#            
#        # range l condition
#        k =0
#        for i in self.temp_areas_abs:
#            if i > (self.maxCells-self.minCells):
#                remove_in.append(k)
#            k = k+1
#        for i in sorted(remove_in,reverse=True):
#            del temp_areas[i]
#            del self.temp_areas_abs[i]
#            del self.endPoints[i]
#        
#        
#        while not self.overlapCondition():
#            self.end_points()
#            
##        maximum = self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))]
##        
##        # overlap Condition            
##        for i in range(self.start[0], self.maximum[0]+1):
##                for j in range(self.start[1], maximum[1]+1):
##                    if Pizza.CHECKING[i][j] == 1:
#                        
#                    
#        if len(self.endPoints)>0:       
#            return(self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))])
#        else:
#            return False
    
    def set_piece(self,setter, x1, y1, x2, y2):
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                self.checking[i][j] = setter
        return True
            
    def Area(self):
        self.temp = self.start[:]
        self.temp[0] = self.temp[0] + 1
        self.temp[0] = self.temp[0] - 1
        self.maxCells = self.H
        self.minCells = 2*self.L
        endshape = self.end_points()
        print("start  out = "+ str(self.start))
        print("temp =       " + str(self.temp))
        
        if self.start != self.temp:
            return     
        # that means it's the end of the file and there would be some holes
        if self.start == False:
            return
        
        if endshape == False:     
            self.checking[self.start[0]][self.start[1]]=2
            self.start = self.nextStart()
            return
        print(str(self.start) + " " + str(endshape))
        self.set_piece(1,self.start[0],self.start[1],endshape[0],endshape[1])
        self.printM(self.checking)
        print(self.nextStart())
        print(self.start)
        if self.start == False:
            return

        
                
        
    def start(self):
        self.start = [0,0]
        self.enum()
        self.enumFile = sumRange(self.enum_file)
        
        self.enumFile.getS()
        self.enumFile.cumSum()
        while self.start:
            self.Area()


def main():
    pizza = Pizza("small.in")
    pizza.start()
if __name__ == "__main__":
    main()
    
    