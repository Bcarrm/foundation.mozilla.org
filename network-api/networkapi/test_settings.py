from .settings import *  # noqa

# #############
# Specific settings for running tests

# #############
# Performance

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
