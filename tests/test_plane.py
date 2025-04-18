import pytest

def test_plane_intialization(plane):
    assert plane.width == 100
    assert plane.height == 100
    assert len(plane.food) == 1

def test_food_spawn(plane):
    food = plane.food
    assert food[0][0] == 50
    assert food[0][1] == 50