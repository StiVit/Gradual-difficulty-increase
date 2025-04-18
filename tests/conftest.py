import pytest
from app.simulation.agent import Agent
from app.simulation.environment import Plane

@pytest.fixture
def agent():
    agent = Agent(10, 10)
    return agent

@pytest.fixture
def plane():
    plane = Plane(100, 100, 1)
    return plane