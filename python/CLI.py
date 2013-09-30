#Axys Client File Object
#Platform  Python 2.5, Axys 3.6
#Author:  Joel Bondurant
#Date:  03/29/2007
from struct import *
import AxysCalendar
from Transactions import *

class CLIFile(object):
    'Axys Client File Object'
    
    def __init__(self, aFile, loadSettings = True):
        self.__file = aFile
        self.labels = {}
        self.transactions = []
        self.__labelOffset = 15
        self.__transactionOffset = 0
        if loadSettings:
            self.readSettings()

    def getTransactionOffset(self):
        return self.__transactionOffset
    
    transactionOffset = property(getTransactionOffset)
    
    def readLabels(self):
        f = self.__file
        f.seek(self.__labelOffset)
        skip = 7
        while True:
            labelName = f.read(8).rstrip('\x00')
            if len(labelName) == 0:
                self.__transactionOffset = f.tell()
                break
            if labelName[0] == '$':
                self.labels[labelName] = f.read(79-skip).rstrip('\x00')
                f.seek(f.tell() + skip)
            elif labelName[0] == '#':
                f.seek(f.tell() + 1)
                numStr = f.read(8)
                self.labels[labelName] = unpack('d',numStr)[0]
                f.seek(f.tell() + skip)
            elif labelName[0] == '%':
                dateStr = f.read(4)
                dateVal = unpack('L',dateStr)[0]
                self.labels[labelName] = AxysCalendar.getDate(dateVal)
                f.seek(f.tell() + skip)
            else:
                self.__transactionOffset = f.tell() - 8
                break

    def readSettings(self):
        self.readLabels()
        
    def printLabels(self):
        for label in self.labels.iteritems():
            print label
    
    def readTransactions(self):
        f = self.__file
        f.seek(self.__transactionOffset)
        while True:
            tranCode = f.read(3).lstrip('\x00').rstrip('\x00')
            if len(tranCode) == 0:
                break
            if tranCode == ';':
                tranBytes = f.read(84-3)
                #dateStr = tranBytes[4:9]
                #comment = tranBytes[9:]
                #tradeDate = unpack('L',dateStr)[0]
                #tran = CommentTransaction(tradeDate, comment)
                self.transactions.append(tranCode)
            elif tranCode == 'li':
                tranBytes = f.read(57-3)
                tran = LongInTransaction()
                self.transactions.append(tranCode)
            elif tranCode == 'by':
                tranBytes = f.read(134-3)
                self.transactions.append(tranCode)
            elif tranCode == 'sl':
                tranBytes = f.read(131-3)
                self.transactions.append(tranCode)
            elif tranCode == 'ti':
                tranBytes = f.read(86-3)
                self.transactions.append(tranCode)
            else:
                break
                
    def printTransactions(self):
        for tran in self.transactions:
            print tran