import re


class DateBeautifier:
    """
    This utility class bundles id3 tag beautification methods for dates. This class beautifies a single string at a time.
    """

    @staticmethod
    def extract_year(string: str) -> str:
        """
        Shorten any YYYY-MM-DD values into YYYY.
        """

        output = string

        if output is None:
            return output

        elif output is not None:  # Dealing with the special of None - which is not converted into a string.
            output = str(output)

        try:
            output = re.search(r"(19|20|21)\d{2}", output).group(0)  # Look for 19xx, 20xx or 21xx (where xx are two digits). First found entry will be taken.
        except:
            pass  # If no YYYY string can be extracted, e.g. data provided is "01-01-20", then return untouched string.

        return output
