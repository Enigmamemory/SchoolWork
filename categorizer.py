import string
import math

categories = {}
catprob = {}
words = {}
wordcat = {}
wordcattotal = {}
wordprob = {}
wordmiss = {}

#trainname = 'corpus3_train.labels'
#testname = 'corpus3_test.list'

trainname = input("Enter training file: ")
testname = input("Enter testing file: ")

def catwords(alarray,cat):
    for word in alarray:
        #Seperate words into category dictionaries
        if wordcat[cat].get(word.lower()) == None:
            wordcat[cat].setdefault(word.lower(),1)
        else:
            wordcat[cat][word.lower()] = wordcat[cat][word.lower()] + 1

        #Seperate word totals into categories
        wordcattotal[cat] = wordcattotal[cat] + 1

        
        #Seperate words for inclusive dictionary
        if words.get(word.lower()) == None:
            words.setdefault(word.lower(),1)
        else:
            words[word.lower()] = words[word.lower()] + 1
        

def readart(art):
    #open the article and read lines
    article = open(art)
    #list of all words stored here
    alarray = []
    for aline in article:
        #remove punctuations and replace new lines, tabs with spaces
        translator = str.maketrans('','',string.punctuation)
        fixline1 = aline.replace('`','')
        fixline2 = aline.translate(translator)
        fixline = fixline2.replace('\n',' ')
        fixline = fixline.replace('\t',' ')        
        #split words
        alarray += fixline.split(" ")
    
    article.close()
    return alarray

def training(trainname):
    
    trainf = open(trainname)

    for line in trainf:
        
        #Take lines from input file and split them, stripping \n
        larray = line.split(" ")
        larray[1] = larray[1].strip('\n')

        #Add all necessary keys if they do not exist

        if categories.get(larray[1]) == None:
            categories.setdefault(larray[1], 1)
            empdict = {}
            empdict2 = {}
            wordcat.setdefault(larray[1],empdict)
            wordprob.setdefault(larray[1],empdict2)
            wordcattotal.setdefault(larray[1],0)
            catprob.setdefault(larray[1],0)
            wordmiss.setdefault(larray[1],0)
        else:
            #Count the number of articles in each category
            categories[larray[1]] = categories[larray[1]] + 1
        
        #Read article for words
        allwords = readart(larray[0])
        #Categorize words
        catwords(allwords,larray[1])
    
    for cat in wordcat:
        wordcat[cat].pop('',-1)
        wordcat[cat].pop('\t',-2)
        wordcat[cat].pop('\n',-3)
        wordprob[cat].pop('',-1)
        wordprob[cat].pop('\t',-2)
        wordprob[cat].pop('\n',-3)

    #words.pop('',-1)
    #words.pop('\t',-2)
    #words.pop('\n',-3)

    trainf.close()

def categoryprob():
    cattotal = 0
    for cat in categories:
        cattotal += categories[cat]
    #print(cattotal)
    for cat in catprob:
        catprob[cat] = math.log10(categories[cat] / cattotal)

def wordsprob():
    '''
    vocab = 0
    for cat in wordcattotal:
        vocab += wordcattotal[cat]
    '''
    for cat in wordcat:
        for word in wordcat[cat]:
            wordchance = math.log10((wordcat[cat][word] / wordcattotal[cat]))
            wordprob[cat].setdefault(word,wordchance)
            '''
            if wordcat[cat][word] > 200:
                print(cat)
                print(word)
                print(wordcat[cat][word])
                print(wordchance)
            '''
            #Create key for word probability in category for future use
 


def testword(words):
    vocab = 0
    for cat in wordcattotal:
        vocab += wordcattotal[cat]
    catscore = catprob.copy()
    for cat in catscore:
        for word in words:
            if wordprob[cat].get(word.lower()) == None:
                catscore[cat] += math.log10(1 / (wordcattotal[cat] + vocab))
                wordmiss[cat] += 1
            else:
                catscore[cat] += wordprob[cat][word.lower()]
    first = True
    largest = 0
    mostprob = ""
    #print(catscore)
    for cat in catscore:
        if first:
            largest = catscore[cat]
            mostprob = cat
            first = False
        else:
            if largest < catscore[cat]:
                largest = catscore[cat]
                mostprob = cat
    return mostprob

def testing(testname):
    
    testf = open(testname)
    results = ""
    testnum = 0
    
    for line in testf:
        '''
        if testnum == 10:
            break;
        '''
        pathname = line.strip('\n')
        allwords = readart(pathname)
        results += pathname + " " + testword(allwords) + "\n"
        testnum += 1

    writename = input("Enter output file name: ")
    writefile = open(writename,"w+")
    writefile.write(results)
    writefile.close()
    #print(results)
    
training(trainname)
categoryprob()
wordsprob()
testing(testname)

'''
print(catprob)
print(wordmiss)
print(wordcattotal)
'''




 
    
