# TODO Add tests for the whole beautify_tags that contain real input (a list of dicts (which contain tags)) for testing of real life scenarios like a folder without any track numbers.

# TODO Check usage of fixtures: https://youtu.be/WkUBx3g2QfQ?t=5458

from beautify_single_string import beautify_string


def test_string_beautification():
    """
    This tests the main/public method for beautifying strings. It contains all the (private) methods related to strings.
    """
    assert beautify_string.beautify_string("") == ""
    assert beautify_string.beautify_string("Test's test's test`s test´s") == "Test's Test's Test's Test's", "Test accents"
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
    assert beautify_string.beautify_string("baum,stamm") == "Baum, Stamm", "Test comma and space"
    assert beautify_string.beautify_string("10,5") == "10,5", "Test comma and space"
    assert beautify_string.beautify_string("Gerd,10") == "Gerd, 10", "Test comma and space"
    assert beautify_string.beautify_string("10,Gerd") == "10, Gerd", "Test comma and space"
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
    assert beautify_string.beautify_string("äh") == "Äh"
    assert beautify_string.beautify_string("äh !") == "Äh !"
    assert beautify_string.beautify_string("your's") == "Your's"
    assert beautify_string.beautify_string("Capone 'n' Noreaga") == "Capone 'n' Noreaga"
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
    assert beautify_string._beautify_colons("Deus : Ex") == "Deus - Ex"
    assert beautify_string._beautify_colons("Deus: Ex") == "Deus - Ex"
    assert beautify_string._beautify_colons("Über:Über") == "Über-Über"
    assert beautify_string._beautify_colons("Über: Über") == "Über - Über"
    assert beautify_string._beautify_colons("Ü: Ü") == "Ü - Ü"
    assert beautify_string._beautify_colons("ß: ß") == "ß - ß"
    assert beautify_string._beautify_colons("é: é") == "é - é"
    assert beautify_string._beautify_colons("Deus:Ex") == "Deus-Ex", "Colon followed by non-whitespace 1"
    assert beautify_string._beautify_colons("12:34") == "12-34", "Colon followed by non-whitespace 2"
    assert beautify_string._beautify_colons(" : ") == " - ", "Colon surrounded by whitespace"
    assert beautify_string._beautify_colons(":Ex") == "-Ex", "Colon surrounded by whitespace"
    assert beautify_string._beautify_colons("Ex:") == "Ex-", "Colon surrounded by whitespace"
    assert beautify_string._beautify_colons("Ex:") == "Ex-", "Colon surrounded by whitespace"

def test_enforce_round_brackets():
    assert beautify_string._enforce_round_brackets("(Test)") == "(Test)"
    assert beautify_string._enforce_round_brackets("(Test]") == "(Test)"
    assert beautify_string._enforce_round_brackets("[Test]") == "(Test)"
    assert beautify_string._enforce_round_brackets("[[Test]]") == "(Test)"
    assert beautify_string._enforce_round_brackets("{Test}") == "(Test)"
    assert beautify_string._enforce_round_brackets("⟨Test⟩") == "(Test)"



