import random

def update_follow_list(model: dict[str, list[str]], word: str, follow_word: str) -> None:
    """Add follow_word and, when applicable, word to model.

    If word is not already present in model, add it to the model with the follow list
    [follow_word]. Otherwise, add follow_word to the follow list of word.
    """
    if word not in model:
        follow_list = [follow_word]
        model[word] = follow_list
    else:
        list.append(model[word], follow_word)


def create_model_owc(text: str) -> tuple[int, dict[str, list[str]]]:
    """Return a tuple of the number of words in text and one-word context model of the given text,
    as described in the handout.

    Preconditions:
        - text != ''
        - len(str.split(text)) > 1
    """
    split_text = str.split(text)
    text_counter_without_last_word = 1
    context_model = {}

    for i in range(0, len(split_text) - 1):
        text_counter_without_last_word = text_counter_without_last_word + 1
        update_follow_list(context_model, split_text[i], split_text[i + 1])

    return (text_counter_without_last_word, context_model)


def choose_from_keys(transitions: dict[str, list[str]]) -> str:
    """Return a random key from transitions.

    Preconditions:
        - transitions != {}
    """
    keys_choice_list = list(transitions.keys())
    return random.choice(keys_choice_list)


def choose_from_follow_list(key: str, transitions: dict[str, list[str]]) -> str:
    """Return a random word from the follow list in transitions that is associated with key.

    Also remove one occurrence of the random word from the follow list. If the follow list is then
    empty, remove the key-value pair from transitions.

    Preconditions:
        - transitions != {}
        - key in transitions
        - transitions[key] != []
    """
    follow_choice_index = random.choice(range(0, len(transitions[key])))
    follow_choice = transitions[key][follow_choice_index]
    follow_choice_return_val = follow_choice

    if transitions[key] == []:
        transitions.pop(key)

    transitions[key].pop(follow_choice_index)

    return follow_choice_return_val


def generate_text_owc(count: int, transitions: dict[str, list[str]]) -> str:
    """Return a string containing (count - 1) randomly generated words based on the data in
    transitions, which maps words to a list of words that follow it.

    Preconditions:
        - model is in the format described by the assignment handout
    """
    # ACCUMULATOR: a list of the randomly-generated words so far
    words_so_far = []

    # We've provided this template as a starting point; you may modify it as necessary.
    next_word = ''

    for i in range(0, count - 1):
        if i == 0:
            chosen_key = choose_from_keys(transitions)
            list.append(words_so_far, chosen_key)
            next_word = transitions[words_so_far[i]][0]
        elif i < count - 1:
            if words_so_far[i - 1] not in transitions:
                chosen_key = next_word
            elif len(transitions[words_so_far[i - 1]]) == 1:
                next_word = transitions[words_so_far[i - 1]][0]
                chosen_key = words_so_far[i - 1]
            else:
                chosen_key = words_so_far[i - 1]
            chosen_transition = choose_from_follow_list(chosen_key, transitions)
            list.append(words_so_far, chosen_transition)
        else:
            var = [transitions[x] for x in transitions]
            chosen_transition = var[0]
            list.append(words_so_far, chosen_transition)

    return str.join(' ', words_so_far)


def run_example(filename: str) -> str:
    """Run an example to demonstrate random text generation based on the data in filename."""
    
    with open(filename) as f:
        file_text = f.read()

    stripped_text = str.strip(file_text)  # str.strip removes leading/trailing whitespace
    word_count, transition_model = create_model_owc(stripped_text)
    generated_words = generate_text_owc(word_count, transition_model)

    return generated_words


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
