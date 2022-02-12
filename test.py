import unittest
from src.auth import Base64Codec
from src.auth import Tokens


class TestAuth(unittest.TestCase):
    def test_base64_encoding(self):
        utf8_s = "loremipsum"
        correct_utf8_base64_s = "bG9yZW1pcHN1bQ=="
        output_s = Base64Codec.encode(utf8_s)
        self.assertEqual(output_s, correct_utf8_base64_s)

    def test_create_base64encoded_auth_value(self):
        client_id = "test_id"
        client_secret = "test_secret"
        correct_auth_value = "dGVzdF9pZDp0ZXN0X3NlY3JldA=="
        token = Tokens()
        output_auth_value = token.create_base64encoded_auth_value(client_id,
                                                                  client_secret)
        self.assertEqual(output_auth_value, correct_auth_value)


if __name__ == "__main__":
    unittest.main()
