# TODO Add tests for the whole beautify_tags that contain real input (a list of dicts (which contain tags)) for testing of real life scenarios like a folder without any track numbers.

# TODO Could this whole bunch of tests be made simpler by using Pytest parameters? Yes: https://docs.pytest.org/en/reorganize-docs/new-docs/user/parametrize.html

import pytest

from beautify_single_string import StringBeautifier


def test_string_beautification():
    """
    This tests the main/public method for beautifying strings. It contains all the (private) methods related to strings.
    """
    assert StringBeautifier.beautify_string("") == ""
    assert StringBeautifier.beautify_string("Test's test's test`s test´s") == "Test's Test's Test's Test's", "Test accents"
    assert StringBeautifier.beautify_string("Ac/Dc AC/DC ac/dc guns 'n' roses") == "ACDC ACDC ACDC Guns 'n' Roses", "Test edge cases"
    assert StringBeautifier.beautify_string(" lost in      space  Lost in Space ") == "Lost In Space Lost In Space", "Test spaces"
    assert StringBeautifier.beautify_string("where to? what now???") == "Where To What Now", "Question mark"
    assert StringBeautifier.beautify_string("?!?") == "!", "Question mark"
    assert StringBeautifier.beautify_string("I'am") == "I'am", "Test connected words"
    assert StringBeautifier.beautify_string("data/now data\\yesterday") == "Data-Now Data-Yesterday", "Test slash"
    assert StringBeautifier.beautify_string("A feat. B C featuring D E feat F") == "A Feat. B C Feat. D E Feat F", "Test Featuring"
    assert StringBeautifier.beautify_string("New Song Pt. 4 pt. 5 pt 6") == "New Song Part 4 Part 5 Pt 6", "Test Part"
    assert StringBeautifier.beautify_string("abC dEF ghi j5L") == "abC dEF Ghi j5L", "Test word contains capital letter - but not at beginning"
    assert StringBeautifier.beautify_string("m&m M&m") == "M&M M&m", "Test &"
    assert StringBeautifier.beautify_string("baum,stamm") == "Baum, Stamm", "Test comma and space"
    assert StringBeautifier.beautify_string("10,5") == "10,5", "Test comma and space"
    assert StringBeautifier.beautify_string("Gerd,10") == "Gerd, 10", "Test comma and space"
    assert StringBeautifier.beautify_string("10,Gerd") == "10, Gerd", "Test comma and space"
    assert StringBeautifier.beautify_string("10,gerd") == "10, Gerd", "Test comma and space"
    assert StringBeautifier.beautify_string(" ") == "", "Test empty 1"
    assert StringBeautifier.beautify_string("") == "", "Test empty 2"
    assert StringBeautifier.beautify_string("Nice Track REMIX") == "Nice Track Remix", "Test Remix suffix 1"
    assert StringBeautifier.beautify_string("Nice Track (REMIX)") == "Nice Track (Remix)", "Test Remix suffix 2"
    assert StringBeautifier.beautify_string("Nice Track LIVE") == "Nice Track Live", "Test Live suffix 1"
    assert StringBeautifier.beautify_string("Nice Track (LIVE)") == "Nice Track (Live)", "Test Live suffix 2"
    assert StringBeautifier.beautify_string(" Featuring Test") == "Feat. Test", "Test Feat. 1"
    assert StringBeautifier.beautify_string("Featuring Test") == "Feat. Test", "Test Feat. 2"
    assert StringBeautifier.beautify_string("Bomb Featuring Test") == "Bomb Feat. Test", "Test Feat. 3"
    assert StringBeautifier.beautify_string(" Pt. 2") == "Part 2", "Test Part 1"
    assert StringBeautifier.beautify_string("Pt. 2") == "Part 2", "Test Part 2"
    assert StringBeautifier.beautify_string("Bomb Pt. 2") == "Bomb Part 2", "Test Part 3"
    assert StringBeautifier.beautify_string("test III") == "Test III"
    assert StringBeautifier.beautify_string("äh") == "Äh"
    assert StringBeautifier.beautify_string("äh !") == "Äh !"
    assert StringBeautifier.beautify_string("your's") == "Your's"
    assert StringBeautifier.beautify_string('"123"') == "'123'"
    assert StringBeautifier.beautify_string('"abc"') == "'Abc'"
    assert StringBeautifier.beautify_string("'abc'") == "'Abc'"
    assert StringBeautifier.beautify_string("1st") == "1st"
    assert StringBeautifier.beautify_string("2nd") == "2nd"
    assert StringBeautifier.beautify_string("3rd") == "3rd"
    assert StringBeautifier.beautify_string("4th") == "4th"
    assert StringBeautifier.beautify_string("34th") == "34th"
    assert StringBeautifier.beautify_string("91st") == "91st"
    assert StringBeautifier.beautify_string("30th") == "30th"
    assert StringBeautifier.beautify_string("st1") == "St1"
    assert StringBeautifier.beautify_string("r2d2") == "R2D2"
    assert StringBeautifier.beautify_string("The sound of you and me") == "The Sound Of You And Me"
    assert StringBeautifier.beautify_string("we're") == "We're"
    assert StringBeautifier.beautify_string("We're") == "We're"
    assert StringBeautifier.beautify_string("we´re") == "We're"
    assert StringBeautifier.beautify_string("We´re") == "We're"
    assert StringBeautifier.beautify_string("We`re") == "We're"
    assert StringBeautifier.beautify_string("BG-EE") == "BG-EE"
    assert StringBeautifier.beautify_string(None) is None, "Test none"


