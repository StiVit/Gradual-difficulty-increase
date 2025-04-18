from app.utils.helpers import get_closest_edge, get_direction
from app.utils.spawn_agent import spawn_agent
import pytest

def test_get_closest_edge(agent):
    closest_edge = get_closest_edge(agent, 100, 100)
    assert closest_edge[0] == 0
    assert closest_edge[1] == 10

@pytest.mark.parametrize("output, direction", [
    ([0, 0, 0, 1], 'd'),
    ([0, 0, 1, 0], 'r'),
    ([0, 1, 0, 0], 'u'),
    ([1, 0, 0, 0], 'l')
])
def test_get_direction(output, direction):
    assert get_direction(output) == direction

def test_invalid_output():
    with pytest.raises(ValueError, match="Wrong output format"):
        get_direction([0])
        get_direction(["", 3, 21, 1])

def test_spawn_agent():
    agent = spawn_agent(0, 1, 20, 20)
    assert agent.x == 10
    assert agent.y == 10