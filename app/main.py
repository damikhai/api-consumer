import asyncio

from loguru import logger

from clients.cluster_client import ClusterClient, HttpClient
from config import Config


async def main_loop(env: Config) -> None:
    logger.info("Starting ClusterClient...")
    http_client = HttpClient()
    cluster_client = ClusterClient(base_url=env.BASE_URL, hosts=env.HOSTS, http_client=http_client)
    group_id = "example_group"
    while True:
        result = await cluster_client.create_group(group_id)
        logger.info(f"Create group result: {result}")
        await asyncio.sleep(env.WAIT_BETWEEN_RETRIES)  # Run the task every WAIT_BETWEEN_RETRIES

if __name__ == "__main__":
    env_variables = Config()
    asyncio.run(main_loop(env=env_variables))
