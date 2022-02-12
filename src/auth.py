from abc import ABC, abstractmethod
import requests
import base64
from .custom_exception_check import request_call_with_exception_check


class StringCodecs(ABC):
    """Blueprint for adding new codecs"""

    @classmethod
    @abstractmethod
    def encode(cls, s: str):
        raise NotImplementedError


class Base64Codec(StringCodecs):
    """Requires "base64" library"""

    @classmethod
    def encode(cls, s: str):
        """
        Argument :
            s (str) : UTF8 encoded string
        Returns :
            s (str) : UTF8 encoded string
        """
        binary_s = s.encode()
        binary_base64encoded_s = base64.b64encode(binary_s)
        utf8_base64encoded_s = binary_base64encoded_s.decode()
        return utf8_base64encoded_s


class Tokens:
    """
    The tokens in the Token class :

        1. Access Token for "Client Credentials Flow"

    Requires :
        client_id     : Developer's client id
        client_secret : Developer's client secret


    (Another token type refresh token is required for requests
     that require user permission.)

    How to obtain a token to make track search and receive datas from Spotify:

        -> Call request_client_credential_access_token method
                Returns a header that contains access token.
    """
    def create_base64encoded_auth_value(self,
                                        client_id,
                                        client_secret) -> str:
        """
        Arguments :
            client_id     (str) : Developer's client_id
            client_secret (str) : Developer's client_secret

        Returns :
            Authorization Value : Basic <base64 encoded client_id:client_secret>
        """
        auth_value = f"{client_id}:{client_secret}"
        auth_value = Base64Codec.encode(auth_value)
        return auth_value

    def request_client_credential_access_token(self,
                                               client_id,
                                               client_secret) -> requests.models.Response:
        """
        Purpose :
            Getting the "Access Token"
            to make search requiest in spotify and retrieve search results.

        Spotify API, Client Credentials Flow
        Section 1 ->   Have your application request authorization

                ! Does not require user's authorization for access.

        Requires :
            Authorization Value : Basic <base64 encoded client_id:client_secret>

        Returns :
            {
                "access_token": "NgCXRKc...MzYjw",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        """
        auth_value = self.create_base64encoded_auth_value(client_id,
                                                          client_secret)

        endpoint = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "client_credentials"
            }
        headers = {
            "Authorization": f"Basic {auth_value}"
            }

        r = request_call_with_exception_check(
                lambda: requests.post(endpoint, data=data, headers=headers)
                )
        return r
