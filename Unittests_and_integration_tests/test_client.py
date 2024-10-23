#!/usr/bin/env python3
"""
Tests the 'client.py' module, found in this file.
"""
import unittest
from fixtures import TEST_PAYLOAD
import client
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from typing import Dict

TEST_ORG_NAME = "google"
ORG_GET_JSON_OUTPUT = TEST_PAYLOAD[0][0]
ORG_OUTPUT = ORG_GET_JSON_OUTPUT
PUBLIC_REPOS_URL_OUTPUT = ORG_OUTPUT["repos_url"]
REPOS_PAYLOAD_GET_JSON_OUTPUT = TEST_PAYLOAD[0][1]
PUBLIC_REPOS_OUTPUT = TEST_PAYLOAD[0][-2]
APACHE2_LICENSE = "apache-2.0"
PUBLIC_REPOS_APACHE2_OUTPUT = TEST_PAYLOAD[0][-1]


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the <client.GithubOrgClient> class.
    """
    ORG_GET_JSON_OUTPUT = TEST_PAYLOAD[0][1][0]["owner"]
    ORG_OUTPUT = ORG_GET_JSON_OUTPUT
    PUBLIC_REPOS_URL_OUTPUT = ORG_OUTPUT["repos_url"]
    REPOS_PAYLOAD_GET_JSON_OUTPUT = TEST_PAYLOAD[0][1]

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json", new=Mock(return_value=ORG_GET_JSON_OUTPUT))
    def test_org(self, org: str) -> None:
        """
        Tests the 'org' method
        """
        gh_client = client.GithubOrgClient(org)

        self.assertEqual(gh_client.org, self.ORG_GET_JSON_OUTPUT)

        client.get_json.assert_called_once_with(
            client.GithubOrgClient.ORG_URL.format(org=org)
        )

        self.assertEqual(gh_client.org, self.ORG_GET_JSON_OUTPUT)

        client.get_json.assert_called_once_with(
            client.GithubOrgClient.ORG_URL.format(org=org)
        )

    def test_public_repos_url(self) -> None:
        """
        Tests the '_public_repos_url' method
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock(
                return_value=self.ORG_OUTPUT
            )
        ):
            GH_CLIENT = client.GithubOrgClient(TEST_ORG_NAME)

            self.assertEqual(
                GH_CLIENT._public_repos_url,
                self.PUBLIC_REPOS_URL_OUTPUT
            )

    @patch(
        "client.get_json",
        new=Mock(
            return_value=REPOS_PAYLOAD_GET_JSON_OUTPUT
        )
    )
    def test_public_repos(self) -> None:
        """
        Tests the 'public_repos' method
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock(
                return_value=self.PUBLIC_REPOS_URL_OUTPUT
            )
        ):
            GH_CLIENT = client.GithubOrgClient(TEST_ORG_NAME)

            self.assertEqual(
                GH_CLIENT.public_repos(APACHE2_LICENSE),
                PUBLIC_REPOS_APACHE2_OUTPUT
            )

            client.get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ]
    )
    def test_has_license(self,
                         repo: Dict[str, Dict],
                         license_key: str,
                         expected: bool) -> None:
        """
        Tests the 'has_license' method
        """
        self.assertEqual(
            client.GithubOrgClient.has_license(repo, license_key),
            expected
        )

    def test_public_repos(self):
        """
        tests the 'public_repos' method
        """
        GH_CLIENT = client.GithubOrgClient("google")

        self.assertTrue(
            set(GH_CLIENT.public_repos()).issuperset(
                PUBLIC_REPOS_OUTPUT
            )
        )

    def test_public_repos_with_license(self):
        """
        tests the 'public_repos' method
        """
        GH_CLIENT = client.GithubOrgClient("google")

        self.assertTrue(
            set(GH_CLIENT.public_repos(APACHE2_LICENSE)).issuperset(
                PUBLIC_REPOS_APACHE2_OUTPUT
            )
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(
        ORG_GET_JSON_OUTPUT,
        PUBLIC_REPOS_URL_OUTPUT,
        REPOS_PAYLOAD_GET_JSON_OUTPUT,
        PUBLIC_REPOS_APACHE2_OUTPUT
    )]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    tests the 'client.GithubOrgClient' class
    """
    @classmethod
    def setUpClass(cls) -> None:
        ORG_REQUEST_URL = client.GithubOrgClient.ORG_URL.format(
            org=TEST_ORG_NAME
        )
        """
        sets up the class
        """
        REPOS_PAYLOAD_REQUEST_URL = PUBLIC_REPOS_URL_OUTPUT

        def mocked_requests_get(url: str):
            json_output = None

            if url == ORG_REQUEST_URL:
                json_output = ORG_GET_JSON_OUTPUT
            elif url == REPOS_PAYLOAD_REQUEST_URL:
                json_output = REPOS_PAYLOAD_GET_JSON_OUTPUT
            else:
                raise ValueError(f"Unexpected url: {url}")

            return Mock(json=Mock(return_value=json_output))

        cls.get_patcher = patch(
            "requests.get",
            new=Mock(side_effect=mocked_requests_get)
        )
        cls.get_patcher.start()

    def test_public_repos(self):
        """
        tests the 'public_repos' method
        """
        GH_CLIENT = client.GithubOrgClient(TEST_ORG_NAME)

        GH_CLIENT_ORG = GH_CLIENT.org
        self.assertIn("repos_url", GH_CLIENT_ORG)

        self.assertEqual(
            GH_CLIENT.public_repos(APACHE2_LICENSE),
            PUBLIC_REPOS_APACHE2_OUTPUT
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.get_patcher.stop()
