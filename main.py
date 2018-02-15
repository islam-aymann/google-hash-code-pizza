
class sumRange:
    def __init__(self, A=list()):
        self.A = A
        self.s = []
        self.x = []
        self.t = []
        self.cumSum()

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


class Pizza(object):
    VISITED = list()
    SLICES = list()
    CHECKING = list()

    def __init__(self, filename):
        self.filename = filename
        self.rows = int()
        self.cls = int()
        self.L = int()
        self.H = int()
        self.start =[0, 0] ####### e7na wa2afnaa henaaaaa
        self.step= 0
        self.enum_file = list()
        self.enum()
        self.edge_condition(self.end_points())
        
        
        
        self.MaxCells=int()
        self.acc_sum = int()
    
    """
    this method reads the input file and save the pizza into an array called "self.enum_file" 
    where -1 indicated that the cell have Machrom and 1 indicates Tomato
    it also creates another array called "self.CHECKING" which keep tracking of the chosen slices 
    having 1 for chossen slices and 0 for non chosen slices to prevent overlaping and for backtracking
    
    returns: :D
         self.enum_file
         self.rows: ​is the number of rows,
         self.cls: is the number of columns,
         self.L: ​is the minimum number of each ingredient cells in a slice,
         self.H: ​is the maximum total number of cells of a slice
    """
    def enum(self):
        data = open(self.filename)
        self.rows, self.cls, self.L, self.H = (map(int, data.readline().strip().split()))
        self.MaxCells= self.H #to keep tracking of the max number of slicing and starting minimizing it after each stucl
        for line in data.readlines():
            string = list(str(line.strip()))
            self.enum_file.append(string)
            for i in range(len(self.enum_file)):
                for j in range(len(self.enum_file[i])):
                    if self.enum_file[i][j] == 'T':
                        self.enum_file[i][j] = 1
                    elif self.enum_file[i][j] == 'M':
                        self.enum_file[i][j] = -1
        data.close()
        self.acc_sum = sumRange(self.enum_file)
        self.acc_sum.cumSum()
        #making a cheking Pizza for backtracking
        for i in range(self.rows):
            Pizza.CHECKING.append([0]*self.cls)
        return self.enum_file, self.rows, self.cls, self.L, self.H

"""
   returns a list of factorials for MaxCells 
   for example if MaxCells=6,  so it returns: [[2,3],[3,2],[6,1],[1,6]]
"""   
    def facts(self):
        
        sol = list()
        
        sol.append([self.MaxCells, 1])
        sol.append([1, self.MaxCells])

        for i in range(2, self.MaxCells):
            if self.MaxCells % i == 0:
                sol.append([i, self.MaxCells / i])
        return sol
"""
    returns alist id edges of each factorial
    each slice is rectangular and is defined by its diagonals,
    diagonals are (self.start) and each start with a different factorial have a different end which is the edge
"""
    def end_points(self):
        facts_list = self.facts()
        edges = list()
        for x, y in facts_list:
            edges.append([self.start[0] + x - 1, self.start[1] + y-1])
        return edges
"""
    this function checks if the indicated slice have been chosen or not and set or clear cells 
    in "self.CHECKING" array to prevent overlapping.
    arguments: 
        setter: could be 1 or 0,
                1 indicates that this slice have been chosen before, we can set an area to 1 and indicate that we want to cut it
                 but before that the code check ot we coull do that or not
                0 indicate that this slice has not been cutted, we can clear an area which is useful for backtracking
        diagonal points:
            (x1,y1): start point
            (x2,y2):end points
    returns:
        false: indicating that slices overlap
        true: when there's no overlaping and you have set or cleaed the chossen area
        
"""
    @staticmethod
    def set_piece(setter, x1, y1, x2, y2):
        if setter:
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    if Pizza.CHECKING[i][j] == 1:
                        return False

        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                Pizza.CHECKING[i][j] = setter
        return True
   """ 
   check if the current endpoints in the eadges list is out of the pizza boundaries (row and colums)
   and remove it from edges list
   also checks if no slices remainig in edge list : 
       it minimize the size of the slice (minimize "self.MaxCells")->get new factorials->check for edge again
   arguments:
       edges
   returns:
       edges after updating it
   """
    def edge_condition(self,edges):
        
       for i in edges:
           if i[0] > self.rows or i[1] > self.cls:
               edges.remove(i)
       if len(edges==0): 
           self.MaxCells=self.MaxCells-1 #minimize the size of the slice
           self.edge_condition(self.end_points())
       else:
           return edges
       
"""
    this function compute the sum of cells (1:Tomato, -1:Mashroom) (called area)
    in the choosen slice by its diagonal(start and endpoints in the edges list)
    argument: 
        edges: 
            list of end points
        return:
            the end=point having the maximun area which means the maximum of one ingredients with the minim of the other
            while sttisfing H and L conditions.
            Solving the local unbalance of ingredient.
    
"""
    def compare_acc(self, edges):
        temp_areas = list()
        
        for i in edges:             
            #compute areas
            area = self.acc_sum.sr(self.start[0], self.start[1], i[0], i[1])
            temp_areas.append(area)
        
        
        #stisfing H condition (delete any area having all T or all M)
        while self.MaxCells in temp_areas:
            index = temp_areas.index(self.MaxCells)
            temp_areas.pop(index)
            edges.pop(index)
        #stisfing L condition (delete any area having T or all M less than L)            
        while i in temp_areas:
            if abs(i) not in range(0,self.MaxCells-2*self.L):
                index = temp_areas.index(i)
                temp_areas.pop(index)
                edges.pop(index)  
        
        return edges[temp_areas.index(max(temp_areas))]
    """
    indicates the new start point for the new slice by checking the availble ones to prevent overlaping
    and update the new start point
    returns:
        true:
            when it succeed in making a new start
        flase:
            there's no slice that could take place in the current row ,
            so we step by one now from the old one and check again for a new start in that row
    """

    def next_start(self):
        
        #there is a cell that could be the new start for a new slice
        if 0 in Pizza.CHECKING[self.step]:
            #update the start after checking if the new slice overlaps with the last ones         
            self.start[1]= Pizza.CHECKING[self.step].index(0)
            self.start[0]=self.step #update the current row
            return True
        
        else:
            self.step += 1
            if self.step >= self.rows:
                return False # pizza has been finished 
            else:
                self.next_start() # search for the cell that could start from it without overlap
    


def main():
    filename = 'small.in'
    pizza = Pizza(filename)
#    pizza.set_piece(1,0,0,0,6)
#    pizza.set_piece(1,1,0,1,2)
#    pizza.next_start()
#    pizza.enum()
    print(Pizza.CHECKING)


if __name__ == "__main__":
    print('Starting...\n')
    main()
    print('End')