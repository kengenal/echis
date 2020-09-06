import base64
import datetime

from dataclasses import dataclass
from typing import Optional, Dict

import requests


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
