from typing import List, Literal, Optional

import httpx
from loguru import logger

from clients.http_client import HttpClient


class ClusterClient:
    def __init__(self, base_url: str, hosts: List[str], http_client: HttpClient = None):
        self.base_url = base_url
        self.hosts = hosts
        self.http_client = http_client or HttpClient()

    async def create_group(self, group_id: str) -> bool:
        data = {"groupId": group_id}
        success_hosts = []

        for host in self.hosts:
            try:
                await self.http_client.request("POST", f"http://{host}{self.base_url}", json=data)
                success_hosts.append(host)
            except httpx.HTTPStatusError as err:
                logger.error(f"Failed to create group on {host}: {err.response.status_code}")
                # Restore the state of the cluster before creation
                await self._rollback("POST", success_hosts, group_id)
                return False
            except Exception as err:
                logger.error(f"Error creating group on {host}: {err}")
                # Restore the state of the cluster before creation
                await self._rollback("POST", success_hosts, group_id)
                return False
        return True

    async def delete_group(self, group_id: str) -> bool:
        data = {"groupId": group_id}
        success_hosts = []

        for host in self.hosts:
            try:
                await self.http_client.request("DELETE", f"http://{host}{self.base_url}", json=data)
                success_hosts.append(host)
            except httpx.HTTPStatusError as err:
                logger.error(f"Failed to delete group on {host}: {err.response.status_code}")
                # Restore the state of the cluster before deletion
                await self._rollback("DELETE", success_hosts, group_id)
                return False
            except Exception as err:
                logger.error(f"Error deleting group on {host}: {err}")
                # Restore the state of the cluster before deletion
                await self._rollback("DELETE", success_hosts, group_id)
                return False
        return True

    async def get_group(self, group_id: str) -> Optional[dict]:
        url = f"{self.base_url}{group_id}/"

        for host in self.hosts:
            try:
                response = await self.http_client.request("GET", f"http://{host}{url}")
                return response.json()
            except httpx.HTTPStatusError as err:
                if err.response.status_code == httpx.codes.NOT_FOUND:
                    continue  # Try the next host if group not found
                logger.error(f"Failed to get group on {host}: {err.response.status_code}")
            except Exception as err:
                logger.error(f"Error getting group on {host}: {err}")
        return None

    async def _rollback(self, http_method: Literal["POST", "DELETE"], hosts: List[str], group_id: str) -> None:
        rollback_mapping = {
            "POST": "DELETE",
            "DELETE": "POST"
        }
        data = {"groupId": group_id}
        for host in hosts:
            try:
                await self.http_client.request(
                    rollback_mapping[http_method],
                    f"http://{host}{self.base_url}",
                    json=data
                )
            except Exception as e:
                logger.error(f"Rollback failed on {host}: {e}")
