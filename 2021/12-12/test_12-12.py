import pytest
import part_one
import part_two

@pytest.fixture
def test_input():
    return "input-12-test"

@pytest.fixture
def test_larger_input():
    return "input-12-test-larger"
    
@pytest.fixture
def test_largest_input():
    return "input-12-test-largest"

def test_part_one_small(test_input):
    result = part_one.run(test_input)
    assert result == 10

def test_part_one_medium(test_larger_input):
    result = part_one.run(test_larger_input)
    assert result == 19

def test_part_one_large(test_largest_input):
    result = part_one.run(test_largest_input)
    assert result == 226

def test_part_two_small(test_input):
    result = part_two.run(test_input)
    assert result == 36

def test_part_two_medium(test_larger_input):
    result = part_two.run(test_larger_input)
    assert result == 103

def test_part_two_large(test_largest_input):
    result = part_two.run(test_largest_input)
    assert result == 3509