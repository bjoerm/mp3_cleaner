# TODO Add tests for the whole beautify_tags that contain real input (a list of dicts (which contain tags)) for testing of real life scenarios like a folder without any track numbers.

# TODO Could this whole bunch of tests be made simpler by using Pytest parameters? Yes: https://docs.pytest.org/en/reorganize-docs/new-docs/user/parametrize.html

import pytest

from strings.beautify_single_string import StringBeautifier


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["Empty String", "", ""],
        ["Empty String", " ", ""],
        ["Accents", "Test's test's test`s test´s", "Test's Test's Test's Test's"],
        ["Edge Cases", "Ac/Dc AC/DC ac/dc guns 'n' roses", "ACDC ACDC ACDC Guns 'n' Roses"],
        ["Spaces", " lost in      space  Lost in Space ", "Lost In Space Lost In Space"],
        ["Question mark", "where to? what now???", "Where To What Now"],
        ["Question mark", "?!?", "!"],
        ["Connected words", "I'am", "I'am"],
        ["Slash", "data/now data\\yesterday", "Data-Now Data-Yesterday"],
        ["Featuring", "A feat. B C featuring D E feat F", "A Feat. B C Feat. D E Feat F"],
        ["Part", "New Song Pt. 4 pt. 5 pt 6", "New Song Part 4 Part 5 Pt 6"],
        ["Word contains capital letter - but not at beginning", "abC dEF ghi j5L", "abC dEF Ghi j5L"],
        ["&", "m&m M&m", "M&M M&m"],
        ["Stars", "a*a", "A-A"],
        ["Stars", "a*", "A-"],
        ["Stars", "***", "---"],
        ["Comma and space", "abc,def", "Abc, Def"],
        ["Comma and space", "10,5", "10,5"],
        ["Comma and space", "Abc,10", "Abc, 10"],
        ["Comma and space", "10,Abc", "10, Abc"],
        ["Comma and space", "10,abc", "10, Abc"],
        ["Remix suffix", "Nice Track REMIX", "Nice Track Remix"],
        ["Remix suffix", "Nice Track (REMIX)", "Nice Track (Remix)"],
        ["Remix suffix", "Nice Track LIVE", "Nice Track Live"],
        ["Remix suffix", "Nice Track (LIVE)", "Nice Track (Live)"],
        ["Feat.", " Featuring Test", "Feat. Test"],
        ["Feat.", "Featuring Test", "Feat. Test"],
        ["Feat.", "Bomb Featuring Test", "Bomb Feat. Test"],
        ["Part", " Pt. 2", "Part 2"],
        ["Part", "Pt. 2", "Part 2"],
        ["Part", "Bomb Pt. 2", "Bomb Part 2"],
        ["Roman letters", "test III", "Test III"],
        ["Umlaut", "äh", "Äh"],
        ["Umlaut", "äh !", "Äh !"],
        ["Accents", "your's", "Your's"],
        ["Quotations", '"123"', "'123'"],
        ["Quotations", '"abc"', "'Abc'"],
        ["Quotations", "'abc'", "'Abc'"],
        ["Numbers", "1st", "1st"],
        ["Numbers", "2nd", "2nd"],
        ["Numbers", "3rd", "3rd"],
        ["Numbers", "4th", "4th"],
        ["Numbers", "34th", "34th"],
        ["Numbers", "91st", "91st"],
        ["Numbers", "30th", "30th"],
        ["Alphanumeric", "st1", "St1"],
        ["Alphanumeric", "r2d2", "R2D2"],
        ["Some title", "The sound of you and me", "The Sound Of You And Me"],
        ["Accents", "we're", "We're"],
        ["Accents", "We're", "We're"],
        ["Accents", "we´re", "We're"],
        ["Accents", "We´re", "We're"],
        ["Accents", "We`re", "We're"],
        ["Hyphen", "BG-EE", "BG-EE"],
        ["None", None, None],
        ["Special words", "gmbh", "GmbH"],
        ["Special words", "Gmbh", "GmbH"],
        ["Special words", "GMBH", "GmbH"],
        ["Normal", "What's your name?", "What's Your Name"],
        ["Normal", "What's your name", "What's Your Name"],
        ["Normal", "What your name", "What Your Name"],
    ],
)
def test_string_beautification(name, input, expected_output):
    """
    This tests the main/public method for beautifying strings. It contains all the (private) methods related to strings.
    """
    assert StringBeautifier.beautify_string(input) == expected_output, name


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["Empty String", "", ""],
        ["Empty String", " ", ""],
        ["The", "The Beatles ", "Beatles"],
        ["The", " The Beatles ", "Beatles"],
        ["Concat", "TheBeatles ", "TheBeatles"],
        ["Hyphen", "The-Beatles ", "The-Beatles"],
        ["None", None, None],
        ["A band named 'The'", "The", "The"],
    ],
)
def test_string_beautification_leading_the(name, input, expected_output, remove_leading_the=True):
    assert StringBeautifier.beautify_string(input, remove_leading_the=remove_leading_the) == expected_output, name


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["", ""],
        [" lost in      space  Lost In Space ", "lost in space Lost In Space"],
        [" Test", "Test"],
        ["Test ", "Test"],
        [" Test ", "Test"],
        [" 123 456 ", "123 456"],
        [" ", ""],
        ["  ", ""],
    ],
)
def test_string_remove_whitespaces(input, expected_output):
    assert StringBeautifier._remove_not_needed_whitespaces(input) == expected_output


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["Empty string", "", ""],
        ["Quotation marks", '"Great Song"', "'Great Song'"],
        ["Double single quotation marks", "''Great Song''", "'Great Song'"],
        ["Accents", "Tim´s", "Tim's"],
        ["Accents", "Tim`s", "Tim's"],
    ],
)
def test_string_unify_quotation_marks_and_accents(name, input, expected_output):
    assert StringBeautifier._unify_quotation_marks_and_accents(input) == expected_output, name


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["", ""],
        ["Deus Ex: Human Revolution", "Deus Ex - Human Revolution"],
        ["He: Hello", "He - Hello"],
        ["Deus : Ex", "Deus - Ex"],
        ["Deus: Ex", "Deus - Ex"],
        ["Über:Über", "Über-Über"],
        ["Über: Über", "Über - Über"],
        ["Ü: Ü", "Ü - Ü"],
        ["ß: ß", "ß - ß"],
        ["é: é", "é - é"],
        ["Deus:Ex", "Deus-Ex"],
        ["12:34", "12-34"],
        ["Folge 34: Test", "Folge 34 - Test"],
        [" : ", " - "],
        [":Ex", "-Ex"],
        ["Ex:", "Ex-"],
        ["Ex:", "Ex-"],
    ],
)
def test_string_beautify_colons(input, expected_output):
    assert StringBeautifier._beautify_colons(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["(Test)", "(Test)"],
        ["(Test]", "(Test)"],
        ["[Test]", "(Test)"],
        ["[[Test]]", "(Test)"],
        ["{Test}", "(Test)"],
        ["⟨Test⟩", "(Test)"],
    ],
)
def test_enforce_round_brackets(input, expected_output):
    assert StringBeautifier._enforce_round_brackets(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["Test-Case", "Test-Case"],
        ["Test―Case", "Test-Case"],
        ["Test‒Case", "Test-Case"],
    ],
)
def test_unify_hyphens(input, expected_output):
    assert StringBeautifier._unify_hyphens(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["", ""],
        [";", ","],
        ["tl;dr", "tl,dr"],
        ["\\", "-"],
        ["abc\\def", "abc-def"],
        ["/", "-"],
        ["abc/def", "abc-def"],
        ["?", ""],
        ["WTF?", "WTF"],
        ["&", "&"],
        ["C&A", "C&A"],
    ],
)
def test_string_replace_special_characters(input, expected_output):
    assert StringBeautifier._replace_special_characters(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["", ""],
        ["baum,stamm", "baum, stamm"],
        ["10,5", "10,5"],
        ["5,neu", "5, neu"],
        ["neu,5", "neu, 5"],
    ],
)
def test_string_fill_missing_space_after_comma(input, expected_output):
    assert StringBeautifier._fill_missing_space_after_comma(input) == expected_output


