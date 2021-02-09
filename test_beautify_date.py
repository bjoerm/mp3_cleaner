# TODO Could this whole bunch of tests be made simpler by using Pytest parameters?


from beautify_single_date import DateBeautifier

def test_mp3_tags_extract_year():
    """
    Testing the regex that extracts the year (YYYY).
    """
    assert DateBeautifier.extract_year("") == ""
    assert DateBeautifier.extract_year("1999-12-12") == "1999"
    assert DateBeautifier.extract_year("1999") == "1999"
    assert DateBeautifier.extract_year("20-12-1999") == "1999"
    assert DateBeautifier.extract_year("1999-10") == "1999"
    assert DateBeautifier.extract_year("1999-October") == "1999"
    assert DateBeautifier.extract_year("1999-H1") == "1999"
    assert DateBeautifier.extract_year("11.11.1999") == "1999"
    assert DateBeautifier.extract_year("2020-12-12") == "2020"
    assert DateBeautifier.extract_year("2020") == "2020"
    assert DateBeautifier.extract_year("20-12-2020") == "2020"
    assert DateBeautifier.extract_year("2020-10") == "2020"
    assert DateBeautifier.extract_year("2020-October") == "2020"
    assert DateBeautifier.extract_year("2020-H1") == "2020"
    assert DateBeautifier.extract_year("11.11.2020") == "2020"
    assert DateBeautifier.extract_year("11.11.11") == "11.11.11"
    assert DateBeautifier.extract_year("11-11-11") == "11-11-11"
    assert DateBeautifier.extract_year(" 1999") == "1999"
    assert DateBeautifier.extract_year(" 1999 ") == "1999"
    assert DateBeautifier.extract_year("1999 ") == "1999"
    assert DateBeautifier.extract_year("20/12/2020") == "2020"
    assert DateBeautifier.extract_year("99") == "99"
    assert DateBeautifier.extract_year("October '99") == "October '99" # TODO Adjust this case? But should be a total edge case possibly not worth the effort.
    assert DateBeautifier.extract_year(2020) == "2020"
    assert DateBeautifier.extract_year(1980) == "1980"
    assert DateBeautifier.extract_year(None) == None


