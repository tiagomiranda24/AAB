## Naive Algorithm
def naive(seq, pattern):
    """
    Naive string matching algorithm to find all occurrences of a pattern in a given sequence.
    Source: Attempted implementation of Naive Algorithm following steps provided by professor Rui Mendes

    Args:
        seq (str): The sequence in which to search for the pattern.
        pattern (str): The pattern to search for within the sequence.

    Returns:
        list: A list of starting indices where the pattern is found in the sequence.
    """
    n = len(seq)                            # Length of the sequence
    m = len(pattern)                        # Length of the pattern
    matches = []                            # List to store the starting indices of matches
    
    # Iterate over each possible starting position in the sequence
    for i in range(n - m + 1):
        match = True                        # Assume a match unless proven otherwise
    
        # Check each character in the pattern
        for j in range(m):
            if seq[i + j] != pattern[j]:
                match = False               # Mismatch found, so no match at this position
                break
        
        if match:
            matches.append(i)               # Add the starting index to the list of matches
    return matches


## Knuth-Morris-Pratt (KMP) Algorithm
def KMP(seq, pattern):
    """
    Perform pattern search using Knuth-Morris-Pratt (KMP) algorithm.
    """
    if not pattern or not seq:                  # Check if either pattern or sequence is empty
        return []

    def lps_array(pattern):
        """
        Compute the Longest Prefix Suffix (LPS) array for the given pattern.
        """
        lps = [0] * len(pattern)                # Initialize LPS array with zeros
        j = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[j]:
                j += 1
                lps[i] = j
                i += 1
            else:
                if j != 0:
                    j = lps[j - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(seq)
    m = len(pattern)

    lps = lps_array(pattern)                    # Compute LPS array for the pattern

    i = 0                                       # Index for seq[]
    j = 0                                       # Index for pattern[]
    indices = []                                # List to store the indices where pattern is found
    while i < n:
        if pattern[j] == seq[i]:
            i += 1
            j += 1
        if j == m:
            indices.append(i - j)               # Adds the index where pattern starts in the sequence
            j = lps[j - 1] if j > 0 else 0      # Updates j using the LPS array
        elif i < n and pattern[j] != seq[i]:
            if j != 0:
                j = lps[j - 1]                  # Updates j using the LPS array
            else:
                i += 1
    return indices


## Rabin-Karp Algorithm
def rabin_karp(seq, pattern):
    """
    Rabin-Karp string matching algorithm to find all occurrences of a pattern in a given sequence.
    
    Args:
        seq (str): The sequence in which to search for the pattern.
        pattern (str): The pattern to search for within the sequence.
    
    Returns:
        list: A list of starting indices where the pattern is found in the sequence.
    """
    n = len(seq)        # Length of the sequence
    m = len(pattern)    # Length of the pattern
    matches = []        # List to store the starting indices of matches

    # Calculate hash value for the pattern and the first window of the sequence
    pattern_hash = hash(pattern)
    window_hash = hash(seq[:m])

    # Iterate over each possible starting position in the sequence
    for i in range(n - m + 1):
        # Check if hash values match and compare characters if they do
        if pattern_hash == window_hash and seq[i:i + m] == pattern:
            matches.append(i)
        
        # Update rolling hash for the next window if not at the end of the sequence
        if i < n - m:
            window_hash = hash(seq[i + 1:i + m + 1])
    return matches



## Boyer-Moore Algorithm
def boyer_moore(seq, pattern):
    """
    Boyer-Moore string matching algorithm to find all occurrences of a pattern in a given sequence.
    This implementation uses the Bad Character Heuristic.
    Source: Modification of code provided by https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/

    Args:
        seq (str): The sequence in which to search for the pattern.
        pattern (str): The pattern to search for within the sequence.

    Returns:
        list: A list of starting indices where the pattern is found in the sequence.
    """
    def badCharHeuristic(pattern):
        """
        Preprocessing function for the Bad Character Heuristic.
        Constructs a dictionary that maps each character in the pattern to its last occurrence index.
        
        Args:
            pattern (str): The pattern to preprocess.
        
        Returns:
            dict: A dictionary with characters as keys and their last occurrence index in the pattern as values.
        """
        badChar = {}
        for i, char in enumerate(pattern):
            badChar[char] = i
        return badChar

    m = len(pattern)                        # Length of the pattern
    n = len(seq)                            # Length of the sequence
    badChar = badCharHeuristic(pattern)     # Preprocess the pattern to get the bad character heuristic table
    shift = 0                               # Shift of the pattern with respect to the sequence
    occurrences = []                        # List to store the starting indices of matches

    while shift <= n - m:
        j = m - 1                           # Start from the end of the pattern
        
        # Move backwards through the pattern as long as characters are matching
        while j >= 0 and pattern[j] == seq[shift + j]:
            j -= 1
        
        # If the pattern is found, add the shift index to the occurrences list
        if j == -1:
            occurrences.append(shift)
            shift += m - badChar.get(seq[shift + m], -1) if shift + m < n else 1
        else:
            # Calculate the shift based on the bad character heuristic
            shift += max(1, j - badChar.get(seq[shift + j], -1))
    return occurrences