def test_string_beautification_leading_the(remove_leading_the=True):  # Switch this to True to easily test it also for that case.
    assert StringBeautifier.beautify_string("", remove_leading_the=remove_leading_the) == ""
    assert StringBeautifier.beautify_string("The Beatles ", remove_leading_the=remove_leading_the) == "Beatles", "Test Leading The"
    assert StringBeautifier.beautify_string(" The Beatles ", remove_leading_the=remove_leading_the) == "Beatles", "Test Leading The"
    assert StringBeautifier.beautify_string("TheBeatles ", remove_leading_the=remove_leading_the) == "TheBeatles", "Test Leading The"
    assert StringBeautifier.beautify_string("The-Beatles ", remove_leading_the=remove_leading_the) == "The-Beatles", "Test Leading The"
    assert StringBeautifier.beautify_string(None, remove_leading_the=remove_leading_the) is None, "Test none"
    assert StringBeautifier.beautify_string("The", remove_leading_the=remove_leading_the) == "The", "Test for a band named 'The'"


def test_string_remove_whitespaces():
    assert StringBeautifier._remove_not_needed_whitespaces("") == ""
    assert StringBeautifier._remove_not_needed_whitespaces(" lost in      space  Lost In Space ") == "lost in space Lost In Space", "Test spaces"
    assert StringBeautifier._remove_not_needed_whitespaces(" Test") == "Test"
    assert StringBeautifier._remove_not_needed_whitespaces("Test ") == "Test"
    assert StringBeautifier._remove_not_needed_whitespaces(" Test ") == "Test"
    assert StringBeautifier._remove_not_needed_whitespaces(" 123 456 ") == "123 456"
    assert StringBeautifier._remove_not_needed_whitespaces(" ") == ""
    assert StringBeautifier._remove_not_needed_whitespaces("  ") == ""


def test_string_unify_quotation_marks_and_accents():
    assert StringBeautifier._unify_quotation_marks_and_accents("") == ""
    assert StringBeautifier._unify_quotation_marks_and_accents('"Great Song"') == "'Great Song'", "Quotation marks"
    assert StringBeautifier._unify_quotation_marks_and_accents("Tim´s") == "Tim's", "Accents"
    assert StringBeautifier._unify_quotation_marks_and_accents("Tim`s") == "Tim's", "Accents"


def test_string_beautify_colons():
    assert StringBeautifier._beautify_colons("") == ""
    assert StringBeautifier._beautify_colons("Deus Ex: Human Revolution") == "Deus Ex - Human Revolution", "Colon followed by whitespace"
    assert StringBeautifier._beautify_colons("He: Hello") == "He - Hello", "Colon followed by whitespace"
    assert StringBeautifier._beautify_colons("Deus : Ex") == "Deus - Ex"
    assert StringBeautifier._beautify_colons("Deus: Ex") == "Deus - Ex"
    assert StringBeautifier._beautify_colons("Über:Über") == "Über-Über"
    assert StringBeautifier._beautify_colons("Über: Über") == "Über - Über"
    assert StringBeautifier._beautify_colons("Ü: Ü") == "Ü - Ü"
    assert StringBeautifier._beautify_colons("ß: ß") == "ß - ß"
    assert StringBeautifier._beautify_colons("é: é") == "é - é"
    assert StringBeautifier._beautify_colons("Deus:Ex") == "Deus-Ex", "Colon followed by non-whitespace 1"
    assert StringBeautifier._beautify_colons("12:34") == "12-34", "Colon followed by non-whitespace 2"
    assert StringBeautifier._beautify_colons("Folge 34: Test") == "Folge 34 - Test"
    assert StringBeautifier._beautify_colons(" : ") == " - ", "Colon surrounded by whitespace"
    assert StringBeautifier._beautify_colons(":Ex") == "-Ex", "Colon surrounded by whitespace"
    assert StringBeautifier._beautify_colons("Ex:") == "Ex-", "Colon surrounded by whitespace"
    assert StringBeautifier._beautify_colons("Ex:") == "Ex-", "Colon surrounded by whitespace"


