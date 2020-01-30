##Kieran Devany
##Plan Design


##Linked list construction
class Node:
    def __init__(self, title=None,body=None,goal=None,status="I"):
        self.title=title
        self.body=body
        self.goal=goal
        self.status=status
        self.nextval=None

##used once in the begining of every linkedlist

class HeadNode:
    def __init__(self, title=None, author=None, rating=0, scope="p") 
        self.title=title
        self.author=author
        self.rating=rating
        self.scope=scope
        self.nextval=None
        
        
class linkedList:
    def __init__(self):
        self.headval=None
        
test1=linkedList()
test1.headval=HeadNode()
node2=Node("no")
test1.headval.next=node2
print(test1.headval.val)
print(test1.headval.next.val)
