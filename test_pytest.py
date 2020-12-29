from beautify_string import beautify_string
from beautify_disc_and_track_number import beautify_disc_and_track_number
from beautify_date import beautify_date
from tag_management import TagManager

def test_string_beautification():
    """
    This tests the main/public method for beautifying strings. It contains all the (private) methods related to strings.
    """
    assert beautify_string.beautify_string("") == ""
    assert beautify_string.beautify_string("Test's test's test`s test´s test'S") == "Test's Test's Test's Test's test's", "Test hyphens"
    assert beautify_string.beautify_string("Ac/Dc AC/DC ac/dc guns 'n' roses") == "ACDC ACDC ACDC Guns 'n' Roses", "Test edge cases"
    assert beautify_string.beautify_string(" lost in      space  Lost in Space ") == "Lost In Space Lost In Space", "Test spaces"
    assert beautify_string.beautify_string("where to? what now???") == "Where To What Now", "Question mark"
    assert beautify_string.beautify_string("?!?") == "!", "Question mark"
    assert beautify_string.beautify_string("I'am") == "I'am", "Test connected words"
    assert beautify_string.beautify_string("data/now data\yesterday") == "Data-Now Data-Yesterday", "Test slash"
    assert beautify_string.beautify_string("A feat. B C featuring D E feat F") == "A Feat. B C Feat. D E Feat F", "Test Featuring"
    assert beautify_string.beautify_string("New Song Pt. 4 pt. 5 pt 6") == "New Song Part 4 Part 5 Pt 6", "Test Part"
    assert beautify_string.beautify_string("abC dEF ghi j5L") == "abC dEF Ghi j5L", "Test word contains capital letter - but not at beginning"
    assert beautify_string.beautify_string("m&m M&m") == "M+M M+m", "Test &"
    assert beautify_string.beautify_string("baum,stamm 10,5 Gerd,10 10,Gerd") == "Baum, Stamm 10,5 Gerd,10 10, Gerd", "Test comma and space"
    assert beautify_string.beautify_string(" ") == "", "Test empty 1"
    assert beautify_string.beautify_string("") == "", "Test empty 2"
    assert beautify_string.beautify_string("Nice Track REMIX") == "Nice Track Remix", "Test Remix suffix 1"
    assert beautify_string.beautify_string("Nice Track (REMIX)") == "Nice Track (Remix)", "Test Remix suffix 2"
    assert beautify_string.beautify_string("Nice Track LIVE") == "Nice Track Live", "Test Live suffix 1"
    assert beautify_string.beautify_string("Nice Track (LIVE)") == "Nice Track (Live)", "Test Live suffix 2"
    assert beautify_string.beautify_string(" Featuring Test") == "Feat. Test", "Test Feat. 1"
    assert beautify_string.beautify_string("Featuring Test") == "Feat. Test", "Test Feat. 2"
    assert beautify_string.beautify_string("Bomb Featuring Test") == "Bomb Feat. Test", "Test Feat. 3"
    assert beautify_string.beautify_string(" Pt. 2") == "Part 2", "Test Part 1"
    assert beautify_string.beautify_string("Pt. 2") == "Part 2", "Test Part 2"
    assert beautify_string.beautify_string("Bomb Pt. 2") == "Bomb Part 2", "Test Part 3"
    assert beautify_string.beautify_string("test III") == "Test III"
    assert beautify_string.beautify_string(None) == None, "Test none"


def test_string_beautification_leading_the(remove_leading_the=True): # Switch this to True to easily test it also for that case.
    assert beautify_string.beautify_string("", remove_leading_the=remove_leading_the) == ""
    assert beautify_string.beautify_string("The Beatles ", remove_leading_the=remove_leading_the) == "Beatles", "Test Leading The"
    assert beautify_string.beautify_string(" The Beatles ", remove_leading_the=remove_leading_the) == "Beatles", "Test Leading The"
    assert beautify_string.beautify_string("TheBeatles ", remove_leading_the=remove_leading_the) == "TheBeatles", "Test Leading The"
    assert beautify_string.beautify_string("The-Beatles ", remove_leading_the=remove_leading_the) == "The-Beatles", "Test Leading The"
    assert beautify_string.beautify_string(None, remove_leading_the=remove_leading_the) == None, "Test none"
    assert beautify_string.beautify_string("The", remove_leading_the=remove_leading_the) == "The", "Test for a band named 'The'"



