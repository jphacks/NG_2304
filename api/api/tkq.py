import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker

from api.settings import settings

broker = ZeroMQBroker()

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "api.web.application:get_app",
)
