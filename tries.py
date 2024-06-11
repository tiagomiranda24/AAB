from graphviz import Digraph

class TriesNode:
    def __init__(self):
        """
        Initialize a TriesNode object.
        """
        self.children = [None] * 26
        self.isLeaf = False

class Tries:
    """
    Source: Modification of code provided by https://wangyy395.medium.com/implement-a-trie-in-python-e8dd5c5fde3a with newly added functions.
    """
    def __init__(self):
        """
        Initialize a Tries data structure.
        """
        self.root = TriesNode()

    ### Operation: Insertion ###
    def insert(self, word: str) -> None:
        """
        Inserts a word into the tries.

        Parameters:
            word (str): The word to insert into the tries.

        Returns:
            None
        """
        if not word.islower():
            raise ValueError("Invalid input: Word must consist only of lowercase letters.")
        
        current = self.root 
        for letter in word:
            index = ord(letter) - ord('a')
            if not current.children[index]:
                current.children[index] = TriesNode()
            current = current.children[index]
        current.isLeaf = True

    def insert_fromList(self, words: list) -> None:
        """
        Inserts a list of words into the tries.

        Parameters:
            words (list): A list of words to insert into the tries.

        Returns:
            None
        """
        for word in words:
            self.insert(word)

    def insert_fromInput(self) -> None:
        """
        Inserts words into the tries based on user input.

        Displays the number of total inputs and remaining inputs.

        Returns:
            None
        """
        try:
            num_words = int(input("Specify number of words to insert: "))
            for i in range(1, num_words + 1):
                word = input(f"Input word ({i} out of {num_words} inputs remaining): ")
                self.insert(word)
        except ValueError:
            print("Invalid input: Number of words must be an integer.")

    ### Operation: Deletion ###
    def delete(self, word: str) -> None:
        """
        Deletes a specified existing word from the tries.

        Parameters:
            word (str): The word to delete from the tries.

        Returns:
            None
        """
        # First, we need to check if the word exists in the tries
        if not self.search(word):
            raise ValueError(f"Deletion Failed: Input word '{word}' is not present in the Tries!")

        # Remaining deletion logic...
        current = self.root
        nodes_to_delete = []  # To store nodes that need to be deleted
        
        for letter in word:
            index = ord(letter) - ord('a')
            current = current.children[index]
            nodes_to_delete.append((current, index))

        # Mark the node corresponding to the last character of the word as not a leaf node
        current.isLeaf = False

        # Traverse back from the last character node towards the root and delete nodes that are not part of any other words
        while nodes_to_delete:
            node, index = nodes_to_delete.pop()
            if not any(node.children):
                parent_node, parent_index = nodes_to_delete[-1] if nodes_to_delete else (self.root, None)
                parent_node.children[parent_index] = None
            elif node.isLeaf:
                break

        print(f"Input word '{word}' was deleted from Tries successfully!")

    def delete_fromList(self, words: list) -> None:
        """
        Deletes a list of words from the tries.

        Parameters:
            words (list): A list of words to delete from the tries.

        Returns:
            None
        """
        for word in words:
            if self.search(word):
                self.delete(word)
            else:
                print(f"Deletion Failed: Input word '{word}' is not present in the Tries!")

    ### Operation: Searching ###
    def search(self, word: str) -> bool:
        """
        Returns if the word is in the tries.

        Parameters:
            word (str): The word to search for in the tries.

        Returns:
            bool: True if the word is in the tries, False otherwise.
        """
        current = self.root 
        for letter in word:
            index = ord(letter) - ord('a')
            if not current.children[index]:
                return False
            current = current.children[index]
        return current.isLeaf
    
    def search_fromList(self, words: list) -> dict:
        """
        Searches each word from the input list in the tries.

        Parameters:
            words (list): A list of words to search for in the tries.

        Returns:
            dict: A dictionary containing each word from the input list
                  as keys and their existence in the tries as values.
        """
        result = {}
        for word in words:
            result[word] = self.search(word)
        return result
    
    def search_fromInput(self) -> tuple:
        """
        Searches for words in the tries based on user input.
        Empty input or pressing the Escape key ends the input action, all the input words will be searched.

        Returns:
            tuple: A tuple containing two lists:
                - A list of words found in the tries.
                - A list of words not found in the tries.
        """
        found_words = []
        not_found_words = []

        while True:
            word = input("Input word to search (Press 'Enter' on an empty input to stop): ")
            if not word:
                break
            if self.search(word):
                found_words.append(word)
            else:
                not_found_words.append(word)

        print(f"Words found in Tries: {found_words}\nWords NOT found in Tries: {not_found_words}")
        return found_words, not_found_words
    
    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the tries that starts with the given prefix.

        Parameters:
            prefix (str): The prefix to search for in the tries.

        Returns:
            bool: True if there is any word in the tries that starts with the given prefix, False otherwise.
        """
        current = self.root 
        for letter in prefix:
            index = ord(letter) - ord('a')
            if not current.children[index]:
                return False
            current = current.children[index]
        return True

    def _collectAllWords(self, node: TriesNode, path: str, words: list) -> None:
        """
        Helper function to collect all words in the tries.

        Parameters:
            node (TriesNode): The current node being traversed.
            path (str): The current path of letters from the root to the current node.
            words (list): A list to collect all words found in the tries.

        Returns:
            None
        """
        if node.isLeaf:
            words.append(path)
        
        for index in range(26):
            if node.children[index] is not None:
                self._collectAllWords(node.children[index], path + chr(index + ord('a')), words)

    def getAllWords(self) -> list:
        """
        Returns all words stored in the tries.

        Returns:
            list: A list of all words stored in the tries.
        """
        words = []
        self._collectAllWords(self.root, "", words)
        return words
    
    def get_all_nodes(self) -> list:
        """
        Returns a list of all nodes in the tries.

        Returns:
            list: A list containing all nodes in the tries.
        """
        all_nodes = []

        # Helper function to perform DFS traversal
        def dfs(node):
            if node is None:
                return
            all_nodes.append(node)
            for child in node.children:
                dfs(child)

        dfs(self.root)
        return all_nodes
    
    def observeNodes(self, dot) -> None:
        """
        Observes all tries nodes along with the words they represent and their identifiers.

        Parameters:
            dot: The Digraph object from Graphviz used to represent the tries nodes.

        Returns:
            None
        """
        queue = [(self.root, "")]
        while queue:
            node, word = queue.pop(0)
            if node.isLeaf:
                dot.node(str(id(node)), label=f"{word}", shape='doublecircle')
            else:
                dot.node(str(id(node)), label=f"{word}")
            for i, child in enumerate(node.children):
                if child is not None:
                    queue.append((child, word + chr(i + ord('a'))))
                    dot.edge(str(id(node)), str(id(child)), label=chr(i + ord('a')))

    ### Operation: Visualization ###
    def visualize(self, filename=None):
        """
        Visualizes the tries using Graphviz and optionally saves the image as a PNG file.

        Parameters:
            filename (str, optional): If provided, saves the visualization as a PNG file with the given filename.
                If not provided, the visualization is displayed in the python notebook.

        Returns:
            None
        """
        dot = Digraph(comment='Tries')
        self.observeNodes(dot)
        if filename: 
            dot.render(filename, format='png', cleanup=True)
        else:
            display(dot) # type: ignore
