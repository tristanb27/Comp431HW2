# Tristan Blizzard 730390144
# Honor Pledge

import sys
# Globals
sp= [' ','\t']
special = ["<", ">", ")", "(", "]", "[", "\\", ".","@", ',', ";", ":", '"', "'"]
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
CRLF = '\n'
null = None
# List for recipients' <path>
rcpts = []
# For the sender's <path>
sender = ""
# For the data that is to be sent in the message
msg = ""
# List that contains the names of the files to be created in the forward directory
names = []
# Used for differnetiating when to add a <path> to sender or rcpts; if i = 0: Sender <path>, i = 1: rcpts <path>
i = 0

# Function that hard checks if "MAIL" and "FROM:" are in the cmd, along with infinite whitespace in between
def mail_from_cmd(line):
    if line[0] != 'M':
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if line[1] != 'A':
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if line[2] != 'I':
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if line[3] != 'L':
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    fromLine = checkWhitespace(line,line[4:])
    if fromLine is None:
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if fromLine[0] != "F":
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if fromLine[1] != "R":
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if fromLine[2] != "O":
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if fromLine[3] != "M":
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if fromLine[4] != ":":
        sys.stdout.write(line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    reversePathLine = checkNull(line,fromLine[5:])
    checkReversePath(line, reversePathLine)

# Same as mail_from_cmd but for RCPT TO:
def rcpt_to_cmd(rcpt_line):
    if rcpt_line[0] != "R":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if rcpt_line[1] != "C":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if rcpt_line[2] != "P":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if rcpt_line[3] != "T":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    toLine = checkWhitespace(rcpt_line, rcpt_line[4:])
    if toLine is None:
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if toLine[0] != "T":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if toLine[1] != "O":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if toLine[2] != ":":
        sys.stdout.write(rcpt_line)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    forwardPathLine = checkNull(rcpt_line, toLine[3:])
    checkForwardPath(rcpt_line, forwardPathLine)


# Function used to check if a space between something is null. If it is, simply send the line back, but if it is not, go to the whitespace checker
def checkNull(line,nullSpaceLine):
    if nullSpaceLine[0] not in sp:
        return nullSpaceLine
    else:
        return checkWhitespace(line,nullSpaceLine)

# Function that feeds into the check path function
def checkReversePath(line, reversePathLine):
    checkPath(line, reversePathLine)

#Same as checkReversePath; done for name's sake
def checkForwardPath(rcpt_line, forwardPathLine):
    checkPath(rcpt_line, forwardPathLine)

# Function that checks if the first character is "<" and if the last character is ">". Between those two, it checks the mailbox
def checkPath(line, pathLine):
    global i
    if pathLine[0] != "<":
        sys.stdout.write(line)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    finalLine = checkMailbox(line,pathLine[1:])
    if finalLine is None:
        sys.exit()
    if finalLine [0] != ">":
        sys.stdout.write(line)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    finalCheck = checkNull(line,finalLine[1:])
    CRLFCheck = checkCRLF(line, finalCheck)
    if CRLFCheck != True:
        sys.stdout.write(line)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    if i == 1:
        rcptAdd(pathLine)
    else:
        global sender
        sender += pathLine[:-1]

    printLine(line)

# This appends path names (the ones with "<" and ">" at the end) to the rcpts list for the document, and appends
# the name to be used in the forward directory (without the "<" and ">")
def rcptAdd(pathLine):
    global rcpts
    global name
    rcpts.append(pathLine[:-1])
    name = pathLine[1:]
    name = name[:-2]
    names.append(name)

# For finishing the MAIL TO and RCPT TO requests 
def printLine(line):
    sys.stdout.write(line)
    print("250 OK")



# Function that checks the mailbox by checking local, the @ symbol in between, and domain. If the local name or domain result in an error, it returns none and the statement is printed out
def checkMailbox(line,mailboxLine):
    atSymbolLine = checkLocalName(line,mailboxLine)
    if atSymbolLine is None:
        sys.exit()
    if atSymbolLine[0] != "@":
        sys.stdout.write(line)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    finalBracketLine = checkDomain(line,atSymbolLine[1:])
    if finalBracketLine is None:
        sys.exit()
    return finalBracketLine


# Goes into check string
def checkLocalName(line,localNameLine):
    return checkString(line,localNameLine)


# Function for checking local name standards
def checkString(line,stringLine):
    if stringLine[0] in sp or stringLine[0] in special:
        sys.stdout.write(line)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    i = 0
    while i < len(stringLine):
        if stringLine[i] in sp or stringLine[i] in special:
            return stringLine[i:]
        if stringLine[i] == "@":
            return stringLine[i:]
        i+=1


# Checks the domain to see if it is a let-dig-str, and if it is a '.', to see if another let-dig-str is after it
def checkDomain(line,domainLine):
    i = 0
    while i < len(domainLine):
        if domainLine[0] not in letter:
            sys.stdout.write(line)
            print("501 Syntax error in parameters or arguments")
            sys.exit()
        if domainLine[i] in letter or domainLine[i] in digit:
            i+=1
        elif domainLine[i] in sp or digit:
            if domainLine[i] == '.' and domainLine[i+1] in letter:
                i+=1
            elif domainLine[i] == '.' and domainLine[i+1] not in letter:
                sys.stdout.write(line)
                print("501 Syntax error in parameters or arguments")
                sys.exit()
            else:
                return domainLine[i:]
        elif domainLine[i] == CRLF:
            return domainLine[i:]
        else:
            return domainLine[i:]
        

# Checks the whitespace by seeing if at least one character of whitespace exists already, and then checking for further whitespaces
def checkWhitespace(line,whitespaceLine):
    i = 0
    while i < len(whitespaceLine):
        if whitespaceLine[0] not in sp:
            return None
        elif whitespaceLine[i] not in sp:
            return(whitespaceLine[i:])
        i+=1


# Checks to see if the \n character exists
def checkCRLF(line, lineCRLF):
    if lineCRLF != CRLF:
        return False
    else:
        return True

# Checks the DATA request in the same manner as mail_from_cmd and rcpt_to_cmd
def dataCheck(dataLine):
    if dataLine[0] != "D":
        sys.stdout.write(dataLine)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if dataLine[1] != "A":
        sys.stdout.write(dataLine)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if dataLine[2] != "T":
        sys.stdout.write(dataLine)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    if dataLine[3] != "A":
        sys.stdout.write(dataLine)
        print("500 Syntax error: command unrecognized")
        sys.exit()
    CRLFLine = checkNull(dataLine, dataLine[4:])
    if (checkCRLF(dataLine, CRLFLine)) != True:
        sys.stdout.write(dataLine)
        print("501 Syntax error in parameters or arguments")
        sys.exit()
    sys.stdout.write(dataLine)
    print("354 Start mail input; end with <CRLF>.<CRLF>")
    

# Checks the message. Will keep on going until CRLF.CRLF is encountered 
def msgChecker():
    msgLine = sys.stdin.readline()
    if msgLine[0] == '.' and msgLine[1] == CRLF:
        sys.stdout.write(msgLine)
        print("250 OK")
    else:
        sys.stdout.write(msgLine)
        global msg
        msg += msgLine
        msgChecker()

# Checks if a request is MAIL FROM: when it shouldn't be
def mailFromCheck(line): 
    if (line[0] == "M" and line[1] == "A" and line[2] == "I" and line[3] == "L"):
        fromLine = checkWhitespace(line, line[4:])
        if fromLine is None:
            sys.stdout.write(line)
            print("500 Syntax error: command unrecognized")
            sys.exit()
        elif (fromLine[0] == "F" and fromLine[1] == "R" and fromLine[2] == "O" and fromLine[3] == "M" and fromLine[4] == ":"):
            return True
    else:
        return False

# Checks if a request is RCPT TO: when it shouldn't be
def rcptToCheck(line):
    if (line[0] == "R" and line[1] == "C" and line[2] == "P" and line[3] == "T"):
        toLine = checkWhitespace(line, line[4:])
        if toLine is None:
            sys.stdout.write(line)
            print("500 Syntax error: command unrecognized")
            sys.exit()
        elif (toLine[0] == "T" and toLine[1] == "O" and toLine[2] == ":"):
            return True
    else:
        return False

# Checks if a request is DATA when it shouldn't be
def dataInputCheck(line):
    if (line[0] == "D" and line[1] == "A" and line[2] == "T" and line[3] == "A"):
        return True
    else:
        return False

def main():
    mailFromLine = sys.stdin.readline()
    if(rcptToCheck(mailFromLine) == True or dataInputCheck(mailFromLine) == True):
        sys.stdout.write(mailFromLine)
        print("503 Bad sequence of commands")
        sys.exit()
    mail_from_cmd(mailFromLine)
    global i 
    i = 1
    rcptToLine = sys.stdin.readline()
    if(mailFromCheck(rcptToLine) == True or dataInputCheck(rcptToLine) == True):
        sys.stdout.write(rcptToLine)
        print("503 Bad sequence of commands")
        sys.exit()
    rcpt_to_cmd(rcptToLine)
    data = False
    while data == False:
        nthToLine = sys.stdin.readline()
        if (mailFromCheck(nthToLine) == True):
            sys.stdout.write(nthToLine)
            print("503 Bad sequence of commands")
            sys.exit()
        if nthToLine == "DATA\n":
            data = True
            dataCheck(nthToLine)
        else:
            rcpt_to_cmd(nthToLine)
    msgChecker()
    for name in names:
        file = open("forward/" + name, "+a")
        file.write("From: " + sender + "\n")
        for rcpt in rcpts:
            file.write("To: " + rcpt + "\n")
        file.write(msg)
        file.close()
    i = 0
    
if __name__ == "__main__":
    main()
 
