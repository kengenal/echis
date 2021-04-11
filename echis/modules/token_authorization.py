import base64
import datetime

from dataclasses import dataclass
from typing import Optional, Dict

import jwt
import requests

from echis.modules.endpoints import AppleMusicEndpoints
from echis.modules.exceptions import BadAppleMusicCredentialsException


@dataclass
class SpotifyAuthorization:
    client_id: str
    client_secret: str
    token_type: Optional[str] = None
    expires_in: datetime = datetime.datetime.now()
    token: Optional[str] = None
    token_url = "https://accounts.spotify.com/api/token"

    def set_client_id(self, client_id: str):
        self.client_id = client_id

    def set_client_secret(self, client_secret: str):
        self.client_secret = client_secret

    def create_base64(self) -> bytes:
        auth = f"{self.client_id}:{self.client_secret}"
        auth_base = base64.b64encode(auth.encode())
        return auth_base

    @property
    def get_body(self) -> Dict:
        return {
            "grant_type": "client_credentials",
        }

    @property
    def get_headers(self) -> Dict:
        return {
            "Authorization": f"Basic {self.create_base64().decode()}"
        }

    @property
    def is_active(self) -> bool:
        return self.expires_in > datetime.datetime.now()

    def get_token(self):
        try:
            rq = requests.post(url=self.token_url, headers=self.get_headers, data=self.get_body)
            if rq.status_code in range(200, 299):
                json = rq.json()
                self.token = json["access_token"]
                self.expires_in = datetime.datetime.now() + datetime.timedelta(seconds=json["expires_in"])
                self.token_type = json["token_type"]
        except Exception:
            raise Exception("Cannot get token from spotify")


class AppleMusicToken:
    def __init__(self, secret_key: str, key_id: str, team_id: str):
        """
        This class is used to connect to the Apple Music API and make requests for catalog resources
        :param secret_key: Secret Key provided by Apple
        :param key_id: Key ID provided by Apple
        :param team_id: Team ID provided by Apple
        """

        self._secret_key = secret_key
        self._key_id = key_id
        self._team_id = team_id
        self._alg = 'ES256'  # encryption algo that Apple requires
        self.token = ""  # encrypted api token
        self.headers: Dict = {}
        self.endpoints = AppleMusicEndpoints()

    def generate_token(self, session_length: float = 30.0):
        """
        Generate encrypted token to be used by in API requests.
        Set the class token parameter.
        :param session_length: Length Apple Music token is valid, in hours
        """
        headers = {
            'alg': self._alg,
            'kid': self._key_id
        }
        payload = {
            'iss': self._team_id,  # issuer
            'iat': int(datetime.datetime.now().timestamp()),  # issued at
            'exp': int((datetime.datetime.now() + datetime.timedelta(minutes=session_length)).timestamp())
        }
        try:
            token = jwt.encode(payload, self._secret_key.strip(), algorithm=self._alg, headers=headers)
            self.token = token if type(token) is not bytes else token.decode()
            self._generate_header()
        except Exception:
            raise BadAppleMusicCredentialsException()

    def _generate_header(self):
        if token := self.token:
            self.headers["Authorization"] = f"Bearer {token}"
