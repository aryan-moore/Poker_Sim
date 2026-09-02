from poker.ranges import range
import pytest

def test_parse_hand_class():
    # Test parse_hand_class
    assert range.parse_hand_class("AKs") == ('A', 'K', 's')
    assert range.parse_hand_class("QJo") == ('Q', 'J', 'o')
    assert range.parse_hand_class("TT") == ('T', 'T', None)

def test_generate_combinations():
    # Test generate_combinations
    assert len(range.generate_combinations("AKs")) == 4
    assert len(range.generate_combinations("QJo")) == 12
    assert len(range.generate_combinations("TT")) == 6
    assert len(range.generate_combinations("AK")) == 16

def test_expand_plus_notation():
    # Test expand_plus_notation
    assert range.expand_plus_notation("ATs+") == ['ATs', 'AJs', 'AQs', 'AKs']
    assert range.expand_plus_notation("TT+") == ['TT', 'JJ', 'QQ', 'KK', 'AA']
    assert range.expand_plus_notation("K9o+") == ['K9o', 'KTo', 'KJo', 'KQo']

def test_duplicate_combinations():

    # AK already includes AKs, so this should still be 16
    assert range.count_combinations("AK, AKs") == 16


def test_parse_range():
    # Test parse_range
    assert range.parse_range("ATs+, K9o+, 22-66") == [
        'ATs', 'AJs', 'AQs', 'AKs',
        'K9o', 'KTo', 'KJo', 'KQo',
        '22', '33', '44', '55', '66'
    ]

def test_expand_interval_notation():

    assert range.expand_interval_notation("22-66") == [
        '22', '33', '44', '55', '66'
    ]

    assert range.expand_interval_notation("ATs-AQs") == [
        'ATs', 'AJs', 'AQs'
    ]

    assert range.expand_interval_notation("76s-T9s") == [
        '76s', '87s', '98s', 'T9s'
    ]

    assert range.expand_interval_notation("64s-T8s") == [
        '64s', '75s', '86s', '97s', 'T8s'
    ]

    assert range.expand_interval_notation("76-T9") == [
        '76', '87', '98', 'T9'
    ]

def test_invalid_intervals():

    with pytest.raises(ValueError):
        range.expand_interval_notation("T9s-76s")

    with pytest.raises(ValueError):
        range.expand_interval_notation("76s-T9o")

    with pytest.raises(ValueError):
        range.expand_interval_notation("76s-AQs")