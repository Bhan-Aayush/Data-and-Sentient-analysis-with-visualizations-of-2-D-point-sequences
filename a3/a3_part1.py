import random


def generate_text_uniform(model: dict[str, int], n: int) -> str:
    """Return a string of n randomly-generated words chosen from the given model.

    Each word in the returned string is separated by a single space.

    Preconditions:
        - n >= 0
        - model != {}
    """
    # Unpack model into two lists whose indexes correspond to one another
    words = []
    word_frequencies = []
    for word in model:
        words.append(word)
        word_frequencies.append(model[word])

    new_words = random.choices(words, weights=word_frequencies, k=n)
    return str.join(' ', new_words)


def create_model_uniform(text: str) -> dict[str, int]:
    """Return a model of the words in text.

    The model is a mapping of words to the number of times the word occurs in text. A "word"
    contains no spaces.

    This function should return model that is valid input to generate_text_uniform.

    Preconditions:
        - text != ''

    IMPLEMENTATION NOTE: Use the str.split method to get a list of words.
    """
    words = text.split()  # ["hello", "world", "how", "hello"] = {"hello": 2, "world": 1, "how": 1}
    word_to_frequency = {}

    for word in words:

        if word in word_to_frequency:
            word_to_frequency[word] += 1
        else:
            word_to_frequency[word] = 1

    return word_to_frequency


def run_example(filename: str, num_words: int) -> str:
    """Run an example to demonstrate random text generation with num_words words based on the data in filename."""
    
    with open(filename) as f:
        file_text = f.read()

    stripped_text = str.strip(file_text)  # str.strip removes leading/trailing whitespace
    model_from_file = create_model_uniform(stripped_text)
    generated_words = generate_text_uniform(model_from_file, num_words)

    return generated_words


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
