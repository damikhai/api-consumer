from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from config import Config

env = Config()


@pytest.mark.asyncio
async def test_create_group_success(cluster_client, http_client):
    http_client.request.return_value = AsyncMock(status_code=httpx.codes.CREATED)

    result = await cluster_client.create_group("test_group")

    assert result is True
    assert http_client.request.call_count == len(env.HOSTS)


@pytest.mark.asyncio
async def test_create_group_failure(cluster_client, http_client):
    http_client.request.side_effect = httpx.HTTPStatusError(
        "Error",
        request=None,
        response=AsyncMock(status_code=httpx.codes.INTERNAL_SERVER_ERROR)
    )

    result = await cluster_client.create_group("test_group")

    assert result is False
    assert http_client.request.call_count == 1  # It should stop after the first failure


@pytest.mark.asyncio
async def test_delete_group_success(cluster_client, http_client):
    http_client.request.return_value = AsyncMock(status_code=httpx.codes.OK)

    result = await cluster_client.delete_group("test_group")

    assert result is True
    assert http_client.request.call_count == len(env.HOSTS)


@pytest.mark.asyncio
async def test_delete_group_failure(cluster_client, http_client):
    http_client.request.side_effect = httpx.HTTPStatusError(
        "Error",
        request=None,
        response=AsyncMock(status_code=httpx.codes.INTERNAL_SERVER_ERROR)
    )

    result = await cluster_client.delete_group("test_group")

    assert result is False
    assert http_client.request.call_count == 1  # It should stop after the first failure


@pytest.mark.asyncio
async def test_get_group_success(cluster_client, http_client):
    http_client.request.return_value = AsyncMock(
        status_code=httpx.codes.OK,
        json=Mock(return_value={'groupId': 'test_group'})
    )

    result = await cluster_client.get_group("test_group")

    assert result == {'groupId': 'test_group'}
    assert http_client.request.call_count == 1


@pytest.mark.asyncio
async def test_get_group_not_found(cluster_client, http_client):
    http_client.request.side_effect = httpx.HTTPStatusError(
        "Not found",
        request=None,
        response=AsyncMock(status_code=httpx.codes.NOT_FOUND)
    )

    result = await cluster_client.get_group("test_group")

    assert result is None
    assert http_client.request.call_count == len(env.HOSTS)


@pytest.mark.asyncio
async def test_rollback_create(cluster_client, http_client):
    http_client.request.return_value = AsyncMock(status_code=httpx.codes.OK)
    await cluster_client._rollback("POST", env.HOSTS, "test_group")

    assert http_client.request.call_count == len(env.HOSTS)
    for call in http_client.request.call_args_list:
        assert call[0][0] == "DELETE"
        assert call[1]['json'] == {'groupId': 'test_group'}


@pytest.mark.asyncio
async def test_rollback_delete(cluster_client, http_client):
    http_client.request.return_value = AsyncMock(status_code=httpx.codes.OK)
    await cluster_client._rollback("DELETE", env.HOSTS, "test_group")

    assert http_client.request.call_count == len(env.HOSTS)
    for call in http_client.request.call_args_list:
        assert call[0][0] == "POST"
        assert call[1]['json'] == {'groupId': 'test_group'}
