##Kieran Devany
##Plan Design


##Linked list construction
class Node:
    def __init__(self, title=None,body=None,goal=None,status= "I"):
        self.title=title
        self.body=body
        self.goal=goal
        self.status=status
        self.nextval=None

##used once in the begining of every linkedlist

class HeadNode:
    def __init__(self, title=None, author=None, rating=0, scope="p"): 
        self.title=title
        self.author=author
        self.rating=rating
        self.scope=scope
        self.nextval=None
        
        
class linkedList:
    def __init__(self):
        self.headval=None
        
def printNodes(node):
    print("Title: " + node.title)
    print("Author: " + node.author)
    print("Rating: " + str(node.rating))

test1=linkedList()
test1.headval=HeadNode("learn python","Kieran Devany")
node2=Node("unit 1", "ayy lmao", "say what")
test1.headval.next=node2
printNodes(test1.headval)



