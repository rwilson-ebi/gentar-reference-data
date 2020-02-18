import csv, sys, os, re

class MgiMrkPreProcessor:

    def __init__(self):
    
        self.file = sys.argv[1]
        self.pathname = os.path.dirname(self.file)
        self.basename = os.path.basename(self.file)
        self.filename = os.path.abspath(os.path.join(self.pathname,self.basename))
        
        self.pattern = re.compile("o")

        self.outputfilename = os.path.abspath(os.path.join(self.pathname,'Mrk_synonyms.txt'))

        self.data = []
        self.headings = ['MGI Accession ID','Chr','cM Position','genome coordinate start','genome coordinate end','strand','Marker Symbol','Status','Marker Name','Marker Type','Feature Type','Marker Synonyms (pipe-separated)']
        
        
    
    
    def testHeadings(self, row, headings):
        
        
        if row != headings:
            print('The headings of the spreadsheet have changed')
            print('Expected:')
            for index, elem in enumerate(headings):
                print(index, elem)
            print('')
            print('Found:')
            for indexF, elemF in enumerate(row):
                print(indexF, elemF)
            print('')
            print('******************')
            sys.exit('Headers have changed')
    
    
    def readMrkFile(self):
        with open(self.filename, newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            try:
                counter=0
                for row in reader:
                    counter+=1
                    
                    # Ensure the expected columns are present
                    if counter == 1:
                    	self.testHeadings(row,self.headings)
                    
                    
                    # Load in the data rows, skipping the summary at the bottom
                    elif row[2]:
                        self.data.append(row)
                    
                    
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(self.filename, reader.line_num, e))
    
    # Only look for gene synonyms, avoid QTL synonyms
    def marker_type_match(self, marker_type):
    	if marker_type == 'Gene':
    		return True
    	elif marker_type == 'Complex/Cluster/Region':
    		return True
    	elif marker_type == 'DNA Segment':
    		return True
    	elif marker_type == 'Pseudogene':
    		return True
    	elif marker_type == 'Other Genome Feature':
    		return True
    	else:
    		return False
    	
    
    
    def writeMrkFile(self):
        with open(self.outputfilename, 'w') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            try:
                for row in self.data:
					if self.marker_type_match(row[9].strip()):
                    	synonyms = row[11].strip().split('|')
                    	for s in synonyms:
                        	synonym = s.strip()
                        	if synonym:
                            	id = row[0].strip()
                            	if id:
                                	writer.writerow([id,synonym])
                    
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(self.outputfilename, writer.line_num, e))
                

if __name__ == '__main__':
    l = MgiMrkPreProcessor()
    l.readMrkFile()
    l.writeMrkFile()
