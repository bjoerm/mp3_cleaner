from string_beautification import string_beautification
from track_number_beautification import track_number_beautification

def test_string_beautification(): # Switch this to True to easily test it also for that case.
    assert string_beautification("Test's test's test`s test´s test'S") == "Test's Test's Test's Test's test's", "Test hyphens"
    assert string_beautification("Ac/Dc AC/DC ac/dc guns 'n' roses") == "ACDC ACDC ACDC Guns 'n' Roses", "Test edge cases"
    assert string_beautification(" lost in      space  Lost in Space ") == "Lost In Space Lost In Space", "Test spaces"
    assert string_beautification("where to? what now???") == "Where To What Now", "Question mark"
    assert string_beautification("I'am") == "I'am", "Test connected words"
    #assert string_beautification("data/now data\yesterday", remove_leading_the=False) == "Data-Now Data-Yesterday", "Test slash"
    assert string_beautification("A feat. B C featuring D E feat F") == "A Feat. B C Feat. D E Feat F", "Test Featuring"
    assert string_beautification("New Song Pt. 4 pt. 5 pt 6") == "New Song Part 4 Part 5 Pt 6", "Test Part"
    assert string_beautification("abC dEF ghi j5L") == "abC dEF Ghi j5L", "Test word contains capital letter - but not at beginning"
    assert string_beautification("m&m M&m") == "M+M M+m", "Test &"
    assert string_beautification("baum,stamm 10,5 Gerd,10 10,Gerd") == "Baum, Stamm 10,5 Gerd,10 10, Gerd", "Test comma and space"
    assert string_beautification(" ") == "", "Test empty 1"
    assert string_beautification("") == "", "Test empty 2"



def test_string_beautification_leading_the(input=True): # Switch this to True to easily test it also for that case.
    assert string_beautification("The Beatles ", remove_leading_the=input) == "Beatles", "Test Leading The"
    assert string_beautification(" The Beatles ", remove_leading_the=input) == "Beatles", "Test Leading The"
    assert string_beautification("TheBeatles ", remove_leading_the=input) == "TheBeatles", "Test Leading The"
    assert string_beautification("The-Beatles ", remove_leading_the=input) == "The-Beatles", "Test Leading The"



def test_track_number_beautification():
    assert track_number_beautification(track_number="1", helper_length_max=1, minimum_length=1) == "1", "Test normal"
    assert track_number_beautification(track_number="1", helper_length_max=2, minimum_length=2) == "01", "Test leading zeros 1"
    assert track_number_beautification(track_number="1", helper_length_max=3, minimum_length=2) == "001", "Test leading zeros 2"
    assert track_number_beautification(track_number="11", helper_length_max=2, minimum_length=2) == "11", "Test leading zeros 3"
    assert track_number_beautification(track_number="11", helper_length_max=3, minimum_length=2) == "011", "Test leading zeros 4"
    assert track_number_beautification(track_number="1/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 1"
    assert track_number_beautification(track_number="01/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 2"
    assert track_number_beautification(track_number="01", helper_length_max=2, minimum_length=2) == "01", "Test existing leading zero 1"
    assert track_number_beautification(track_number="01", helper_length_max=3, minimum_length=2) == "001", "Test existing leading zero 2"
    assert track_number_beautification(track_number="", helper_length_max=3, minimum_length=2) == "", "Test existing leading zero 2"
    # assert track_number_beautification(track_number="01", helper_length_max=1) == "1", "Test removing existing leading zero"

