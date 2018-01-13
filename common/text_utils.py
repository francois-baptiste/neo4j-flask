import re
import string
import unicodedata


class TextCleanUp:

    @staticmethod
    def is_empty_string(value: str):
        if value is None:
            return True
        if value.strip() == "":
            return True
        return False

    @staticmethod
    def remove_double_whitespace(value: str):
        whitespace_regex = re.compile('\s{2,}')
        return whitespace_regex.sub(' ', value).strip()

    @staticmethod
    def remove_punctuation(value: str, replace_with: str = ' ', exclusions: dict = None):
        table = str.maketrans({key: replace_with for key in string.punctuation})
        # some exclusions
        if exclusions is not None:
            for item in exclusions:
                table[ord(item)] = exclusions[item]

        return value.translate(table)

    @staticmethod
    def normalise_unicode(text: str):
        result = text.encode('latin1', 'ignore').decode('latin1')
        return unicodedata.normalize('NFKD', result).encode('ascii', 'ignore').decode('utf-8')


    @staticmethod
    def delim_frequency(text: str, delimeters = string.punctuation):
        frequencies = [(c, text.count(c)) for c in set(text)]
        result = {}

        for i, item in enumerate(frequencies):
            if item[0] in delimeters:
                result[item[0]] = item[1]

        return result
