# Comparison in finding elements BST and list

Comparison of finding 10000 elements at:
* list
* BST created through adding elements in alphabetic order
* BST created through adding elements in random order
* Balanced BST

### Results
Time take for finding 10000 elements using build in methods in list: 1.425175666809082
Time take for finding 10000 elements using BST created through adding element in alphabatic order: 11.522167205810547
Time take for finding 10000 elements using BST created through adding element in random order: 0.02445220947265625  
Time take for finding 10000 elements in balanced tree: 0.018008947372436523

### Analysys
As we can see time taken for finding elements in BST (alphabetic order) takes the largest amount of time as it goes through the whole tree. Also adding elements to such tree will take a lot of time as it goes through every element. Than list build in method with complexity of O(n). Fastest is finding elements at balanced tree as to get to particular element you have to make small amount of steps, complexity (O(log(n))), h - height of tree. Random order comes closer to this idea, but its uncertainty can not provide fastest approach.
