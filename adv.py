from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
reverse = []
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# starting room
graph[player.current_room.id] = player.current_room.get_exits()

# begins traversal loop
while len(graph) < len(room_graph)-1:

    # track room
    # if room not visited
    if player.current_room.id not in graph:

        # add it & its' exits to graph
        graph[player.current_room.id] = player.current_room.get_exits()

        # remove last direction from its' unexplored exits
        last_direction = reverse[-1]
        graph[player.current_room.id].remove(last_direction)

    # track exits
    # no unexplored exits
    # loop while no exits (walking back through reverse until there are unexeplored exits)
    while len(graph[player.current_room.id]) == 0:

        # remove last direction from reverse
        goBack = reverse.pop()

        # add that last one to traversal_path
        traversal_path.append(goBack)

        # travel back at it
        player.travel(goBack)

    # available exits?
    # get first available exit
    goForward = graph[player.current_room.id].pop(0)

    # add exit to traversal_path
    traversal_path.append(goForward)

    # add opposite direction to reverse
    reverse.append(opposites[goForward])

    # travel to exit
    player.travel(goForward)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
