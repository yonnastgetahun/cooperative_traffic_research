"""Offline LinkedIn OAuth scope parser regressions: no secrets or API calls."""
import unittest
from authorize_local import parse_scopes, SCOPES


class LinkedInScopeParsingTests(unittest.TestCase):
    def test_supported_formats_grant_all_required_scopes(self):
        expected = set(SCOPES.split())
        examples = (
            "openid profile w_member_social",
            "openid,profile,w_member_social",
            "openid%20profile%20w_member_social",
            "openid+profile+w_member_social",
            "openid%2Cprofile%2Cw_member_social",
            "openid%2520profile%2520w_member_social",
            ["openid", "profile", "w_member_social"],
            "openid profile email w_member_social",
        )
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(expected.issubset(parse_scopes(example)))

    def test_missing_permission_not_assumed_granted(self):
        self.assertNotIn("w_member_social", parse_scopes("openid profile"))
        self.assertEqual(parse_scopes(None), set())
        self.assertEqual(parse_scopes(""), set())
        self.assertEqual(parse_scopes({"scope": "openid profile"}), set())


if __name__ == "__main__":
    unittest.main()
