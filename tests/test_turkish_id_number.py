from turkish_validator.tr_validator import is_valid_turkish_id

def test_is_valid_turkish_id():
    assert is_valid_turkish_id('123') == False

