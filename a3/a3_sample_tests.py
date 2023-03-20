import a3_part1
import a3_part2


class TestCreateModelUniform:
    """Some example tests for A3 Part 1 - create_model_uniform."""

    def test_two_words(self) -> None:
        """Test that the correct model is produced when the text contains two words."""
        test_text = 'Hello, World!'
        expected = {'Hello,': 1, 'World!': 1}

        assert a3_part1.create_model_uniform(test_text) == expected


class TestUpdateFollowList:
    """Some example tests for A3 Part 2 - update_follow_list."""

    def test_empty(self) -> None:
        """Test that an empty dictionary is mutated correctly."""
        test_model = {}
        a3_part2.update_follow_list(test_model, 'I', 'like')

        assert test_model == {'I': ['like']}

    def test_not_empty_key_exists(self) -> None:
        """Test that a non-empty dictionary is mutated correctly when the key already exists."""
        test_model = {'I': ['like']}
        a3_part2.update_follow_list(test_model, 'I', 'really')

        assert test_model == {'I': ['like', 'really']}

    def test_not_empty_key_does_not_exist(self) -> None:
        """Test that a non-empty dictionary is mutated correctly when the key already exists."""
        # TODO: Consider completing this test based on its docstring
        test_model = {'I': ['like']}
        a3_part2.update_follow_list(test_model, 'like', 'chocolate')

        assert test_model == {'I': ['like'], 'like': ['chocolate']}


class TestCreateModelOwc:
    """Some example tests for A3 Part 2 - create_model_owc."""

    def test_two_words(self) -> None:
        """Test that the correct model is produced when the text contains two words."""
        test_text = 'Hello, World!'

        expected_word_count = 2
        expected_model = {'Hello,': ['World!']}

        actual_word_count, actual_model = a3_part2.create_model_owc(test_text)
        assert actual_word_count == expected_word_count
        assert actual_model == expected_model


class TestChooseFromKeys:
    """Some example tests for A3 Part 2 - choose_from_keys."""

    def test_one_possibility(self) -> None:
        """Test that the only possible key is returned."""
        test_transitions = {'The': ['cat']}

        assert a3_part2.choose_from_keys(test_transitions) == 'The'

    def test_two_possibilities(self) -> None:
        """Test that one of two possible keys is returned."""
        test_transitions = {'The': ['cat'], 'cat': ['in']}
        possibilities = {'The', 'cat'}

        assert a3_part2.choose_from_keys(test_transitions) in possibilities


class TestChooseFromFollowList:
    """Some example tests for A3 Part 2 - choose_from_follow_list."""

    def test_one_possibility(self) -> None:
        """Test that the only possible value for a key is returned."""
        test_transitions = {'The': ['cat'], 'cat': ['in'], 'in': ['the'], 'the': ['hat.']}

        assert a3_part2.choose_from_follow_list('The', test_transitions) == 'cat'

    def test_one_possibility_mutation(self) -> None:
        """Test that the dictionary is mutated correctly."""
        test_transitions = {'The': ['cat'], 'cat': ['in'], 'in': ['the'], 'the': ['hat.']}
        a3_part2.choose_from_follow_list('The', test_transitions)

        assert test_transitions == {'cat': ['in'], 'in': ['the'], 'the': ['hat.']}


if __name__ == '__main__':
    import pytest
    pytest.main(['a3_example_tests.py'])
