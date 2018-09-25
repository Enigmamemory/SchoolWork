import nltk
import random
from nltk.corpus import wordnet as wn
from nltk.stem.porter import *
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

pastobj = ''
key = random.randint(0,4) #-1 for found, 0-4 for location. 0 = drawer, 1 = binder, 2 = cup, 3 = trash, 4 = stack
desknote = 0 #0 for not found, 1 for found
person = 0 #0-4 for location. 0 = door, 1 = desk, 2 = shelf, 3 = window, 4 = trash
water = 0 #0 for not found, 1 for found, 2 for boiled, 3 for used
noodle = 0 #0 for not found, 1 for found, 2 for cooked, 3 for eaten
fork = 0 #0 for not found, 1 for found
fed = 0 #0 for not fed, 1 for drinking water, 2 for fed

def commandparse(teststr):
    tokens = nltk.word_tokenize(teststr)
    POS = nltk.pos_tag(tokens)

    verbs = []
    nouns = []
    pronouns = []
    addi = True
    findit = False

    while (addi == True):

        verbs = []
        nouns = []
        pp = []
        pronouns = []
        
        for word,pos in POS:

            if (pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS' or pos == 'PRP' or pos == 'PRP$'):
                nouns.append(word)
                if (pos == 'PRP' or pos == 'PRP$'):
                    pronouns.append(word)
                    if word == 'it':
                        findit = True
            elif (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ'):
                verbs.append(word)
            elif (pos == 'RP' or pos == 'IN'):
                pp.append(word)

        addi = False
            
        if len(verbs) == 0:
            addi = True
            teststr = "I " + teststr
            tokens = nltk.word_tokenize(teststr)
            POS = nltk.pos_tag(tokens)


    print(POS)
    #print(nouns)
    #print(verbs)    

    #we will begin by assuming "I" is always the subject

    sub = "I"
    findobj = False #possible sentence "assumes" an object, like previous mentioned object
    obj = ""
    verb = ""

    stemmer = PorterStemmer()
    
    for noun in nouns:
        if noun != "I":
            obj = stemmer.stem(noun)
            if len(wn.synsets(obj,pos=wn.NOUN)) == 0:
                obj = noun
            print(obj)
            findobj = True
            break

    if findobj == False: #Currently cannot think of anything besides room that might be an "implicit" object
        obj = 'room' #Assume only reason to implicitly state an object is when referring to "room"
        nouns.append(obj)
        
    verb = verbs[0]

    outputs = {"subject" : sub, "object": obj, "verb": verb, "nouns": nouns, "prep": pp, "pronouns": pronouns}

    #possible want list of nouns to see if certain nouns are in sentence, grouping
    #also want a "previous nouns" list

    if findit == True:
        if pastobj != '':
            outputs["object"] = pastobj
        else:
            outputs["object"] = "room"
    
    return outputs

def guesswords(outputs):

    
    vb = outputs["verb"]
    obj = outputs["object"]

    '''
    vbcombo = {'observe':['observe','inspect','stare'],'leave':['leave','exit','depart'],'open':['open','unbar','unseal'],'walk':['walk','stroll','hike'],'hit':['hit','strike','smack'],'jump':['jump','leap','fall'],'read':['read','study','comprehend'], 'boil':['boil','steam','simmer'],'cook':['cook','prepare','make'],'take':['grab','acquire','take'],'lift':['lift','hoist','elevate'],'eat':['eat','bite','feed'], 'pull':['pull','drag','haul'], 'use':['use','utilize','operate'], 'kill':['kill','murder','assassinate'],'sleep':['sleep','relax','rest']}
    '''

    vbcombo = {'observe':['observe','look'],'exit':['exit','depart'],'open':['open','unseal'],'walk':['walk','stroll'],'hit':['hit','strike'],'jump':['jump','leap'],'study':['study','comprehend'], 'boil':['boil','steam'],'cook':['cook','prepare','make'],'grab':['grab','take'],'lift':['lift','haul'],'eat':['eat','feed'], 'pull':['pull','drag'], 'use':['use','utilize','operate'], 'kill':['kill','murder'],'sleep':['sleep','relax'],'push':['push','force']}

    '''
    objcombo = {'desk':['desk','table'],'chair':['chair','seat'],'door':['door','gateway'],'shelf':['shelf','cupboard'],'drawer':['drawer','drawers'],'trash':['trash','garbage'],'floor':['floor','ground'],'wall':['wall','surface'],'window':['window','porthole'],'cup':['cup','goblet'],'note':['note','document'],'noodle':['noodle','pasta'],'binder':['binder','folder'],'book':['book','novel'],'water':['water','drink'],'bottle':['bottle','jar'],'fork':['fork','utensil'],'paper':['paper','sheet'],'stack':['stack','pile'],'boiler':['kettle','boiler'],'key':['key','opener'],'room':['room','area']}
    '''
    
    objcombo = {'desk':['desk'],'chair':['chair'],'door':['door'],'shelf':['shelf'],'drawer':['drawer','drawers'],'trash':['trash'],'wall':['wall'],'window':['window'],'cup':['cup','mug'],'note':['note','document'],'noodle':['noodle'],'binder':['binder'],'book':['book'],'water':['water'],'canteen':['canteen'],'fork':['fork','utensil'],'paper':['paper','sheet'],'stack':['stack','pile'],'boiler':['kettle','boiler'],'key':['key','opener'],'room':['room'],'floor':['floor']}
    
    testset = wn.synsets(vb,pos=wn.VERB)
    testset2 = wn.synsets(obj,pos=wn.NOUN)
    testset3 = wn.synsets('grail',pos=wn.NOUN)
    
    #print(testset)
    #print(testset2[0].definition())
    #print(testset3[0].definition())
    
    maxvbsim = 0
    maxvbword = ''

    vcounttotal = 0
    ocounttotal = 0
    
    for vbs in vbcombo:
        thisvbsim = 1
        vcount = 0
        #print(vbs)
        for vb in vbcombo[vbs]:
            #print(vb)
            vbset = wn.synsets(vb,pos=wn.VERB)
            if len(vbset) == 0:
                print("Problem with finding synsets for the verb: " + vb)
                return 1
            #print(vbset)
            vbsim = vbset[0].path_similarity(testset[0])
            thisvbsim += vbsim
            vcount += 1
            vcounttotal += 1

        thisvbsim = thisvbsim / vcount
        #print(thisvbsim)
    
        if thisvbsim > maxvbsim:
            maxvbsim = thisvbsim
            maxvbword = vbs

    #print(maxvbsim)
    #print(maxvbword)

    '''
    testword = 'paper'
    testpn = wn.synsets(testword,pos=wn.NOUN)
    print(testpn[0].definition())
    '''
    maxobjsim = 0
    maxobjword = ''

    for objs in objcombo:
        thisobjsim = 1
        ocount = 0
        #print(objs)
        for obj in objcombo[objs]:
            #print(vb)
            objset = wn.synsets(objs,pos=wn.NOUN)
            if len(objset) == 0:
                print("Problem with finding synsets for the object: " + obj)
                return 1
            #print(vbset)
            objsim = objset[0].path_similarity(testset2[0])
            thisobjsim += objsim
            ocount += 1
            ocounttotal += 1

        thisobjsim = thisobjsim / ocount
        #print(thisobjsim)
    
        if thisobjsim > maxobjsim:
            maxobjsim = thisobjsim
            maxobjword = objs

    #print(maxobjsim)
    #print(maxobjword)

    #print(maxvbword,maxobjword)
    #print(maxvbsim,maxobjsim)

    #print(vcounttotal,ocounttotal)

    return {'words':[maxvbword,maxobjword],'sims':[maxvbsim,maxobjsim]}

#################################################Game Statements###############################################

#threshold at 0.7? ok

def interpretguess(guesses):

    global key
    global desknote
    global person
    global water
    global noodle
    global fork
    global fed
    
    if (guesses['sims'][0] < 0.7 and guesses['sims'][1] < 0.7):
        print("You have no idea how this idea popped in your mind. Probably just too tired.")
    elif (guesses['sims'][0] < 0.7):
        print("You think about it and decide maybe that's a bad idea.")
    elif (guesses['sims'][1] < 0.7):
        print("There doesn't seem to be anything resembling that in this room. You might be hallucinating.")
    else:
        #print("Possible pair?")

        #exit#
        
        if guesses['words'][0] == 'exit':
            if guesses['words'][1] == 'door' or guesses['words'][1] == 'room':
                if key >= 0:
                    print("That door isn't unlocking itself, you know. No amount of testing will change that. Better find that key. Stupid employee.")
                    person = 0
                else:
                    print('Free at last.')
                    return 1
            elif guesses['words'][1] == 'window':
                print('Your office is on the fifth floor. Walking home will be difficult if your legs, among other things, are broken. You reconsider that plan.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't.")

        #open#            
        if guesses['words'][0] == 'open':
            if guesses['words'][1] == 'door': #depends on whether or not you have key
                if key >= 0:
                    person = 0
                    print('You try to open the door. What do you know, it is still locked. Shocker.')
                else:
                    print("With the key, you unlock the door and step towards your newfound freedom. Score.")
                    return 1

            elif guesses['words'][1] == 'window':
                print('You open the window just enough to get some fresh air. Not really helpful, but at least it feels nice.')
            elif guesses['words'][1] == 'note':
                if person == 0 or desknote == 0:
                    person = 0
                    print('You read the note at the wall. It reads:') #door note
                    print('''
"Hey, you look like you need some fun in your life. So I made a small Escape the Room scenario. I hid the key somewhere in the room, good luck finding it!"

Hold up, there is another, smaller line of text that you missed previously. It says:

"P.S: If you really want to leave though, read the note on the desk."
'''
                      )
                    desknote = 1
                elif person == 1:
                    print('You open the note on the desk. It reads:') #desk note
                    if key == 0:
                        print("Key is hidden in a drawer")
                    elif key == 1:
                        print("Key is hidden in a binder")
                    elif key == 2:
                        print("Key is hidden in the cup")
                    elif key == 3:
                        print("Key is hidden in the trash")
                    else:
                        print("Key is hidden in the stack of papers")
 

                else:
                    print('There are multiple notes in this room. You should move towards the location of the one you want')
                    
            elif guesses['words'][1] == 'drawer':
                person = 1
                print('You open the drawers. There are mostly papers, but one drawer actually had one cup noodle. Now you have something to eat') #need description of what's in drawer
                noodle = 1
                if key == 0:
                    print('After some thorough searching, you managed to find the key. Now you can get out of here.')
                    key = -1

            elif guesses['words'][1] == 'book':
                person = 2
                print('You try opening some of those books and, looking at the number of books in your shelf, give up. If the key is in one of them, then you are going to stay the night.')

            elif guesses['words'][1] == 'binder':
                person = 2
                if key == 1:
                    print("You flip through the binders. The key was hidden in one of them. Very nice.")
                    key = -1
                else:
                    print("You flip through all the binders and succeeded in creating a disorderly pile of binders.")
                
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")

        #walk#

        if guesses['words'][0] == 'walk': #If already at location, need to point out. Also need to put before location change method
            if guesses['words'][1] == 'door' or guesses['words'][1] == 'room': #depends on whether or not you have key
                if person == 0:
                    print('You are right next to the door, so walking there feels a bit silly.')
                if key >= 0:
                    person = 0
                    print('You walk to the door. It is still stubbornly shut, which is disappointing.')
                else:
                    print('With the key in hand, you walk to the door, unlock it, and get the heck out of here. Good night')
                    return 1
            elif guesses['words'][1] == 'window':
                if person == 3:
                    print('You are right next to the window, so walking there feels a bit silly.')
                person = 3
                print('You walk to the window. It looks quite dark out.')
            elif guesses['words'][1] == 'desk' or guesses['words'][1] == 'chair':
                if person == 1:
                    print('You are right next to the desk, so walking there feels a bit silly.')
                person = 1
                print('You walk to the desk and the chair. Maybe something helpful is here.')
            elif guesses['words'][1] == 'trash':
                if person == 4:
                    print('You are right next to the trash, so walking there feels a bit silly.')
                person = 4
                print('You walk to the trash. You wonder if your dignity can take dumpster diving. You also wonder if your diginity matters if no one is around.')
            elif guesses['words'][1] == 'shelf':
                if person == 2:
                    print('You are right next to the shelf, so walking there feels a bit silly.')
                person = 2
                print('You walk to the shelf. Perhaps you can find something useful.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #hit#

        if guesses['words'][0] == 'hit':
            if guesses['words'][1] == 'door' or guesses['words'][1] == 'wall':
                person = 0
                print('You raise a ruckus by abusing the doors and walls. Either no one is around, or anyone around does not care. In any case, you got to vent your feelings.')
            elif guesses['words'][1] == 'trash' or guesses['words'][1] == 'desk' or guesses['words'][1] == 'chair' or guesses['words'][1] == 'shelf':
                print('Doing that would either create a mess or break something you would not want to break. You reign your frustration in.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #jump#

        if guesses['words'][0] == 'jump':
            if guesses['words'][1] == 'desk' or guesses['words'][1] == 'shelf' or guesses['words'][1] == 'chair':
                print('Sounds fun, but your shoes might dirty the object. And if you take your shoes off, then your socks might get dirty. Some other time.')
            elif guesses['words'][1] == 'window':
                print('You think about it, then decide self-harm is not productive in this situation, if ever. Again, this office is on the fifth floor.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #boil#
        
        if guesses['words'][0] == 'boil' or guesses['words'][0] == 'cook':
            if guesses['words'][1] == 'noodle': #need to check if water is found
                if noodle == 0:
                    print('Noodles would be nice, they are your guilty pleasure. You have not found any yet. Maybe there is some in the room')
                elif noodle == 3:
                    print('You already ate the noodles. What, you want more? Who knows if there are any more in here.')
                elif noodle == 2:
                    print('You already cooked the noodles. It is time to dig in')
                elif water == 3:
                    print("It's unlucky but you might've drank the only water source in here. Doesn't seem like noodles are happening tonight")
                elif water > 0:
                    person = 1
                    print('You cooked those noodles. It looks like instant noodles is going to be your dinner tonight.')
                    noodle = 2
                    water = 3
                else:
                    print('You have the noodles. Now find some the water and boil it.')
                
            elif guesses['words'][1] == 'water': #need to check if water is found
                if water == 1:
                    water = 2
                    print('Some hot water would be nice. You got some now.')
                elif water == 2:
                    print("The water is already boiled. You deem it unnecessary to boil it even further")
                elif water == 3:
                    print("You already drank the water. Boiling yourself seems bad, so you won't do it.")
                else:
                    print("You don't even have water to boil. Calm down, take a deep breath, and don't lose it too much.")
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")

        #cook - see boil#
        
        #grab#

        if guesses['words'][0] == 'grab':
            if guesses['words'][1] == 'noodle':
                if noodle == 1:
                    print('You grabbed the noodles. Hopefully you can prepare them somehow.')
                    person = 1
                elif noodle == 2:
                    print('You already grabbed the noodles. Ate it too. Whoop whoop.')
                else:
                    print("You can't grab what you haven't seen.")
            elif guesses['words'][1] == 'water' or guesses['words'][1] == 'canteen':
                if water > 1:
                    print('You already grabbed the water. Used it too. Whoop whoop.')
                elif water == 1:
                    print('You took the canteen of water. At the very least, it could serve as a drink.')
                    person = 1
                else:
                    print("You can't grab what you haven't seen.")
            elif guesses['words'][1] == 'key':
                if key < 0:
                    print('You already took the key. Now you can get out of here.')
                else:
                    print("You really want to, but you have no idea where your employee hid the key.")
            elif guesses['words'][1] == 'note':
                if person == 0 or desknote == 0:
                    person = 0
                    print('You read the note at the wall. It reads:') #door note
                    print('''
"Hey, you look like you need some fun in your life. So I made a small Escape the Room scenario. I hid the key somewhere in the room, good luck finding it!"

Hold up, there is another, smaller line of text that you missed previously. It says:

"P.S: If you really want to leave though, read the note on the desk."
'''
                      )
                    desknote = 1
                elif person == 1:
                    print('You open the note on the desk. It reads:') #desk note
                    if key == 0:
                        print("Key is hidden in a drawer")
                    elif key == 1:
                        print("Key is hidden in a binder")
                    elif key == 2:
                        print("Key is hidden in the cup")
                    elif key == 3:
                        print("Key is hidden in the trash")
                    else:
                        print("Key is hidden in the stack of papers")
 
                else:
                    print('There are multiple notes in this room. You should move towards the location of the one you want')
            elif guesses['words'][1] == 'paper' or guesses['words'][1] == 'stack':
                person = 1
                if key == 4:
                    print('You grabbed the stack of paper on the desk. As you lifted it up, you heard a clang of metal as the key fell out from inside the stack, onto the desk. Perfect.')
                    key = -1
                else:
                    print('You grabbed the stack of paper on the desk. A careful search showed that nothing was here. You put the stack back.')
            elif guesses['words'][1] == 'cup':
                person = 1
                if key == 2:
                    key = -1
                    print("You grabbed the cup on the desk. Deciding to peek inside out of curiosity, you are rewarded with a key. Guess you're not a cat.")
                else:
                    print('You grabbed the cup on the desk. You think to yourself what exactly could you do with a cup. You put it back on the desk because you had no good answer.')
            elif guesses['words'][1] == 'book':
                print('You took out some books on the shelf. You then ask yourself if you have time to read these books. You put them back because you do not.')
            elif guesses['words'][1] == 'binder':
                person = 2
                if key == 1:
                    print("You flip through the binders. The key was hidden in one of them. Very nice.")
                    key = -1
                else:
                    print('You pick up the binders and look through them. You fail to find anything. Unfortunate.')
            elif guesses['words'][1] == 'fork':
                person = 4
                print('You took the fork. If you find anything to eat, you can use this to poke at the food.')
            elif guesses['words'][1] == 'trash':
                person = 4
                if key == 3:
                    print('This sounds like a dumb idea, but you go for it anyways. Thankfully it was a short endeavor, as the key was in the trash all along.')
                    key = -1
                else:
                    print('Picking up trash will not help you in any way. How did you even come up with this stuff?')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")

        
        #lift#
        
        if guesses['words'][0] == 'lift':
            if guesses['words'][1] == 'stack' or guesses['words'][1] == 'paper':
                person = 1
                if key == 4:
                    print('You lifted the stack of paper on the desk and heard a clang of metal as the key fell out from inside the stack and onto the desk. Perfect.')
                    key = -1
                else:
                    print('You lifted up all your unfinished paperwork and shook it. Nothing special happened. You put it back down. It was a workout at least.')
            elif guesses['words'][1] == 'binder':
                person = 2
                if key == 1:
                    print("You pick up the binders. The key slides out of one of them. Very nice.")
                    key = -1
                else:
                    print('You pick up the binders and look through them. You fail to find anything. Unfortunate.')
                print('You lifted up all the binders on the shelf. All you got out of it was a mess.')
            elif guesses['words'][1] == 'chair':
                person = 1
                print('You lifted up your chair. It is a decent workout, but not very helpful.')
            elif guesses['words'][1] == 'desk':
                print('Your noodle arms are too frail to do that. You remind yourself for the upteenth time that you will start working out this weekend')
            elif guesses['words'][1] == 'cup':
                person = 1
                if key == 2:
                    key = -1
                    print("You lift the cup on the desk. Turning it around, a key falls out instead of coffee. Good job.")
                else:
                    print('You lift up the cup on your desk. It feels weird to lift it up without any intent on getting coffee.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")

        #eat#

        if guesses['words'][0] == 'eat':
            if guesses['words'][1] == 'noodle':
                if noodle == 0:
                    print("Eat noodles? What noodle?")
                elif noodle == 1:
                    print("You don't think you can eat the noodles right now. Not like this, anyways")
                elif noodle == 3:
                    print("You already ate the noodles. It's doubtful you have more lying around in the office.")
                else:
                    noodle = 3
                    fed = 2
                    print("Your friends tell you that instant noodles is not real food. They just don't understand. It tasted great.")
                    if fork == 0:
                        print("You didn't have any utensils to eat with, so you resorted to slurping it out of the cup. You're alone, so who cares about your manners.")
                    else:
                        print("You take the fork from the trash and clean it to the best of your ability. It can't be helped, really, you're kinda hungry.")
            elif guesses['words'][1] == 'water':
                if water == 3:
                    print("You already used a canteen of water. Chances are there isn't any other sources of water left in the room.")
                elif water == 2:
                    print("You wait for the water to cool a bit and help yourself to a hot drink.")
                    fed = 1
                    water = 3
                elif water == 1:
                    print('You downed the water. A drink is pretty refreshing at times like these.')
                    fed = 1
                    water = 3
                else:
                    print("Water? What water?")

            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't.")
                
        #pull#

        if guesses['words'][0] == 'pull':
            if guesses['words'][1] == 'drawer':
                person = 1
                print('You pulled out the drawers. You concluded after a thorough search that there are a lot of papers and one serving of cup noodles.')
                noodle = 1
                if key == 0:
                    print('There also is the key. Now you can get out of here.')
                    key = -1
            elif guesses['words'][1] == 'book':
                person = 2
                print('You pulled out a bunch of books. You got a mess on the floor. Perhaps there was a better way of doing this. Oh well.')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #use#

        if guesses['words'][0] == 'use':
            if guesses['words'][1] == 'boiler':
                if water == 1:
                    person = 1
                    print('You used the boiler to heat the water. Good job, you are still capable of basic actions.')
                    water = 2
                else:
                    print("There really isn't anything TO boil. Let's not start experimenting now.")
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #kill#

        if guesses['words'][0] == 'kill':
            print('You admonish yourself to focus at the task at hand before you tread down a path you might regret.')
            
        #sleep#

        if guesses['words'][0] == 'sleep': #if successful, should end the game
            if fed == 0:
                print('You could, but you feel a bit hungry. Something to eat, or even drink, would be nice.')
            else:
                if fed == 1:
                    print("You only had something to drink, but you'll survive until the next morning.")
                else:
                    print("You had some nice noodles, so you feel pretty good for sleeping now.")
                    
                if guesses['words'][1] == 'floor':
                    print('It is cold, but it will have to do. You lie down on the floor and, after some initial discomfort, fall asleep.')
                    return 2
                elif guesses['words'][1] == 'desk':
                    print('You created a mess clearing the desk, but it is a decent place to sleep. You lie down on your desk and fall asleep.')
                    return 2
                elif guesses['words'][1] == 'chair' or guesses['words'][1] == 'room':
                    print('Well, you woke up on the chair, might as well go back to sleep on the chair. You sit on your chair, lay back, and fall asleep')
                    return 2
                else:
                    print("You could do this. It sounds like a recipe for disaster, so you won't")

        #push#

        if guesses['words'][0] == 'push':
            if guesses['words'][1] == 'door':
                person = 0
                if key >= 0:
                    print('No matter how hard you try, the door refuses to budge. Perhaps, if you went to the gym, you could break the door down like in the movies.')
                else:
                    print('You found the key already. After unlocking it, you successfully pushed open the door. Sweet, time to go home.')
                    return 1
            elif guesses['words'][1] == 'desk':
                print('Moving the desk probably will not help here. Also, for you it is difficult. Shame.')
            elif guesses['words'][1] == 'chair':
                person = 1
                print('You push the chair around, doing your best clown school imitation. You have never went to clown school, so it probably was not an accurate performance')
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")
        
        #observe#
        #study#

        if guesses['words'][0] == 'observe' or guesses['words'][0] == 'study':
            if guesses['words'][1] == 'desk': #Apparently table refers to the data table
                person = 1
                desknote = 1
                print(
'''Your desk isn't the most neat, but you can find what you need on most days, and that's what counts. 

A stack of unfinished paperwork sits front and center. You remember working on it before dozing off. On top of it appears to be a folded note. You don't remember writing one before falling asleep.

Your coffee cup, along with a water boiler, is located at the upper right corner of the desk surface.

Next to the desk is your "boss" chair, it's posh if you do say so yourself. Sleeping in it was comfortable.

There are drawers lined on the side of the desk. You normally store documents there.'''
                )

            elif guesses['words'][1] == 'chair':
                person = 1
                print("It's a really snazzy chair. Otherwise, there appears to be nothing special about it")
   
            elif guesses['words'][1] == 'door': #depends on whether or not you have key
                person = 0
                if key >= 0:
                    print("The door won't unlock itself if you stare at it. The note your employee put up will simply mock your efforts. Who came up with doors that cannot be unlocked from the inside without a key, anyways?")
                else:
                    print("You have the key. Instead of wasting your time looking at the door, why don't you leave?")

            elif guesses['words'][1] == 'shelf':
                print("The shelf is quite small, about waist height. It's holding some books related to your field. Some binders are strewn on top of the shelf. There is also a canteen of water")
                water = 1

            elif guesses['words'][1] == 'drawer': #key might be in here
                print("The drawers normally hold some documents, but it's possible something useful is hidden away in them. You take a look.")
                person = 1
                print('You pulled out the drawers. You concluded after a thorough search that there are a lot of papers and one serving of cup noodles.')
                noodle = 1
                if key == 0:
                    print('There also is the key. Now you can get out of here.')
                    key = -1

            elif guesses['words'][1] == 'trash': #key might be in here
                print("The trash was recently cleaned out. There is a fork in there. It actually doesn't look that dirty. Otherwise some paper balls here and there. You swallow your pride and search the trash.")
                fork = 1
                person = 4
                if key == 3:
                    print('Turns out the key was in the trash all along.')
                    key = -1
                else:
                    print("You feel a bit icky, but nothing came out of it.")

            #elif guesses['words'][1] == 'floor': depends on location, key might be here

            elif guesses['words'][1] == 'wall': 
                print("The walls are pretty plain. You could try knocking the wall and make some noise, but you're pretty sure no one is around to hear it.")
                
            elif guesses['words'][1] == 'window':
                person = 3
                print("A window overlooking the great city horizon. Just kidding, you're only on the fifth floor, most buildings are taller than that.")

            elif guesses['words'][1] == 'cup': #key might be in here
                person = 1
                print("Your coffee cup. It's been your partner through the tough times. It's possible the key is hidden in the cup.")

                if key == 2:
                    key = -1
                    print("You lift the cup on the desk. Turning it around, a key falls out instead of coffee. Good job.")
                else:
                    print('You check, but the cup is empty of both key and joe.')
                
            elif guesses['words'][1] == 'note': #location dependent
                if person == 0 or desknote == 0:
                    person = 0
                    print('You read the note at the wall. It reads:') #door note
                    print('''
"Hey, you look like you need some fun in your life. So I made a small Escape the Room scenario. I hid the key somewhere in the room, good luck finding it!"

Hold up, there is another, smaller line of text that you missed previously. It says:

"P.S: If you really want to leave though, read the note on the desk."
'''
                      )
                    desknote = 1
                elif person == 1:
                    print('You open the note on the desk. It reads:') #desk note
                    if key == 0:
                        print("Key is hidden in a drawer")
                    elif key == 1:
                        print("Key is hidden in a binder")
                    elif key == 2:
                        print("Key is hidden in the cup")
                    elif key == 3:
                        print("Key is hidden in the trash")
                    else:
                        print("Key is hidden in the stack of papers")
 

                else:
                    print('There are multiple notes in this room. You should move towards the location of the one you want')

            elif guesses['words'][1] == 'noodle':
                if noodle == 0:
                    print("Noodles? What noodles?")
                else:
                    print("Noodles are meant to be eaten, not examined. You would rather figure out how to cook and eat this instead.")
                            
            elif guesses['words'][1] == 'binder': #key might be in here
                person = 2
                print("You were meaning to clean up the binder mess on top of the shelf for a few days now. This still isn't the time, but maybe the key is hidden in this mess.")
                if key == 1:
                    print("You flip through the binders. The key was hidden in one of them. Very nice.")
                    key = -1
                else:
                    print("You flip through all the binders and succeeded in creating an even more disorderly pile of binders.")
                
            elif guesses['words'][1] == 'book':
                person = 2
                print("You don't think you've read the majority of these books. You wonder what that means for you. It's possible your employee hid the key in one of them, but you hope they weren't that mean.")

            elif guesses['words'][1] == 'water' or guesses['words'][1] == 'canteen':
                if water == 0:
                    print("Water? What water?")
                else:
                    person = 2
                    print("An clean canteen bottle. You don't remember why you have this in the office but you sure are happy to see it.")

            elif guesses['words'][1] == 'fork':
                if fork == 0:
                    print("Fork? What fork?")
                else:
                    person = 3
                    print("A fork in the trash can. It's dirty, but if you don't want to eat with your hands, it might have to do.")
   
            elif guesses['words'][1] == 'paper' or guesses['words'][1] == 'stack': #might hold key
                person = 1
                print("You've been working on this pile of paperwork the whole morning. You wouldn't be surprised if your employee hid the key in this stack.")
                if key == 4:
                    print('You lifted the stack of paper on the desk and heard a clang of metal as the key fell out from inside the stack and onto the desk. Perfect.')
                    key = -1
                else:
                    print('You lifted up all your unfinished paperwork and shook it. Nothing special happened. You put it back down. It was a workout at least.')

            elif guesses['words'][1] == 'boiler':
                person = 1
                print("A water boiler. It's nothing fancy, just gets the job done. You look inside the boiler. No key there.")

            #elif guesses['words'][1] == 'key': #depends on whther or not you have it

            elif guesses['words'][1] == 'room':
                print('''Your office isn't that big, but it's cozy.

Your desk takes up most of the space. A soft, comfortable chair is next to it.

On one side of the room is a shelf.

There is a window at the back of the room.

The door is at the front of the room. 

There is a trash can in one corner of the room.            
            
'''
                      )
            else:
                print("You could do this. It sounds like a recipe for disaster, so you won't")

                
    return 0

endgame = False

print('''

You wake up at your desk. It's Thursday and you've dozed off near the end of your work hours while you were working on your paperwork.

Deciding that your work can wait until tomorrow, you get up to leave your office. You try to open the door, but it's locked.

Ok, that sucks. You reach into your pocket for the key to unlock it. It's not there.

You pat yourself down. The key is nowhere to be found. You begin to panic, thinking how you're going to be stuck here for at least a night.

Then you glance at the door again and you notice that a note has been taped to it. It says:

"Hey, you look like you need some fun in your life. So I made a small Escape the Room scenario. I hid the key somewhere in the room, good luck finding it!"

It appears one of your employees has taken your key and hidden it in your room. Incredible. You decide that once you figure out the culprit, you're cutting his/her wages.

But first, you should figure out where the key is so you can get out of here.

...Or maybe you can stay the night, who knows.

'''
)

while (endgame == False):
    teststr = raw_input('What will you do? ')
    outputs = commandparse(teststr)

    #need to figure out ways to deal with cases "look up" and "look down"
      
    print(outputs)
    guesses = guesswords(outputs)
    print(guesses)
    if guesses != 1:
        check = interpretguess(guesses)
        pastobj = outputs['object']

        if check > 0:
            if check == 1:
                print("As you head home, you think to yourself just who could've pranked you like this. You feel tired, however, so you decide to leave the reckoning for tomorrow.")
            else:
                print("When you wake up the next morning, you raise a ruckus in your office. People hear you and try to open the door, but with no key on their end, they had to call the fire department to break down the door. You seriously consider how much of the budget could be devoted to better doors, as well as who exactly do you have to give a pay cut to.")
            print("The End")
            endgame = True

