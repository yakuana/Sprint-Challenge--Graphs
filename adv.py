from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from structures import Stack, Queue 

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

mapDictionary = {}

# search for shortest path 
def bfs(start_room): 
    q = Queue()
    q.enqueue([start_room]) # enqueue starting point = start_room
    visited = set() 

    # while queue is not empty 
    while q.size() > 0:
        path = q.dequeue()         # pop first available path
        current_room = path[-1]    # current_room = last item in the path
        visited.add(current_room)

        # traverse each direction in current_room
        for direction in mapDictionary[current_room]:
            if mapDictionary[current_room][direction] == '?':
                return path
            elif mapDictionary[current_room][direction] not in visited:
                new_path = list(path)                                      # create a new path
                new_path.append(mapDictionary[current_room][direction])    # append the direction to new path
                q.enqueue(new_path) 



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
