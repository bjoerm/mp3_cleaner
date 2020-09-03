from string_beautification import string_beautification


def test_string_beautification(input=False): # Switch this to True to easily test it also for that case.
    assert string_beautification("Test's test's test`s test´s test'S", remove_leading_the=input) == "Test's Test's Test's Test's test's", "Test hyphens"
    assert string_beautification("Ac/Dc AC/DC ac/dc guns 'n' roses", remove_leading_the=input) == "ACDC ACDC ACDC Guns 'n' Roses", "Test edge cases"
    assert string_beautification(" lost in      space Lost in Space ", remove_leading_the=input) == "Lost In Space Lost In Space", "Test spaces"
    assert string_beautification("where to? what now???", remove_leading_the=input) == "Where To What Now", "Question mark"
    assert string_beautification("I'am", remove_leading_the=input) == "I'am", "Test connected words"
    #assert string_beautification("data/now data\yesterday", remove_leading_the=False) == "Data-Now Data-Yesterday", "Test slash"
    assert string_beautification("A feat. B C featuring D E feat F", remove_leading_the=input) == "A Feat. B C Feat. D E Feat F", "Test Featuring"
    assert string_beautification("abC dEF ghi j5L", remove_leading_the=input) == "abC dEF Ghi j5L", "Test word contains capital letter - but not at beginning"



def test_string_beautification_leading_the(input=True): # Switch this to True to easily test it also for that case.
    assert string_beautification("The Beatles ", remove_leading_the=input) == "Beatles", "Leading The"
    assert string_beautification(" The Beatles ", remove_leading_the=input) == "Beatles", "Leading The"
    assert string_beautification("TheBeatles ", remove_leading_the=input) == "TheBeatles", "Leading The"
    assert string_beautification("The-Beatles ", remove_leading_the=input) == "The-Beatles", "Leading The"
    
