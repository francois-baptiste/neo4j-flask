from unittest import TestCase
from common.text_utils import TextCleanUp


class TestTextCleanUp(TestCase):
    tc = TextCleanUp()
    target = "hello world"

    def test_is_empty_string(self):
        self.assertEqual(self.tc.is_empty_string("     "), True)
        self.assertEqual(self.tc.is_empty_string(None), True)
        self.assertEqual(self.tc.is_empty_string(''), True)
        self.assertEqual(self.tc.is_empty_string('foo'), False)

    def test_remove_double_whitespace(self):
        self.assertEqual(self.tc.remove_double_whitespace(self.target), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello  world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello   world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello    world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello    world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace(" hello world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("  hello  world"), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello   world "), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("hello    world  "), self.target)
        self.assertEqual(self.tc.remove_double_whitespace("  hello    world   "), self.target)


    def test_remove_punctuation(self):
        self.assertEqual(self.tc.remove_punctuation(self.target), self.target)
        self.assertEqual(self.tc.remove_punctuation("hello.world"), self.target)
        self.assertEqual(self.tc.remove_punctuation("hello.world "), "hello world ")
        self.assertEqual(self.tc.remove_punctuation("hello.world!"), "hello world ")
        self.assertEqual(self.tc.remove_punctuation("hello.world!", replace_with = ''), "helloworld")
        self.assertEqual(self.tc.remove_punctuation("hello.world!", replace_with=''), "helloworld")
        self.assertEqual(self.tc.remove_punctuation("hello.world!", replace_with='',
                                                    exclusions={'!': '.'}), "helloworld.")
        self.assertEqual(self.tc.remove_punctuation("hello.world!", replace_with='',
                                                    exclusions={'!': '.', '.': '_'}), "hello_world.")


    def test_normalise_unicode(self):
        self.assertEqual(self.tc.normalise_unicode(self.target), self.target)
        self.assertEqual(self.tc.normalise_unicode('hêllö world'), self.target)
        self.assertEqual(self.tc.normalise_unicode('hêllö world  '), "hello world  ")


    def test_delim_frequency(self):
        self.assertEqual(self.tc.delim_frequency(self.target), {})
        self.assertEqual(self.tc.delim_frequency("hello world!"), {'!': 1})
        self.assertEqual(self.tc.delim_frequency("!hello.world!"), {'!': 2, '.': 1})

