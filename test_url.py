import unittest
import unittest.mock
import url as urlm
import itertools
import random
import string
import itertools
import logging


RANDOM_STRING_LEN=64


def setUpModule():
    """Disable logging while doing these tests."""
    logging.disable()


def tearDownModule():
    """Re-enable logging after doing these tests."""
    logging.disable(logging.NOTSET)


def random_string(size=RANDOM_STRING_LEN, chars=string.ascii_letters):
    """Generate a random string of SIZE using CHARS."""

    return ''.join(random.choices(chars, k=size))


def urls_for_test():
    """URL generator."""

    protocols = ['', 'file:///', 'ftp://', 'http://', 'https://']
    paths = ['', 'home', 'home/foo', 'home/foo/bar.txt']
    params = ['', '?abc=cde', '?abc=cde&FgH=iJk!@#$%']
    randoms = ['', random_string()]

    for comb in itertools.product(protocols, paths, params, randoms):
        yield ''.join(comb)


class TestUrlInit(unittest.TestCase):
    """Url instantiation."""

    def test_attr_url(self):
        """Instantiation with URL preserves received value."""

        for url in urls_for_test():
            with self.subTest(url=url):
                self.assertEqual(url, urlm.Url(url).url)


class TestAttr_ResponseUrl(unittest.TestCase):
    """‘_responseurl’ attribute works properly."""

    def test__responseurl_must_be_set_first(self):
        """Raises error if trying to get _responseurl before setting it."""

        with self.assertRaises(RuntimeError):
            urlm.Url('')._responseurl


    def test__responseurl_get(self):
        """‘get’ works properly for ‘_responseurl’."""

        url_obj = urlm.Url('')
        for url in urls_for_test():
            with self.subTest(url=url):
                url_obj._responseurl = url
                self.assertEqual(url_obj._responseurl, url)


class Test_UrlPath(unittest.TestCase):
    """‘_urlpath’ attribute works properly."""

    def test_uses_expected_method(self):
        """Uses ‘urllib.parse.urlparse’, with the correct URL.

        It’s assumed that ‘urllib.parse.urlparse’ will be used."""

        with unittest.mock.patch('urllib.parse.urlparse') as urlparse_mock:
            # Get a test Url instance ready.
            url_obj = urlm.Url(random_string())

            # Using another random string for the attribute ‘_responseurl’ to
            # have an independent test that the program sets and gets it
            # properly, and that it does not change it before using it to
            # obtain ‘_urlpath’.
            responseurl = random_string()
            url_obj._responseurl = responseurl

            # Get the mocked method ready to be called.
            # Assigns the property ‘path’ to whatever is returned after calling
            # ‘urlparse_mock()’.
            # This is necessary because the parsed URL itself corresponds to the
            # property ‘path’ from the object that is returned from the parsing
            # method.
            urlparse_mock().path = random_string()

            # Force test object to parse its URL, giving it a reason to call
            # ‘urllib.parse.urlparse’.
            urlpath = url_obj._urlpath

            # Check if ‘urllib.parse.urlparse’ was called, and with the correct
            # URL.
            urlparse_mock.assert_called_with(responseurl)

            # Check if it assigned its attribute to the correct property from
            # the return value of ‘urllib.parse.urlparse’.
            self.assertEqual(url_obj._urlpath, urlparse_mock().path)


    def test_raises_errors(self):
        """Raises errors as promised in the docstring."""

        # Check if a RuntimeError is raised as a result of a ValueError
        # triggered by a malformed URL.
        with unittest.mock.patch('urllib.parse.urlparse') as urlparse_mock:
            # Create a test object.
            url_obj = urlm.Url(random_string())

            # Make the mocked method raise the proper error when called.
            urlparse_mock.side_effect = ValueError

            # Check if the expected error was raised as a result.
            # For this it suffices to get the attribute, which will then call
            # ‘urllib.parse.urlparse’.
            with self.assertRaises(RuntimeError):
                url_obj._urlpath


if __name__ == '__main__':
    unittest.main()