def test_string_remove_whitespaces():
    assert beautify_string._remove_not_needed_whitespaces("") == ""
    assert beautify_string._remove_not_needed_whitespaces(" lost in      space  Lost In Space ") == "lost in space Lost In Space", "Test spaces"
    assert beautify_string._remove_not_needed_whitespaces(" Test") == "Test"
    assert beautify_string._remove_not_needed_whitespaces("Test ") == "Test"
    assert beautify_string._remove_not_needed_whitespaces(" Test ") == "Test"
    assert beautify_string._remove_not_needed_whitespaces(" 123 456 ") == "123 456"
    assert beautify_string._remove_not_needed_whitespaces(" ") == ""
    assert beautify_string._remove_not_needed_whitespaces("  ") == ""



def test_string_unify_quotation_marks_and_accents():
    assert beautify_string._unify_quotation_marks_and_accents("") == ""
    assert beautify_string._unify_quotation_marks_and_accents('"Great Song"') == "'Great Song'", "Quotation marks"
    assert beautify_string._unify_quotation_marks_and_accents("Tim´s") == "Tim's", "Accents"
    assert beautify_string._unify_quotation_marks_and_accents("Tim`s") == "Tim's", "Accents"


def test_string_beautify_colons():
    assert beautify_string._beautify_colons("") == ""
    assert beautify_string._beautify_colons("Deus Ex: Human Revolution") == "Deus Ex - Human Revolution", "Colon followed by whitespace"
    assert beautify_string._beautify_colons("He: Hello") == "He - Hello", "Colon followed by whitespace"
    assert beautify_string._beautify_colons("Deus:Ex") == "Deus-Ex", "Colon followed by non-whitespace 1"
    assert beautify_string._beautify_colons("12:34") == "12-34", "Colon followed by non-whitespace 2"
    assert beautify_string._beautify_colons(" : ") == " - ", "Colon surrounded by whitespace"
    assert beautify_string._beautify_colons(":Ex") == "-Ex", "Colon surrounded by whitespace"
    assert beautify_string._beautify_colons("Ex:") == "Ex-", "Colon surrounded by whitespace"


def test_string_replace_special_characters():
    assert beautify_string._replace_special_characters("") == ""
    assert beautify_string._replace_special_characters(";") == ","
    assert beautify_string._replace_special_characters("tl;dr") == "tl,dr"
    assert beautify_string._replace_special_characters("\\") == "-"
    assert beautify_string._replace_special_characters("abc\\def") == "abc-def"
    assert beautify_string._replace_special_characters("/") == "-"
    assert beautify_string._replace_special_characters("abc/def") == "abc-def"
    assert beautify_string._replace_special_characters("?") == ""
    assert beautify_string._replace_special_characters("WTF?") == "WTF"
    assert beautify_string._replace_special_characters("&") == "+"
    assert beautify_string._replace_special_characters("C&A") == "C+A"
    

def test_string_fill_missing_space_after_comma():
    assert beautify_string._fill_missing_space_after_comma("") == ""
    assert beautify_string._fill_missing_space_after_comma("baum,stamm") == "baum, stamm"
    assert beautify_string._fill_missing_space_after_comma("10,5") == "10,5"    
    assert beautify_string._fill_missing_space_after_comma("5,neu") == "5, neu"
    assert beautify_string._fill_missing_space_after_comma("neu,5") == "neu, 5"

def test_string_remove_leading_the():
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="") == ""
    assert beautify_string._remove_leading_the(remove_leading_the=False, text="") == ""
    assert beautify_string._remove_leading_the(remove_leading_the=False, text="The Beatles") == "The Beatles"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="The Beatles") == "Beatles"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="The-Beatles") == "The-Beatles"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="Therapy") == "Therapy"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="The 182") == "182"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="T H E") == "T H E"
    assert beautify_string._remove_leading_the(remove_leading_the=True, text="The") == "The"



