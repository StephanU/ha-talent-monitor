import logging
import os

from aiohttp import ClientSession

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)

BASE_URL = "https://www.talent-monitoring.com/prod-api"

class DataProvider():
    """Data provider accessing the MyGekko API"""

    def __init__(
        self,  username: str, password: str, session: ClientSession
    ):
        self._url = BASE_URL
        self._username = username or os.environ.get("PYTALENT_USERNAME")
        self._password = password or os.environ.get("PYTALENT_PASSWORD")
        self._session = session
        self._token = None

    def get_credentials(self):
        """Check whether the credentials are set."""
        if not self._username or not self.password:
            raise ValueError(
                "Credentials not provided via command line arguments or environment variables."
            )

    async def login(self):
        """Log in using the given credentials."""
        login_data = {"username": self._username, "password": self._password}
        response = await self._session.post(f"{self._url}/login", json=login_data)
        response_data = await response.json()
        if "token" in response_data:
            self._token = response_data["token"]
            _LOGGER.debug("Login successful - received token: %s", self._token)
        else:
            _LOGGER.error("Login failed. Got status code %s", response.status)
            raise AuthenticationError("Authentication failed")

    async def refresh_token(self):
        """Refresh the token."""
        _LOGGER.debug("Token expired. Refreshing token...")
        self.login()

    async def get_data(self, endpoint):
        """Get data from the given endpoint."""
        if not self._token:
            await self.login()
        headers = {"Authorization": f"Bearer {self._token}"}
        response = await self._session.get(f"{self._url}/{endpoint}", headers=headers)
        if response.status == 401:  # Unauthorized, token might be expired
            self.refresh_token()
            headers["Authorization"] = f"Bearer {self._token}"
            response = await self._session.get(f"{self._url}/{endpoint}", headers=headers)

        if response.status == 200:
            return await response.json()
        else:
            _LOGGER.error("Failed to fetch data. Status Code: %s", response.status)
            return None

class Entity:
    """Base class for TalentMonitor entities"""

    def __init__(self, entity_id: str, name: str) -> None:
        self.entity_id = entity_id
        self.name = name

class AuthenticationError(Exception):
    """AuthenticationError when connecting to the Talent API."""
    pass