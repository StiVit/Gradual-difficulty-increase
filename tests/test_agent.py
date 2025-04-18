import pytest

def test_agent_spawn(agent):
    assert agent.x == 10
    assert agent.y == 10
    assert agent.energy == 1000
    assert agent.eaten == 0

def test_agent_movement_up(agent):
    agent.move("u")
    assert agent.x == 10
    assert agent.y == 11
    assert agent.energy == 999

def test_agent_movement_down(agent):
    agent.move("d")
    assert agent.x == 10
    assert agent.y == 9
    assert agent.energy == 999

def test_agent_movement_left(agent):
    agent.move("l")
    assert agent.x == 9
    assert agent.y == 10
    assert agent.energy == 999

def test_agent_movement_right(agent):
    agent.move("r")
    assert agent.x == 11
    assert agent.y == 10
    assert agent.energy == 999

def test_agent_perceive_food(agent, plane):
    perceived_food = agent.perceive_food(plane.food)
    plane_food = [food for food in plane.food if agent.distance_to(food) <= agent.sense]
    assert perceived_food == plane_food

def test_measure_distance(agent):
    distance = agent.distance_to((10, 10))
    assert distance == 0

def test_invalid_cooridnates(agent):
    with pytest.raises(ValueError, match="Invalid coordinates"):
        agent.distance_to((10.5, 10.5))
    
def test_type_casting(agent):
    distance = agent.distance_to((10.0, 10.0))
    assert distance == 0

def test_eat(agent):
    agent.eat()
    assert agent.eaten == 1
    assert agent.energy == 1010

def test_failed_eating(agent):
    agent.energy = 0
    agent.eat()
    assert agent.eaten == 0
    assert agent.energy == 0