def test_string_deal_with_special_words():
    assert beautify_string._deal_with_special_words_and_bands(text="") == ""
    assert beautify_string._deal_with_special_words_and_bands(text=" Featuring ") == " Feat. "
    assert beautify_string._deal_with_special_words_and_bands(text="Featuring ") == "Feat. "
    assert beautify_string._deal_with_special_words_and_bands(text="Featuring") == "Featuring"
    assert beautify_string._deal_with_special_words_and_bands(text="(Featuring)") == "(Featuring)"
    assert beautify_string._deal_with_special_words_and_bands(text="(Featuring abc)") == "(Feat. abc)"
    assert beautify_string._deal_with_special_words_and_bands(text=" FEATURING ") == " Feat. "
    assert beautify_string._deal_with_special_words_and_bands(text="Test Featuring") == "Test Featuring"
    assert beautify_string._deal_with_special_words_and_bands(text=" Pt. 1 ") == " Part 1 "
    assert beautify_string._deal_with_special_words_and_bands(text=" Pt. 1") == " Part 1"
    assert beautify_string._deal_with_special_words_and_bands(text="Pt. 1 ") == "Part 1 "
    assert beautify_string._deal_with_special_words_and_bands(text="Pt. 1") == "Part 1"
    assert beautify_string._deal_with_special_words_and_bands(text="pt. 1") == "Part 1"
    assert beautify_string._deal_with_special_words_and_bands(text="copt. 1") == "copt. 1"
    assert beautify_string._deal_with_special_words_and_bands(text="remix") == "Remix"
    assert beautify_string._deal_with_special_words_and_bands(text="REMIX") == "Remix"
    assert beautify_string._deal_with_special_words_and_bands(text="cremeremix") == "cremeremix"
    assert beautify_string._deal_with_special_words_and_bands(text="best remix") == "best Remix"
    assert beautify_string._deal_with_special_words_and_bands(text="(remix)") == "(Remix)"
    assert beautify_string._deal_with_special_words_and_bands(text=" (remix)") == " (Remix)"
    assert beautify_string._deal_with_special_words_and_bands(text="(best remix)") == "(best Remix)"
    assert beautify_string._deal_with_special_words_and_bands(text="live") == "Live"
    assert beautify_string._deal_with_special_words_and_bands(text="(live)") == "(Live)"
    assert beautify_string._deal_with_special_words_and_bands(text="LIVE") == "Live"
    assert beautify_string._deal_with_special_words_and_bands(text="sunlive") == "sunlive"



def test_string_capitalize_string():
    assert beautify_string._capitalize_string(text="") == ""
    assert beautify_string._capitalize_string(text="Bernd's") == "Bernd's"
    assert beautify_string._capitalize_string(text="Bernd's Great Song") == "Bernd's Great Song"
    assert beautify_string._capitalize_string(text="Bernd's Great Song") == "Bernd's Great Song"
    assert beautify_string._capitalize_string(text="DMX") == "DMX"
    assert beautify_string._capitalize_string(text="DMX is testing") == "DMX Is Testing"
    assert beautify_string._capitalize_string(text="bmX bike") == "bmX Bike"



