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
our_graph = {}
reverse = []
opposite_direction = {'e': 'w', 'w': 'e', 'n': 's', 's': 'n'}

# starting room
our_graph[player.current_room.id] = player.current_room.get_exits()

# begins traversal loop
while len(our_graph) < len(room_graph)-1:

    # track room
    # if room is not visited
    if player.current_room.id not in our_graph:

        # add it to graph
        our_graph[player.current_room.id] = player.current_room.get_exits()

        # remove latest direction from the unexplored exits
        last_direction = reverse[-1]
        our_graph[player.current_room.id].remove(last_direction)

    # track exits
    # there is no unexplored exits
    # loop while there is no exits
    while len(our_graph[player.current_room.id]) == 0:

        # remove latest direction from reverse
        moveBack = reverse.pop()

        # add that latest one to traversal_path
        traversal_path.append(moveBack)

        # travel back at it
        player.travel(moveBack)

    # Is there an available exits?
    # get first available exit
    moveForward = our_graph[player.current_room.id].pop(0)

    # add exit to traversal_path
    traversal_path.append(moveForward)

    # add opposite direction to reverse
    reverse.append(opposite_direction[moveForward])

    # travel to exit
    player.travel(moveForward)


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
