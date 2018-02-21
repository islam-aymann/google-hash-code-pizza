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
    def __init__(self, filename):
        self.filename = filename
        self.rows = int()
        self.cls = int()
        self.L = int()
        self.H = int()
        self.maxCells = int()
        self.checking = list()
        self.enum_file = list()
        self.step = 0
        self.slices = 0

    # Printing a Matrix in an organised way
    def printM(self, x):
        for i in x:
            print(i)

    # Printing a large Matrix to a file called OUT
    def printMF(self, x):
        file = open("out", "w")
        for i in x:
            file.write(str(i) + '\n')
        file.close()

    def set_piece(self, setter, x1, y1, x2, y2):
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.checking[i][j] = setter
        return True

    # In[1]:
    # Reading a Pizza File - Preparing the Checking Matrix
    def enum(self):
        data = open(self.filename)
        self.rows, self.cls, self.L, self.H = (map(int, data.readline().strip().split()))
        self.rows -= 1
        self.cls -= 1
        for line in data.readlines():
            self.st = list(str(line.strip()))
            #            print(self.st) #1
            self.enum_file.append(self.st)
            for i in range(len(self.enum_file)):
                for j in range(len(self.enum_file[i])):
                    if self.enum_file[i][j] == 'T':
                        self.enum_file[i][j] = 1
                    elif self.enum_file[i][j] == 'M':
                        self.enum_file[i][j] = -1
        data.close()
        # Generating the chekcing Matrix
        for i in range(self.rows + 1):
            self.checking.append([0] * (self.cls + 1))

    #        self.printM(self.enum_file)

    # In[1]:
    # Generating Factorials  for the Current Maximum no of Cells
    def facts(self):
        sol = list()
        sol.append([self.maxCells, 1])
        sol.append([1, self.maxCells])

        for i in range(2, self.maxCells):
            if self.maxCells % i == 0:
                sol.append([int(i), int(self.maxCells / i)])
        return sol

    # In[1]:
    # Checking if the Generated endPoints violate the edge
    def checkEdge(self):

        remove_in = list()  # list that will contain the indices to be removed
        k = 0  # initalise the index
        for i in self.endPoints:
            if i[0] > (self.rows) or i[1] > (self.cls):
                remove_in.append(k)
            k = k + 1

        # using this way to remove multiple indices
        for i in sorted(remove_in, reverse=True):
            del self.endPoints[i]

    # In[1]:
    # Overlap Condition :D
    def overlapCondition(self):
        # check if the chosen endPoint is overlaping with any other shape
        maximum = self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))]
        print("  maximum area endPoint " + str(maximum))
        # overlap Condition
        for i in range(self.start[0], maximum[0] + 1):
            for j in range(self.start[1], maximum[1] + 1):
                if self.checking[i][j] == 1:
                    if len(self.endPoints) == 0:
                        self.maxCells = self.maxCells - 1
                        return False
                    self.endPoints.pop(self.endPoints.index(maximum))
                    self.temp_areas_abs.pop(self.endPoints.index(maximum))
                    self.overlapCondition()

                else:
                    return True

    # In[1]:
    def nextStart(self):
        print("\n")
        print("inside nextstart()")
        print("step " + str(self.step))
        # there is a cell that could be the new start for a new slice
        if 0 in self.checking[self.step]:
            # update the start after checking if the new slice overlaps with the last ones
            print("index = " + str(self.checking[self.step].index(0)) + " " + str(self.step))
            self.start[1] = self.checking[self.step].index(0)
            self.start[0] = self.step  # update the current row
            print("start ind " + str(self.start))
            print("outside nextstart() no1")
            return self.start

        else:
            self.step += 1
            if self.step > self.rows:
                self.start = False
                print("outside nextstart() here")
                return False  # pizza has been finished
            else:
                self.nextStart()  # search for the cell that could start from it without overlap
                print("outside nextstart() la")
                return self.start

    # In[1]:
    def end_points(self):

        facts_list = self.facts()  # Getting the factoriasl for the current Max
        edges = list()

        for x, y in facts_list:  # Calculating the End Points for the current start
            edges.append([self.start[0] + x - 1, self.start[1] + y - 1])

        self.endPoints = edges  # List of End Points

        print("End Points bf Edge Checking " + str(self.endPoints))
        self.checkEdge()
        print("End Points Af Edge Checking " + str(self.endPoints))

        if len(self.endPoints) == 0:  # Checking if all End Points were violating the edge
            self.maxCells = self.maxCells - 1  # Decreasing the Max Cells/ Slice
            if self.maxCells >= self.minCells:  # making sure Max cells didn't go below the Min Cells
                self.end_points()
                return (self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))])

            else:  # means all allowed slices with different Max Cells violate the edge so we mark the current position and find another start
                self.checking[self.start[0]][self.start[1]] = 2
                self.start = self.nextStart()
                return
            return

        if self.start != self.temp:  # to see if the start was changed we return and start the outer while loop again
            return
        # In[1]:  #calculating Areas

        #        self.printM(self.enumFile.getS())
        self.temp_areas = list()
        for i in self.endPoints:
            area = self.enumFile.sr(self.start[0], self.start[1], i[0], i[1])
            self.temp_areas.append(area)
        self.temp_areas_abs = list(map(abs, self.temp_areas))

        # In[1]: # All Tomattos Condition
        print("\n")
        print("endPoints bf all T condition " + str(self.endPoints))

        #        print("la2 la2a" + str(self.temp_areas_abs))
        while self.maxCells in self.temp_areas_abs:
            index = self.temp_areas_abs.index(self.maxCells)
            self.temp_areas.pop(index)
            self.temp_areas_abs.pop(index)
            self.endPoints.pop(index)
        #        print("we" + str(self.endPoints))
        #        print("area" + str(self.temp_areas_abs))
        #        print("start" + str(self.start))
        print("endPoints af ll T condition " + str(self.endPoints))
        print("Max " + str(self.maxCells))
        print("Min " + str(self.minCells))

        if len(self.endPoints) == 0:  # checking if all slices were  "T" or "M"
            print("here")  # Mark the current cell and get the next start
            self.checking[self.start[0]][self.start[1]] = 2
            self.start = self.nextStart()
            #                self.printM(self.checking) #1
            print(self.start)
            return
        print("start = " + str(self.start) + "Temp " + str(self.temp))
        if self.start != self.temp:
            return

        # In[1]: # Range 0-->(MaxCells - MinCells) Condition

        remove_in = list()
        k = 0
        for i in self.temp_areas_abs:
            if i > (self.maxCells - self.minCells):
                remove_in.append(k)
            k = k + 1
        for i in sorted(remove_in, reverse=True):
            del self.temp_areas[i]
            del self.temp_areas_abs[i]
            del self.endPoints[i]

        self.printMF(self.checking)

        if len(
                self.endPoints) == 0:  # checking if all slices were not in the range / don't satisfy the min l condition per slice
            print("L Condition")
            self.checking[self.start[0]][self.start[1]] = 2  # Mark the current Cell and get the next start
            self.start = self.nextStart()
            #                self.printM(self.checking) #1
            print(self.start)
            return
        print("start = " + str(self.start) + "Temp " + str(self.temp))
        if self.start != self.temp:
            return

        # In[1]: OverLapCondition
        print("\n")
        print("EndPoints bf overlap  " + str(self.endPoints))
        while not self.overlapCondition():
            print("OV ---_________")
            self.end_points()
        # In[1]:
        print("OOOOOOOOOO")
        print("end points af ov " + str(self.endPoints))
        if len(self.endPoints) > 0:  # checking if all endPoints were clear and all areas are verified
            return (self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))])
        else:
            return False
        return (self.endPoints[self.temp_areas_abs.index(max(self.temp_areas_abs))])

    # In[1]:

    def Area(self):
        self.temp = self.start[:]  # make a deep Copy
        self.maxCells = self.H
        self.minCells = 2 * self.L

        self.endshape = self.end_points()
        print("start  out = " + str(self.start))
        print("temp =       " + str(self.temp))

        if self.start != self.temp:  # to restart the while Loop if we chosed anew start in end_points()
            return
            # that means it's the end of the file and there might be some holes
        if self.start == False:
            return

        if self.endshape == False:  # if all endPoints were not verified we chose another start
            self.checking[self.start[0]][self.start[1]] = 2
            self.start = self.nextStart()
            return
        print("shape= " + str(self.start) + " " + str(self.endshape))
        self.out.write(str(self.start[0]) + " " + str(self.start[1]) + " " + str(self.endshape[0]) + " " + str(
            self.endshape[1]) + "\n")
        self.slices += 1
        self.set_piece(1, self.start[0], self.start[1], self.endshape[0], self.endshape[1])
        #        self.printM(self.checking) #1
        print(self.nextStart())
        print(self.start)
        if self.start == False:
            return

    # In[1]:

    def start(self):
        self.start = [0, 0]
        self.enum()
        self.enumFile = sumRange(self.enum_file)
        self.enumFile.getS()
        self.enumFile.cumSum()

        self.out = open("medium", "a")
        while self.start:
            self.printMF(self.checking)
            print(" ---------------")
            print("|Start = " + str(self.start) + "|")
            print(" ---------------")
            self.Area()
            print("-----------------------------------------------\n")
        self.out.write(str(self.slices))
        self.out.close()


def main():
    pizza = Pizza("medium.in")
    pizza.start()


if __name__ == "__main__":
    main()
