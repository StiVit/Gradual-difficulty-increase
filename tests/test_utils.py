from app.utils.helpers import get_closest_edge, get_direction
from app.utils.spawn_agent import spawn_agent

def test_get_closest_edge(agent):
    closest_edge = get_closest_edge(agent, 100, 100)
    assert closest_edge[0] == 0
    assert closest_edge[1] == 10

def test_get_direction():
    assert get_direction([0, 0, 0, 1]) == 'd'
    assert get_direction([0, 0, 1, 0]) == 'r'
    assert get_direction([0, 1, 0, 0]) == 'u'
    assert get_direction([1, 0, 0, 0]) == 'l'

def test_spawn_agent():
    agent = spawn_agent(0, 1, 20, 20)
    assert agent.x == 10
    assert agent.y == 10