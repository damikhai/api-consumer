from unittest.mock import AsyncMock

import pytest

from clients.cluster_client import ClusterClient
from clients.http_client import HttpClient
from config import Config

env = Config()


@pytest.fixture
def http_client():
    client = AsyncMock(spec=HttpClient)
    return client


@pytest.fixture
def cluster_client(http_client):
    return ClusterClient(base_url=env.BASE_URL, hosts=env.HOSTS, http_client=http_client)
