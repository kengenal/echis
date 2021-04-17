class BadAppleMusicCredentialsException(Exception):
    message = "Check your secret key"

    def __str__(self):
        return self.message
