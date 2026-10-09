"""
Text Analyzer

This program analyzes a passage of text and prints:
    * the number of sentences in the passage
    * the total number of words and the number of unique words
    * the 5 most frequent words and how many times each one appears
    * whether each word in a list of search words appears in the passage
      (using binary search on the sorted list of unique words)

Words are compared case-insensitively with leading/trailing punctuation
removed, so "Ram," "RAM" and "ram" all count as the same word.
Every sentence in the passage ends with a period.
"""

import string


PASSAGE = """Colorado State University is located in Fort Collins. The campus
mascot is CAM the Ram. Students at the university enjoy the mountains, the
river, and the trails near campus. Every fall, students and alumni cheer for
the Rams at Canvas Stadium. The university is known for engineering,
veterinary medicine, and agriculture. Many students study computer science,
and the computer science department is in the Computer Science Building."""

SEARCH_WORDS = ["Rams", "university", "Trails", "python", "agriculture", "Fort"]


def clean_word(word):
    """Return the word in lowercase with leading/trailing punctuation removed."""
    word = word.strip(string.punctuation)
    word = word.lower()
    return word


def get_words(text):
    """Return a list of all cleaned words in the text, in order."""
    words = []
    for token in text.split():
        cleaned = clean_word(token)
        if cleaned != "":
            words.append(cleaned)
    return words


def count_sentences(text):
    """Return the number of sentences in the text."""
    return len(text.split("."))


def count_words(words):
    """Return a dictionary mapping each word to the number of times it appears."""
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def most_common(counts, n):
    """Return a list of the n (word, count) pairs with the highest counts."""
    pairs = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    return pairs[:n]


def binary_search(sorted_words, target):
    """Return the index of target in sorted_words, or -1 if it is not found."""
    low = 0
    high = len(sorted_words) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_words[mid] == target:
            return mid
        elif sorted_words[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def main():
    words = get_words(PASSAGE)
    counts = count_words(words)
    unique_words = sorted(counts.keys())

    print(f"Sentences:    {count_sentences(PASSAGE)}")
    print(f"Total words:  {len(words)}")
    print(f"Unique words: {len(unique_words)}")

    print()
    print("Top 5 words:")
    for word, count in most_common(counts, 5):
        print(f"  {word:<12}{count}")

    print()
    print("Word search:")
    for target in SEARCH_WORDS:
        index = binary_search(unique_words, clean_word(target))
        if index != -1:
            print(f"  '{target}' found at position {index}")
        else:
            print(f"  '{target}' was not found")


if __name__ == "__main__":
    main()
