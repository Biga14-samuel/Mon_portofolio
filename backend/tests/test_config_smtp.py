import unittest

from app.config import Settings


class TestSMTPConfig(unittest.TestCase):
    def test_smtp_credentials_are_normalized(self):
        settings = Settings(
            database_url="sqlite:///./portfolio.db",
            jwt_secret="secret-test",
            admin_username="admin",
            admin_password_hash="hashed-password",
            smtp_user=" user@gmail.com ",
            smtp_password="jdth spya fytm kwvl",
            smtp_recipient=" recipient@gmail.com ",
        )

        self.assertEqual(settings.smtp_user, "user@gmail.com")
        self.assertEqual(settings.smtp_password, "jdthspyafytmkwvl")
        self.assertEqual(settings.smtp_recipient, "recipient@gmail.com")


if __name__ == "__main__":
    unittest.main()
