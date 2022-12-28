# Dictionary containing next direction based
# on current direction and input
TURNS = {
    # Moving right
    ((1, 0), "R"): (0, 1),
    ((1, 0), "L"): (0, -1),

    # Moving left
    ((-1, 0), "R"): (0, -1),
    ((-1, 0), "L"): (0, 1),

    # Moving down
    ((0, 1), "R"): (-1, 0),
    ((0, 1), "L"): (1, 0),

    # Moving up
    ((0, -1), "R"): (1, 0),
    ((0, -1), "L"): (-1, 0),
}

# Dictionary containing information regarding "zone" jumping
MOVEMENTS = {
    1:{
        (-1, 0): (4, (1, 0), (0, 1)),
        (0, -1): (6, (1, 0), (1, 1)),
    },
    2:{
        (1, 0): (5, (-1, 0), (0, 1)),
        (0, 1): (3, (-1, 0), (1, 1)),
        (0, -1): (6, (0, -1), (0, 1)),
    },
    3:{
        (1, 0): (2, (0, -1), (1, 1)),
        (-1, 0): (4, (0, 1), (1, 1)),
    },
    4:{
        (-1, 0): (1, (1, 0), (0, 1)),
        (0, -1): (3, (1, 0), (1, 1)),
    },
    5:{
        (1, 0): (2, (-1, 0), (0, 1)),
        (0, 1): (6, (-1, 0), (1, 1)),
    },
    6:{
        (1, 0): (5, (0, -1), (1, 1)),
        (0, 1): (2, (0, 1), (0, 1)),
        (-1, 0): (1, (0, 1), (1, 1)),
    },
}

# Ranges of the different zones on the map
# in total there are 6 zones which makes up a map
ZONES = {
    1: (range(50, 100), range(0, 50)),
    2: (range(100, 150), range(0, 50)),
    3: (range(50, 100), range(50, 100)),
    4: (range(0, 50), range(100, 150)),
    5: (range(50, 100), range(100, 150)),
    6: (range(0, 50), range(150, 200)),
}

