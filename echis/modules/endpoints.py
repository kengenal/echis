from dataclasses import dataclass


@dataclass
class AppleMusicEndpoints:
    root: str = "https://api.music.apple.com/v1"
    playlists: str = root + "catalog/{}/playlists/{}/tracks?limit=300"  # $1-store, $2-id
