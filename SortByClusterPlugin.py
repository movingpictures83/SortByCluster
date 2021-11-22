import PyPluMA

def fixName(name):
    contents = name[1:len(name)-1].split(';')
    for i in range(len(contents)):
        if (len(contents[i]) > 3 and contents[i] != "Other"):
            contents[i] = contents[i][3:]
        else:
            contents[i] = ''
    for i in range(len(contents)-1, 0, -1):
        if (contents[i] != "Other" and contents[i] != ''):
            if (i != 6):
               return '\"' + contents[i].replace('[','').replace(']','') + '\"'
            else:
               return '\"' + contents[5].replace('[','').replace(']','') + ' ' + contents[6].replace('[','').replace(']','') + '\"'

class SortByClusterPlugin:
    def input(self, infile):
       parameterfile = open(infile, 'r')
       self.parameters = dict()
       for line in parameterfile:
           contents = line.strip().split('\t')
           self.parameters[contents[0]] = contents[1]
       network = open(PyPluMA.prefix()+"/"+self.parameters["network"], 'r')
       clusters = open(PyPluMA.prefix()+"/"+self.parameters["clusters"], 'r')

       # Read Network File
       self.nodes = network.readline().strip().split(',') # Header
       if (self.nodes[0] == '\"\"'):  # Remove padding if applicable
           self.nodes = self.nodes[1:]
       self.origADJ = []
       self.N = len(self.nodes)
       for line in network:
           contents = line.strip().split(',')
           contents = contents[1:] # Remove column name
           self.origADJ.append(contents)

       # Read Cluster File
       # Get Node Order
       self.clusternodes = []
       for line in clusters:
           if (not line.startswith('\"\"')): # Breaker
              contents = line.strip().split(',')
              self.clusternodes.append(contents[1])
              

    def run(self):
        # Create a new adjaceny matrix size MxM, where M is the # of cluster nodes
        self.newADJ = []
        self.M = len(self.clusternodes)
        for i in range(self.M):
            self.newADJ.append([])
            for j in range(self.M):
                node1 = self.clusternodes[i]
                node2 = self.clusternodes[j]
                idx1 = self.nodes.index(node1)
                idx2 = self.nodes.index(node2)
                self.newADJ[i].append(self.origADJ[idx1][idx2])

    def output(self, outfile):
        clusternetwork = open(outfile, 'w')
        #clusternetwork.write('\"\",')  # Pad
        for i in range(self.M):
            clusternetwork.write(fixName(self.clusternodes[i]))
            if (i != self.M-1):
                clusternetwork.write(',')
            else:
                clusternetwork.write('\n')

        for i in range(self.M):
            clusternetwork.write(fixName(self.clusternodes[i])+',')
            for j in range(self.M):
                clusternetwork.write(self.newADJ[i][j])
                if (j != self.M-1):
                    clusternetwork.write(',')
                else:
                    clusternetwork.write('\n')