def test_unify_hyphens():
    assert beautify_string._unify_hyphens("Test-Case") == "Test-Case"
    assert beautify_string._unify_hyphens("Test―Case") == "Test-Case"
    assert beautify_string._unify_hyphens("Test‒Case") == "Test-Case"

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
    assert beautify_string._deal_with_special_words_and_bands("") == ""
    assert beautify_string._deal_with_special_words_and_bands(" Featuring ") == " Feat. "
    assert beautify_string._deal_with_special_words_and_bands("Featuring ") == "Feat. "
    assert beautify_string._deal_with_special_words_and_bands("Featuring") == "Featuring"
    assert beautify_string._deal_with_special_words_and_bands("(Featuring)") == "(Featuring)"
    assert beautify_string._deal_with_special_words_and_bands("(Featuring abc)") == "(Feat. abc)"
    assert beautify_string._deal_with_special_words_and_bands(" FEATURING ") == " Feat. "
    assert beautify_string._deal_with_special_words_and_bands("Test Featuring") == "Test Featuring"
    assert beautify_string._deal_with_special_words_and_bands(" Pt. 1 ") == " Part 1 "
    assert beautify_string._deal_with_special_words_and_bands(" Pt. 1") == " Part 1"
    assert beautify_string._deal_with_special_words_and_bands("Pt. 1 ") == "Part 1 "
    assert beautify_string._deal_with_special_words_and_bands("Pt. 1") == "Part 1"
    assert beautify_string._deal_with_special_words_and_bands("pt. 1") == "Part 1"
    assert beautify_string._deal_with_special_words_and_bands("copt. 1") == "copt. 1"
    assert beautify_string._deal_with_special_words_and_bands("remix") == "Remix"
    assert beautify_string._deal_with_special_words_and_bands("REMIX") == "Remix"
    assert beautify_string._deal_with_special_words_and_bands("cremeremix") == "cremeremix"
    assert beautify_string._deal_with_special_words_and_bands("best remix") == "best Remix"
    assert beautify_string._deal_with_special_words_and_bands("(remix)") == "(Remix)"
    assert beautify_string._deal_with_special_words_and_bands(" (remix)") == " (Remix)"
    assert beautify_string._deal_with_special_words_and_bands("(best remix)") == "(best Remix)"
    assert beautify_string._deal_with_special_words_and_bands("live") == "Live"
    assert beautify_string._deal_with_special_words_and_bands("(live)") == "(Live)"
    assert beautify_string._deal_with_special_words_and_bands("LIVE") == "Live"
    assert beautify_string._deal_with_special_words_and_bands("sunlive") == "sunlive"



def test_string_capitalize_string():
    """
    Remember that this shall not touch a string (part (surrounded by spaces)), if that has already any capital letter in it.
    """
    assert beautify_string._capitalize_string("test's") == "Test's"
    assert beautify_string._capitalize_string("Bernd's") == "Bernd's"
    assert beautify_string._capitalize_string("test'N") == "test'N"
    assert beautify_string._capitalize_string("test'S") == "test'S"
    assert beautify_string._capitalize_string("Bernd's Great Song") == "Bernd's Great Song"
    assert beautify_string._capitalize_string("Bernd's Great Song") == "Bernd's Great Song"
    assert beautify_string._capitalize_string("DMX") == "DMX"
    assert beautify_string._capitalize_string("DMX is testing") == "DMX Is Testing"
    assert beautify_string._capitalize_string("bmX bike") == "bmX Bike"
    assert beautify_string._capitalize_string("data-now data-yesterday") == "Data-Now Data-Yesterday"
    assert beautify_string._capitalize_string("Data-Now") == "Data-Now" # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert beautify_string._capitalize_string("Data-now") == "Data-now" # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert beautify_string._capitalize_string("data-Now") == "data-Now" # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert beautify_string._capitalize_string("m+m") == "M+M"
    assert beautify_string._capitalize_string("M+m") == "M+m"
    assert beautify_string._capitalize_string("A-ha") == "A-ha"
    assert beautify_string._capitalize_string("A-Ha") == "A-Ha"
    assert beautify_string._capitalize_string("a-Ha") == "a-Ha"
    assert beautify_string._capitalize_string("a-ha") == "A-Ha"
    assert beautify_string._capitalize_string("self-destruct") == "Self-Destruct"
    assert beautify_string._capitalize_string("ärzte") == "Ärzte"
    assert beautify_string._capitalize_string("bÄrzte") == "bÄrzte"
    assert beautify_string._capitalize_string("Capone 'n' Noreaga") == "Capone 'n' Noreaga"
    assert beautify_string._capitalize_string("Guns 'n' Roses") == "Guns 'n' Roses"
    assert beautify_string._capitalize_string("+44") == "+44"
    assert beautify_string._capitalize_string("your's") == "Your's"
    assert beautify_string._capitalize_string("you're") == "You're"
    assert beautify_string._capitalize_string("") == ""



