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
        self.start =[0, 0]
        self.step= 0
        self.enum_file = list()
        self.enum()
        self.facts()
        #self.end_points()
        self.next_start()


    def enum(self):
        data = open(self.filename)
        self.rows, self.cls, self.L, self.H = (map(int, data.readline().strip().split()))
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
        for i in range(self.rows):
            Pizza.CHECKING.append([0]*self.cls)
        return self.enum_file, self.rows, self.cls, self.L, self.H

    def facts(self):
        sol = list()
        sol.append([self.H, 1])
        sol.append([1, self.H])

        for i in range(2, self.H):
            if self.H % i == 0:
                sol.append([i, self.H / i])
        return sol

    def end_points(self):
        facts_list = self.facts()
        edges = list()
        for x, y in facts_list:
            edges.append([self.start[0] + x - 1, self.start[1] + y-1])
        return edges

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

    def compare_acc(self, edges):
        temp_areas = list()
        for i in edges:
            area = self.acc_sum.sr(self.start[0], self.start[1], i[0], i[1])
            temp_areas.append(area)

        while self.H in temp_areas:
            index = temp_areas.index(self.H)
            temp_areas.pop(index)
            edges.pop(index)

        return edges[temp_areas.index(max(temp_areas))]

    def next_start(self):

        if 0 in Pizza.CHECKING[self.step]:
            self.start[1]= Pizza.CHECKING[self.step].index(0) + self.start[1]
            self.start[0]=self.step
            return True
        else:
            self.step += 1
            if self.step >= self.rows:
                return False
            else:
                self.next_start()



def main():
    filename = 'small.in'
    pizza = Pizza(filename)
    pizza.set_piece(1,0,0,0,6)
    pizza.set_piece(1,1,0,5,0)
    pizza.next_start()
    print(pizza.start)
    print('hello')

if __name__ == "__main__":
    print('Starting...\n')
    main()
    print('End')
