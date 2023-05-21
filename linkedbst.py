"""
File: linkedbst.py
Author: Ken Lambert
"""
import time
from copy import copy
from random import sample, shuffle
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while node is not None:
            if item == node.data:
                return node
            elif item < node.data:
                node = node.left
            else:
                node = node.right
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:

            node = self._root
            while True:
                # New item is less, go left until spot is found
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
                    # End of recurse
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, node = -1):
        '''
        Return the height of tree
        :return: int
        '''

        length = 0

        if self._root is None:
            return 0
        if node is None:
            return -1


        def height1(top, value):
            '''
            Helper function
            :param top:
            :return:
            '''
            left = value
            right = value
            if top.left is None and top.right is None:
                if value > length:
                    return value
            if top.right is not None:
                left = height1(top.right, value + 1)
            if top.left is not None:
                right = height1(top.left, value + 1)

            return max(left, right)
        if node != -1:
            length = height1(node, 0)
        else:
            length = height1(self._root, 0)
        return length

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if not self._root:
            return True
        def check_balanced(top):
            left = True
            right = True
            if abs(self.height(top.left) - self.height(top.right)) > 1:
                return False
            if top.left is not None:
                left = check_balanced(top.left)
            if top.right is not None:
                right = check_balanced(top.right)
            return left and right

        return check_balanced(self._root)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        if not self._root:
            return
        elements = []
        def recurse_tree(node):
            if low <= node.data <= high:
                elements.append(node.data)

            if node.left is not None:
                recurse_tree(node.left)

            if node.right is not None:
                recurse_tree(node.right)
            return
        recurse_tree(self._root)
        return sorted(elements)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if not self._root:
            return
        elements = []
        for element in self:
            elements.append(element)
        elements = sorted(elements)
        half = len(elements)//2
        self._root = BSTNode(elements[half])
        del elements[half]
        def recurse(list_pass):
            if len(list_pass) == 1:
                self.add(list_pass[0])
                return
            elif list_pass == []:
                return
            half = len(list_pass) // 2
            self.add(list_pass[half])
            del list_pass[half]
            recurse(list_pass[:half])
            recurse(list_pass[half:])
            return

        recurse(elements[:half])
        recurse(elements[half:])


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        larger = []
        for element in self:
            if element > item:
                larger.append(element)
        return min(larger) if larger else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        smaller = []
        for element in self:
            if element < item:
                smaller.append(element)
        return max(smaller) if smaller else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        words = []
        with open(path, "r") as file:
            for word in file:
                words.append(word.strip().replace("\n", ""))
        words = words[:30000]
        random_sample = sample(words, 10000)

        # Finding random elements using build in list index method
        start_time = time.time()
        for element in random_sample:
            words.index(element)
        print(f"Time take for finding 10000 elements using\
 build in methods in list: {time.time() - start_time}")

        # Finding random elements using BST created through
        # adding element in alphabatic order
        tree_alphabetic = LinkedBST()

        for word in sorted(words):
            tree_alphabetic.add(word)

        start_time = time.time()
        for element in random_sample:
            tree_alphabetic.find(element)

        print(f"Time take for finding 10000 elements using\
 BST created through adding element in alphabatic order: {time.time() - start_time}")

        # Finding random elements using BST
        # created through adding element in random order
        tree_random = LinkedBST()
        words_shuffle = copy(words)
        shuffle(words_shuffle)
        for word in words_shuffle:
            tree_random.add(word)

        start_time = time.time()
        for element in random_sample:
            tree_random.find(element)

        print(f"Time take for finding 10000 elements using\
 BST created through adding element in random order: {time.time() - start_time}")

        # Finding random elements using balanced BST
        tree_alphabetic.rebalance()

        start_time = time.time()
        for element in random_sample:
            tree_alphabetic.find(element)

        print(f"Time take for finding 10000 elements in balanced tree: {time.time() - start_time}")

tree = LinkedBST()
tree.demo_bst("words.txt")