def test_enforce_round_brackets():
    assert StringBeautifier._enforce_round_brackets("(Test)") == "(Test)"
    assert StringBeautifier._enforce_round_brackets("(Test]") == "(Test)"
    assert StringBeautifier._enforce_round_brackets("[Test]") == "(Test)"
    assert StringBeautifier._enforce_round_brackets("[[Test]]") == "(Test)"
    assert StringBeautifier._enforce_round_brackets("{Test}") == "(Test)"
    assert StringBeautifier._enforce_round_brackets("⟨Test⟩") == "(Test)"


def test_unify_hyphens():
    assert StringBeautifier._unify_hyphens("Test-Case") == "Test-Case"
    assert StringBeautifier._unify_hyphens("Test―Case") == "Test-Case"
    assert StringBeautifier._unify_hyphens("Test‒Case") == "Test-Case"


def test_string_replace_special_characters():
    assert StringBeautifier._replace_special_characters("") == ""
    assert StringBeautifier._replace_special_characters(";") == ","
    assert StringBeautifier._replace_special_characters("tl;dr") == "tl,dr"
    assert StringBeautifier._replace_special_characters("\\") == "-"
    assert StringBeautifier._replace_special_characters("abc\\def") == "abc-def"
    assert StringBeautifier._replace_special_characters("/") == "-"
    assert StringBeautifier._replace_special_characters("abc/def") == "abc-def"
    assert StringBeautifier._replace_special_characters("?") == ""
    assert StringBeautifier._replace_special_characters("WTF?") == "WTF"
    assert StringBeautifier._replace_special_characters("&") == "&"  # Nothing changed here.
    assert StringBeautifier._replace_special_characters("C&A") == "C&A"  # Nothing changed here.


def test_string_fill_missing_space_after_comma():
    assert StringBeautifier._fill_missing_space_after_comma("") == ""
    assert StringBeautifier._fill_missing_space_after_comma("baum,stamm") == "baum, stamm"
    assert StringBeautifier._fill_missing_space_after_comma("10,5") == "10,5"
    assert StringBeautifier._fill_missing_space_after_comma("5,neu") == "5, neu"
    assert StringBeautifier._fill_missing_space_after_comma("neu,5") == "neu, 5"


def test_string_remove_leading_the():
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="") == ""
    assert StringBeautifier._remove_leading_the(remove_leading_the=False, text="") == ""
    assert StringBeautifier._remove_leading_the(remove_leading_the=False, text="The Beatles") == "The Beatles"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="The Beatles") == "Beatles"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="The-Beatles") == "The-Beatles"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="Therapy") == "Therapy"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="The 182") == "182"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="T H E") == "T H E"
    assert StringBeautifier._remove_leading_the(remove_leading_the=True, text="The") == "The"


def test_string_deal_with_special_words():
    assert StringBeautifier._deal_with_special_words_and_bands("") == ""
    assert StringBeautifier._deal_with_special_words_and_bands(" Featuring ") == " Feat. "
    assert StringBeautifier._deal_with_special_words_and_bands("Featuring ") == "Feat. "
    assert StringBeautifier._deal_with_special_words_and_bands("Featuring") == "Featuring"
    assert StringBeautifier._deal_with_special_words_and_bands("(Featuring)") == "(Featuring)"
    assert StringBeautifier._deal_with_special_words_and_bands("(Featuring abc)") == "(Feat. abc)"
    assert StringBeautifier._deal_with_special_words_and_bands(" FEATURING ") == " Feat. "
    assert StringBeautifier._deal_with_special_words_and_bands("Test Featuring") == "Test Featuring"
    assert StringBeautifier._deal_with_special_words_and_bands(" Pt. 1 ") == " Part 1 "
    assert StringBeautifier._deal_with_special_words_and_bands(" Pt. 1") == " Part 1"
    assert StringBeautifier._deal_with_special_words_and_bands("Pt. 1 ") == "Part 1 "
    assert StringBeautifier._deal_with_special_words_and_bands("Pt. 1") == "Part 1"
    assert StringBeautifier._deal_with_special_words_and_bands("pt. 1") == "Part 1"
    assert StringBeautifier._deal_with_special_words_and_bands("copt. 1") == "copt. 1"
    assert StringBeautifier._deal_with_special_words_and_bands("remix") == "Remix"
    assert StringBeautifier._deal_with_special_words_and_bands("REMIX") == "Remix"
    assert StringBeautifier._deal_with_special_words_and_bands("cremeremix") == "cremeremix"
    assert StringBeautifier._deal_with_special_words_and_bands("best remix") == "best Remix"
    assert StringBeautifier._deal_with_special_words_and_bands("(remix)") == "(Remix)"
    assert StringBeautifier._deal_with_special_words_and_bands(" (remix)") == " (Remix)"
    assert StringBeautifier._deal_with_special_words_and_bands("(best remix)") == "(best Remix)"
    assert StringBeautifier._deal_with_special_words_and_bands("live") == "Live"
    assert StringBeautifier._deal_with_special_words_and_bands("(live)") == "(Live)"
    assert StringBeautifier._deal_with_special_words_and_bands("LIVE") == "Live"
    assert StringBeautifier._deal_with_special_words_and_bands("sunlive") == "sunlive"


