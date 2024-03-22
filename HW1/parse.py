#Tristan Blizzard 730390144
# Honor Pledge

import sys
# Globals
sp= [' ','\t']
special = ["<", ">", ")", "(", "]", "[", "\\", ".","@", ',', ";", ":", '"', "'"]
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
CRLF = '\n'
null = None

# Function that hard checks if "MAIL" and "FROM:" are in the cmd, along with infinite whitespace in between
def mail_from_cmd(line):
    if line[0] != 'M':
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if line[1] != 'A':
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if line[2] != 'I':
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if line[3] != 'L':
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    fromLine = checkWhitespace(line,line[4:])
    if fromLine is None:
        return
    if fromLine[0] != "F":
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if fromLine[1] != "R":
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if fromLine[2] != "O":
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if fromLine[3] != "M":
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    if fromLine[4] != ":":
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")
        return
    reversePathLine = checkNull(line,fromLine[5:])
    checkReversePath(line, reversePathLine)

# Function used to check if a space between something is null. If it is, simply send the line back, but if it is not, go to the whitespace checker
def checkNull(line,nullSpaceLine):
    if nullSpaceLine[0] not in sp:
        return nullSpaceLine
    else:
        return checkWhitespace(line,nullSpaceLine)

# Function that feeds into the check path function
def checkReversePath(line, reversePathLine):
    checkPath(line, reversePathLine)


# Function that checks if the first character is "<" and if the last character is ">". Between those two, it checks the mailbox
def checkPath(line, pathLine):
    if pathLine[0] != "<":
        sys.stdout.write(line)
        print("ERROR -- path")
        return
    finalLine = checkMailbox(line,pathLine[1:])
    if finalLine is None:
        return
    if finalLine [0] != ">":
        sys.stdout.write(line)
        print("ERROR -- path")
        return
    finalCheck = checkNull(line,finalLine[1:])
    CRLFCheck = checkCRLF(line, finalCheck)
    if CRLFCheck != True:
        sys.stdout.write(line)
        print("ERROR -- CRLF")
        return
    else:
        printLine(line)

def printLine(line):
    sys.stdout.write(line)
    print("Sender ok")



# Function that checks the mailbox by checking local, the @ symbol in between, and domain. If the local name or domain result in an error, it returns none and the statement is printed out
def checkMailbox(line,mailboxLine):
    atSymbolLine = checkLocalName(line,mailboxLine)
    if atSymbolLine is None:
        return
    if atSymbolLine[0] != "@":
        sys.stdout.write(line)
        print("ERROR -- mailbox")
        return
    finalBracketLine = checkDomain(line,atSymbolLine[1:])
    if finalBracketLine is None:
        return
    return finalBracketLine


# Goes into check string
def checkLocalName(line,localNameLine):
    return checkString(line,localNameLine)


# Function for checking local name standards
def checkString(line,stringLine):
    if stringLine[0] in sp or stringLine[0] in special:
        sys.stdout.write(line)
        print("ERROR -- string")
        return None
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
            print("ERROR -- element")
            return None
        if domainLine[i] in letter or domainLine[i] in digit:
            i+=1
        elif domainLine[i] in sp or digit:
            if domainLine[i] == '.' and domainLine[i+1] in letter:
                i+=1
            elif domainLine[i] == '.' and domainLine[i+1] not in letter:
                sys.stdout.write(line)
                print("ERROR -- element")
                return None
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
            sys.stdout.write(line)
            print("ERROR -- whitespace")
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



def main():
    line = sys.stdin.readline()
    if line != "":
        mail_from_cmd(line)
    else:
        sys.stdout.write(line)
        print("ERROR -- mail-from-cmd")

if __name__ == "__main__":
    main()
    
