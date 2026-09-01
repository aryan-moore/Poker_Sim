from poker.ranges import range

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

def test_parse_range():
    # Test parse_range
    assert range.parse_range("ATs+, K9o+, 22-66") == ['AKs', 'AQs', 'AJs', 'ATs', 'K9o', 'KTo', 'KJo', 'KQo', '22', '33', '44', '55', '66']