def test_track_number_beautification():
    """
    This tests the main/public method for beautifying track numbers. It contains all the (private) methods related to track numbers.
    """
    assert beautify_disc_and_track_number.beautify_track_number(track_number="01", helper_length_max=1, minimum_length=1) == "1", "Test removing existing leading zero 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="", helper_length_max=1, minimum_length=1) == ""
    assert beautify_disc_and_track_number.beautify_track_number(track_number="1", helper_length_max=1, minimum_length=1) == "1", "Test normal"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="1", helper_length_max=2, minimum_length=2) == "01", "Test leading zeros 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="1", helper_length_max=3, minimum_length=2) == "001", "Test leading zeros 2"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="11", helper_length_max=2, minimum_length=2) == "11", "Test leading zeros 3"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="11", helper_length_max=3, minimum_length=2) == "011", "Test leading zeros 4"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="1/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="01/16", helper_length_max=2, minimum_length=2) == "01", "Test track number slash tracks on disc 2"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="01", helper_length_max=2, minimum_length=2) == "01", "Test existing leading zero 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="01", helper_length_max=3, minimum_length=2) == "001", "Test existing leading zero 2"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="", helper_length_max=3, minimum_length=2) == "", "Test empty input"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="01", helper_length_max=1, minimum_length=1) == "1", "Test removing existing leading zero 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number="001", helper_length_max=2, minimum_length=2) == "01", "Test removing existing leading zeros 2"
    assert beautify_disc_and_track_number.beautify_track_number(track_number=" 1", helper_length_max=1, minimum_length=1) == "1", "Test spaces 1"
    assert beautify_disc_and_track_number.beautify_track_number(track_number=" 1 ", helper_length_max=1, minimum_length=1) == "1", "Test spaces 2"
    assert beautify_disc_and_track_number.beautify_track_number(track_number=None, helper_length_max=1, minimum_length=1) == None, "Test none"



def test_mp3_extract_track_number_from_slash_format():
    """
    Testing the regex that extracts the track number from potential 'slash format'.
    """
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("") == ""
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("01") == "01"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("01/") == "01"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("01/16") == "01"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("1") == "1"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("1/") == "1"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format("1/16") == "1"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format(1) == "1"
    assert beautify_disc_and_track_number.extract_track_number_from_slash_format(None) == None




def test_mp3_tags_has_cd_string_in_folder_name():
    """
    Testing the complex regex realted to strings that hint for multiple CDs in the folder name.
    """
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd 1") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd3") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd  2asd") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd  2 asd") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd2aasdfsd") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("12_cd2aasdfsd") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("asd cd2") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("2cd") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("2013-2CD-2013-C4") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("_cd2") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name(",cd2 ") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("-23") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("192cd2 ") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("-cd23") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("-1cd-") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("- 1 cd -") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name(" cd 2 ") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("_1 cd_") == True
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("2cdaasdf") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("cd123455") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name("ACDC 2010") == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name(None) == False
    assert beautify_disc_and_track_number.has_cd_string_in_folder_name(50) == False





def test_mp3_tags_extract_year():
    """
    Testing the regex that extracts the year (YYYY).
    """
    assert beautify_date.extract_year("") == ""
    assert beautify_date.extract_year("1999-12-12") == "1999"
    assert beautify_date.extract_year("1999") == "1999"
    assert beautify_date.extract_year("20-12-1999") == "1999"
    assert beautify_date.extract_year("1999-10") == "1999"
    assert beautify_date.extract_year("1999-October") == "1999"
    assert beautify_date.extract_year("1999-H1") == "1999"
    assert beautify_date.extract_year("11.11.1999") == "1999"
    assert beautify_date.extract_year("2020-12-12") == "2020"
    assert beautify_date.extract_year("2020") == "2020"
    assert beautify_date.extract_year("20-12-2020") == "2020"
    assert beautify_date.extract_year("2020-10") == "2020"
    assert beautify_date.extract_year("2020-October") == "2020"
    assert beautify_date.extract_year("2020-H1") == "2020"
    assert beautify_date.extract_year("11.11.2020") == "2020"
    assert beautify_date.extract_year("11.11.11") == "11.11.11"
    assert beautify_date.extract_year("11-11-11") == "11-11-11"
    assert beautify_date.extract_year(" 1999") == "1999"
    assert beautify_date.extract_year(" 1999 ") == "1999"
    assert beautify_date.extract_year("1999 ") == "1999"
    assert beautify_date.extract_year("20/12/2020") == "2020"
    assert beautify_date.extract_year("99") == "99"
    assert beautify_date.extract_year("October '99") == "October '99" # TODO Adjust this case? But should be a total edge case possibly not worth the effort.
    assert beautify_date.extract_year(2020) == "2020"
    assert beautify_date.extract_year(1980) == "1980"
    assert beautify_date.extract_year(None) == None


