## Naive Algorithm
def naive(seq, pattern):
    n = len(seq)
    m = len(pattern)
    matches = []
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if seq[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)
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
    n = len(seq)
    m = len(pattern)
    matches = []

    # Calculate hash value for pattern and the first window of sequence
    pattern_hash = hash(pattern)
    window_hash = hash(seq[:m])

    # Check if hash values match and compare characters if they do
    for i in range(n - m + 1):
        if pattern_hash == window_hash and seq[i:i + m] == pattern:
            matches.append(i)
        if i < n - m:
            # Update rolling hash for the next window
            window_hash = hash(seq[i + 1:i + m + 1])
    return matches


## Boyer-Moore Algorithm
def boyer_moore(seq, pattern):
    """
    Sequence pattern searching that uses Bad Character Heuristic of Boyer-Moore Algorithm
    Source: Modification of code provided by https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
    """
    def badCharHeuristic(pattern):
        """
        Preprocessing function for Bad Character Heuristic in Boyer-Moore Algorithm
        """
        badChar = {}
        for i, char in enumerate(pattern):
            badChar[char] = i
        return badChar

    m = len(pattern)
    n = len(seq)
    badChar = badCharHeuristic(pattern)
    shift = 0
    occurrences = []

    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == seq[shift + j]:
            j -= 1
        if j == -1:
            occurrences.append(shift)
            shift += m - badChar.get(seq[shift + m], -1) if shift + m < n else 1
        else:
            shift += max(1, j - badChar.get(seq[shift + j], -1))
    return occurrences