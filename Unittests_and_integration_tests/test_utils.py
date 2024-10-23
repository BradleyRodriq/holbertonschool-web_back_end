#!/usr/bin/env python3
"""
Uses the 'unittest' and 'parameterized' modules
to test 'utils.py'.
"""
import unittest
from parameterized import parameterized
import unittest.mock
from fixtures import TEST_PAYLOAD
import utils
from utils import memoize
from typing import (
    Mapping,
    Sequence,
    Any,
)


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests 'utils.access_nested_map'
    """
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Tests utils.access_nested_map

        >>> utils.access_nested_map({"a": 1}, ("a",))
        1
        >>> utils.access_nested_map({"a": {"b": 2}}, ("a",))
        {"b": 2}
        >>> utils.access_nested_map({"a": {"b": 2}}, ("a", "b"))
        2
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b"))
        ]
    )
    def test_access_nested_map_exception(
        self,
        nested_map:
        Mapping,
        path: Sequence
    ) -> None:
        """
        test access nested map exception

        >>> utils.access_nested_map({}, ("a",))
        KeyError
        >>> utils.access_nested_map({"a": 1}, ("a", "b"))
        KeyError
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Tests 'utils.get_json'.
    """
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False})
        ]
    )
    def test_get_json(self, test_url: str, test_payload) -> None:
        """
        tests get json
        """
        with unittest.mock.patch(
            'utils.requests.get',
            new=unittest.mock.Mock(
                return_value=unittest.mock.Mock(
                    json=unittest.mock.Mock(
                        return_value=test_payload
                    )
                )
            )
        ):
            self.assertEqual(utils.get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests 'utils.memoize'
    """
    def test_memoize(self):
        """
        Tests utils.memoize

        >>> class TestClass:
            def a_method(self):
                return 42
            @memoize
            def a_property(self):
                return self.a_method()

        >>> t = TestClass()
        >>> t.a_property
        42
        >>> t.a_property
        42
        >>> t.a_property
        42
        """
        EXPECTED_OUTPUT = 42

        class TestClass:
            def a_method(self):
                return EXPECTED_OUTPUT

            @memoize
            def a_property(self):
                return self.a_method()

        TestClass.a_method = unittest.mock.Mock(return_value=EXPECTED_OUTPUT)

        t = TestClass()

        self.assertEqual(t.a_property, EXPECTED_OUTPUT)
        t.a_method.assert_called_once()
        self.assertEqual(t.a_property, EXPECTED_OUTPUT)
        t.a_method.assert_called_once()
