# Suffix Tree implementation using Ukknonen's Algorithm 
class SuffixTreeNode:
    """
    Represents a node in the suffix tree.

    Attributes:
        children (dict): Dictionary containing child nodes mapped to their respective characters.
        suffix_link (SuffixTreeNode or None): Reference to the suffix link of the node.
        start (int): Starting index of the substring represented by the node.
        end (int or None): Ending index of the substring represented by the node.
    """
    def __init__(self, start=-1, end=None):
        """
        Initializes a suffix tree node.
        
        Args:
            start (int): Starting index of the substring represented by the node. Default is -1.
            end (int or None): Ending index of the substring represented by the node. Default is None.
        """
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end

class SuffixTree:
    """
    Represents the suffix tree.
    
    Attributes:
        string (str): Input string with a termination symbol ('$') appended.
        root (SuffixTreeNode): Root node of the suffix tree.
        size (int): Length of the input string.
        active_node (SuffixTreeNode): Current active node during suffix tree construction.
        active_edge (int): Current active edge during suffix tree construction.
        active_length (int): Current active length during suffix tree construction.
        remaining_suffix_count (int): Count of remaining suffixes to process during construction.
        last_new_node (SuffixTreeNode or None): Last new node created during suffix tree construction.
        current_end (int): Current end index during suffix tree construction.
    """
    def __init__(self, string):
        """
        Initializes the suffix tree with the input string.
        
        Args:
            string (str): Input string for constructing the suffix tree.
        """
        self.string = string + "$"      # Append input string with a termination symbol
        self.root = SuffixTreeNode()    # Root of suffix tree is created with an empty string
        self.build_tree()               # Initializes variables used during suffix tree construction

    def edge_length(self, node):
        """
        Calculates the length of the edge represented by a node.
        
        Args:
            node (SuffixTreeNode): Node whose edge length is to be calculated.
        
        Returns:
            int: Length of the edge represented by the node.
        """
        return min(node.end, self.current_end) - node.start + 1

    def build_tree(self):
        """
        Builds the suffix tree by iterating through the input string and extending it for each character.
        """
        self.size = len(self.string)
        self.root.end = -1
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.last_new_node = None
        self.current_end = -1

        for i in range(self.size):
            self.extend_suffix_tree(i)

    def extend_suffix_tree(self, pos):
        """
        Extends the suffix tree to include suffix ending at position 'pos'.
        """
        self.current_end = pos
        self.remaining_suffix_count += 1
        self.last_new_node = None

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            if self.string[self.active_edge] not in self.active_node.children:
                # If current character is not in active node's children, create new edge and node
                self.active_node.children[self.string[self.active_edge]] = SuffixTreeNode(pos, float('inf'))

                if self.last_new_node:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None
            else:
                next_node = self.active_node.children[self.string[self.active_edge]]
                if self.walk_down(next_node): 
                    continue

                if self.string[next_node.start + self.active_length] == self.string[pos]:
                    if self.last_new_node and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    self.active_length += 1
                    break
                
                # Perform split if necessary
                split_end = next_node.start + self.active_length - 1
                split = SuffixTreeNode(next_node.start, split_end)
                self.active_node.children[self.string[self.active_edge]] = split
                split.children[self.string[pos]] = SuffixTreeNode(pos, float('inf'))
                next_node.start += self.active_length
                split.children[self.string[next_node.start]] = next_node

                if self.last_new_node:
                    self.last_new_node.suffix_link = split

                self.last_new_node = split

            self.remaining_suffix_count -= 1

            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link else self.root

    def walk_down(self, next_node):
        """
        Moves down the tree based on the active length and edge length.
        
        Args:
            next_node (SuffixTreeNode): Next node to traverse.
        
        Returns:
            bool: True if the active length is greater than or equal to the edge length of the next node, False otherwise.
        """
        if self.active_length >= self.edge_length(next_node):
            self.active_edge += self.edge_length(next_node)
            self.active_length -= self.edge_length(next_node)
            self.active_node = next_node
            return True
        return False

    def print_tree(self, node=None, prefix=""):
        """
        Recursively prints the suffix tree starting from the given node.
        
        Args:
            node (SuffixTreeNode, optional): Starting node to print the tree from. Defaults to None (root node).
            prefix (str, optional): Prefix string to be printed before each edge. Defaults to an empty string.
        """
        if node is None:
            node = self.root
        for char, child in node.children.items():
            edge_end = min(child.end, self.current_end)
            edge_string = self.string[child.start:edge_end + 1]
            print(f"{prefix}{edge_string}")
            self.print_tree(child, prefix + edge_string)

    def substring_search(self, pattern):
        """
        Searches for a substring in the suffix tree.

        Args:
            pattern (str): Substring to search for.

        Returns:
           List of positions where substring was found, if substring not found, returns print statement
        """
        def substring_search(string, pattern):
            positions = []
            for i in range(len(string)):
                if string[i:i+len(pattern)] == pattern:
                    positions.append(i)
            return positions

        positions = substring_search(self.string, pattern)
        if positions:
            return positions  # Provides positions of substring if found in string
        else:
            print("Substring '{}' not found".format(pattern))

    def pattern_matching(self, pattern):
        """
        Finds occurrences of a pattern in the suffix tree.

        Args:
            pattern (str): Pattern to search for.

        Returns:
            list: List of starting indices of pattern occurrences.
        """
        def pattern_matching(text, pattern):
            positions = []
            for i in range(len(text) - len(pattern) + 1):
                if text[i:i+len(pattern)] == pattern:
                    positions.append(i)
            return positions

        return pattern_matching(self.string, pattern)

    def longest_common_substring(self, string2):
        """
        Finds the longest common substring between the suffix tree's string and another string.

        Args:
            string2 (str): Second string for finding the longest common substring.

        Returns:
            str: Longest common substring. (returns empty string if no common substring found)
        """
        def longest_common_substring(string1, string2):
            common_substrings = []
            for i in range(len(string1)):
                for j in range(len(string2)):
                    k = 0
                    while (i + k < len(string1) and j + k < len(string2) and
                        string1[i + k] == string2[j + k]):
                        k += 1
                    if k > 0:
                        common_substrings.append(string1[i:i + k])
            if not common_substrings:                               # Check if the list is empty
                return ""                                           # Return empty string if no common substrings found
            return max(common_substrings, key=len)

        return longest_common_substring(self.string, string2)