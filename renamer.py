import os, shutil, re
filenameRegex = re.compile(r'(.*?) (.*?)(.MOV)')      #set regex group (first word) (rest of stuff)(file extension)
#lletteregex = re.compile(r'(.*?)\\(R|T)')             #regex (file path)\(R or T)  2nd parent folder indicated which card it was on    
for subfoldername, subfolder, filenames in os.walk('Z:\\Video\\2015\\Board Overview Videos\\Footage'): #loop all files in directory
    head, tail = os.path.split(subfoldername)       #splits path from last folder name
    #print(tail)

    for filename in filenames:                  #loops through file names in directory
        name = filenameRegex.search(filename)    #search
        #letter = lletteregex.search(head)       #folder letter regex match
        #if  letter == None:        #continue if regex not matched
        #    continue
        if  name == None:        #continue if regex not matched
            continue
        board = name.group(1)   #assign board name from regex split to variable
        #print(board.lower())
        if board.lower() in ('s35', 's38', 'kt36', 'srdh', 'br', 'brsk', 'pr', 'mr', 'tt', 'cc', 'sd', 'prdt', 'b-roll', 'team', 'vape', 'brdh', 'prime', 'batray', 'siphon', 'dropped'  ):
            #board = 'misc'      #if not one of the main boards going to misc folder
            
            #if board.lower() in ('prime', 'batray', 'dropped', 'siphon'):
            #print(board)  
            oldpath = subfoldername + "\\" + filename   #old file path including filename
            #print(os.path.getctime(oldpath))
            if os.path.getctime(oldpath) < 1435611309.0:
                continue
            newfolder = 'Z:\\Video\\2015\\Board Overview Videos\\Footage\\' + board  #new folder location
            print(oldpath)
            #if not os.path.exists(newfolder): #if folder does not exist make it
            #    os.makedirs(newfolder)
            newpath = newfolder + "\\" + name.group(1) + "p " + name.group(2) + name.group(3) #new file name and full path
            print(newpath)
            
            shutil.move(oldpath, newpath)       #move and assign new file names
        
