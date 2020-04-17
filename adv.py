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


reverese_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def Maze():
    traversal_path = []
    reverse_paths = []
    visited_rooms = {}

    # add the first room
    visited_rooms[player.current_room.id] = player.current_room.get_exits()
    # Stop when we add all the rooms to visited_rooms
    while len(visited_rooms) < len(room_graph)-1:
        # if room not in visited_rooms
        if player.current_room.id not in visited_rooms:
            # add the room to visited_rooms
            visited_rooms[player.current_room.id] = player.current_room.get_exits()
            # remove the reverse previous path so that we dont end up with the previous room
            visited_rooms[player.current_room.id].remove(reverse_paths[-1])
        # if the room with no paths
        while len(visited_rooms[player.current_room.id]) == 0:
            path = reverse_paths.pop()
            print("path", path)
            player.travel(path)
            traversal_path.append(path)
        # else room in visited_rooms
        else:
            get_path = visited_rooms[player.current_room.id].pop()
            reverse_paths.append(reverese_directions[get_path])
            # move to another room
            player.travel(get_path)
            traversal_path.append(get_path)
    return traversal_path


traversal_path = Maze()
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