def test_string_capitalize_string():
    """
    Remember that this shall not touch a string (part (surrounded by spaces)), if that has already any capital letter in it.
    """
    assert StringBeautifier._capitalize_string("test's") == "Test's"
    assert StringBeautifier._capitalize_string("Bernd's") == "Bernd's"
    assert StringBeautifier._capitalize_string("test'N") == "test'N"
    assert StringBeautifier._capitalize_string("test'S") == "test'S"
    assert StringBeautifier._capitalize_string("Bernd's Great Song") == "Bernd's Great Song"
    assert StringBeautifier._capitalize_string("Bernd's Great Song") == "Bernd's Great Song"
    assert StringBeautifier._capitalize_string("DMX") == "DMX"
    assert StringBeautifier._capitalize_string("DMX is testing") == "DMX Is Testing"
    assert StringBeautifier._capitalize_string("bmX bike") == "bmX Bike"
    assert StringBeautifier._capitalize_string("data-now data-yesterday") == "Data-Now Data-Yesterday"
    assert StringBeautifier._capitalize_string("Data-Now") == "Data-Now"  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert StringBeautifier._capitalize_string("Data-now") == "Data-now"  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert StringBeautifier._capitalize_string("data-Now") == "data-Now"  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
    assert StringBeautifier._capitalize_string("m+m") == "M+M"
    assert StringBeautifier._capitalize_string("M+m") == "M+m"
    assert StringBeautifier._capitalize_string("A-ha") == "A-ha"
    assert StringBeautifier._capitalize_string("A-Ha") == "A-Ha"
    assert StringBeautifier._capitalize_string("a-Ha") == "a-Ha"
    assert StringBeautifier._capitalize_string("a-ha") == "A-Ha"
    assert StringBeautifier._capitalize_string("self-destruct") == "Self-Destruct"
    assert StringBeautifier._capitalize_string("ärzte") == "Ärzte"
    assert StringBeautifier._capitalize_string("bÄrzte") == "bÄrzte"
    assert StringBeautifier._capitalize_string("Capone 'n' Noreaga") == "Capone 'n' Noreaga"
    assert StringBeautifier._capitalize_string("Guns 'n' Roses") == "Guns 'n' Roses"
    assert StringBeautifier._capitalize_string("+44") == "+44"
    assert StringBeautifier._capitalize_string("your's") == "Your's"
    assert StringBeautifier._capitalize_string("you're") == "You're"
    assert StringBeautifier._capitalize_string("we're") == "We're"
    assert StringBeautifier._capitalize_string("We're") == "We're"
    assert StringBeautifier._capitalize_string("The sound of you and me") == "The Sound Of You And Me"
    assert StringBeautifier._capitalize_string("1st") == "1st"
    assert StringBeautifier._capitalize_string("2nd") == "2nd"
    assert StringBeautifier._capitalize_string("3rd") == "3rd"
    assert StringBeautifier._capitalize_string("4th") == "4th"
    assert StringBeautifier._capitalize_string("34th") == "34th"
    assert StringBeautifier._capitalize_string("91st") == "91st"
    assert StringBeautifier._capitalize_string("30th") == "30th"
    assert StringBeautifier._capitalize_string("") == ""


@pytest.fixture
def suffix_keywords():
    return ["remix", "feat", "skit", "produced", "cut", "cutted", "bonus", "part", "pt", "live"]