@pytest.mark.parametrize(
    "remove_leading_the, input, expected_output",
    [
        [True, "", ""],
        [False, "", ""],
        [False, "The Beatles", "The Beatles"],
        [True, "The Beatles", "Beatles"],
        [True, "TheBeatles", "TheBeatles"],
        [True, "The-Beatles", "The-Beatles"],
        [True, "Therapy", "Therapy"],
        [True, "The 182", "182"],
        [True, "T H E", "T H E"],
        [True, "The", "The"],
    ],
)
def test_string_remove_leading_the(remove_leading_the, input, expected_output):
    assert StringBeautifier._remove_leading_the(remove_leading_the=remove_leading_the, text=input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["", ""],
        [" Featuring ", " Feat. "],
        ["Featuring ", "Feat. "],
        ["Featuring", "Featuring"],  # Is this desired?
        ["(Featuring)", "(Featuring)"],  # Is this desired?
        ["(Featuring abc)", "(Feat. abc)"],
        [" FEATURING ", " Feat. "],
        ["Test Featuring", "Test Featuring"],
        [" Pt. 1 ", " Part 1 "],
        [" Pt. 1", " Part 1"],
        ["Pt. 1 ", "Part 1 "],
        ["Pt. 1", "Part 1"],
        ["pt. 1", "Part 1"],
        ["copt. 1", "copt. 1"],
        ["remix", "Remix"],
        ["REMIX", "Remix"],
        ["cremeremix", "cremeremix"],
        ["best remix", "best Remix"],
        ["(remix)", "(Remix)"],
        [" (remix)", " (Remix)"],
        ["(best remix)", "(best Remix)"],
        ["live", "Live"],
        ["(live)", "(Live)"],
        ["LIVE", "Live"],
        ["sunlive", "sunlive"],
        ["gmbh", "GmbH"],
        ["Gmbh", "GmbH"],
        ["GMBH", "GmbH"],
        ["AC-DC", "ACDC"],
        ["AC-DC test", "ACDC test"],
    ],
)
def test_string_deal_with_special_words(input, expected_output):
    assert StringBeautifier._deal_with_special_words_and_bands(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ["test's", "Test's"],
        ["Bernd's", "Bernd's"],
        ["test'N", "test'N"],
        ["test'S", "test'S"],
        ["Bernd's Great Song", "Bernd's Great Song"],
        ["Bernd's Great Song", "Bernd's Great Song"],
        ["DMX", "DMX"],
        ["DMX is testing", "DMX Is Testing"],
        ["bmX bike", "bmX Bike"],
        ["data-now data-yesterday", "Data-Now Data-Yesterday"],
        ["Data-Now", "Data-Now"],  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
        ["Data-now", "Data-now"],  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
        ["data-Now", "data-Now"],  # Shall return this as it follows the rule to not touch the string, if there is a capital letter somehwere.
        ["m+m", "M+M"],
        ["M+m", "M+m"],
        ["A-ha", "A-ha"],
        ["A-Ha", "A-Ha"],
        ["a-Ha", "a-Ha"],
        ["a-ha", "A-Ha"],
        ["self-destruct", "Self-Destruct"],
        ["ärzte", "Ärzte"],
        ["bÄrzte", "bÄrzte"],
        ["Capone 'n' Noreaga", "Capone 'n' Noreaga"],
        ["Guns 'n' Roses", "Guns 'n' Roses"],
        ["+44", "+44"],
        ["your's", "Your's"],
        ["you're", "You're"],
        ["we're", "We're"],
        ["We're", "We're"],
        ["The sound of you and me", "The Sound Of You And Me"],
        ["1st", "1st"],
        ["2nd", "2nd"],
        ["3rd", "3rd"],
        ["4th", "4th"],
        ["34th", "34th"],
        ["91st", "91st"],
        ["30th", "30th"],
        ["", ""],
    ],
)
def test_string_capitalize_string(input, expected_output):
    """
    Remember that this shall not touch a string (part (surrounded by spaces)), if that has already any capital letter in it.
    """
    assert StringBeautifier._capitalize_string(input) == expected_output
