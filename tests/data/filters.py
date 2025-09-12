import pytest

INCORRECT_REGISTER_PARAMS = (pytest.param("di", "1234", "1234",
                           "Allowed username length should be from 3 to 50 characters", id="Incorrect login"),
                          pytest.param("diana", "12", "12",
                           "Allowed password length should be from 3 to 12 characters", id="Short password"),
                          pytest.param("diana", "1234567890abc", "1234567890abc",
                           "Allowed password length should be from 3 to 12 characters", id="Long password"),
                          pytest.param("didarphin", "123", "123",
                          "Username `didarphin` already exists", id="Account exists")
                             )

INCORRECT_AUTH_PARAMS = (pytest.param("didarphin", "1234", id="Incorrect login"),
                          pytest.param("di", "123", id="Incorrect password")
                          )
