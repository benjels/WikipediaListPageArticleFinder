__author__ = 'user'


list0=['A','B']           # We don't need semicolons
list1=['C','D']
lists=[list0, list1]      # Create a list of lists
z=0
while z < 1:
    for q in lists[z]:    # We access list's index with [], not with ()
        print(q)
    z += 1