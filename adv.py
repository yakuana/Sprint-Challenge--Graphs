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

# graph 
mapDictionary = {}

def bfs(start_room_id): 
    # breath first search for shortest path 

    q = Queue()
    q.enqueue([start_room_id]) # enqueue starting point = start_room_id
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


def search(starting_room): 
    # dft, explore all paths of maze until exit is path found

    opp_directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
    visited_rooms = 0  # visited room counter 
    
    # complete when mapDictionary length == room_graph length 
    while len(mapDictionary) != len(room_graph):
        # current room info
        current_room = player.current_room
        room_id = current_room.id
        
        # graph (dictionary) of rooms with [n,s,e,w] as key and either room_id or '?' as value
        room_dict = {}

        if room_id not in mapDictionary:
            # find the possible exits
            for i in current_room.get_exits():
                # set key at [i] value to '?'
                room_dict[i] = '?'
            
            # update room using traversal_path array 
            if traversal_path:
                prevRoom = opp_directions[traversal_path[-1]]    # previous room is the reverse of last travel path
                room_dict[prevRoom] = visited_rooms              # add the prevRoom to the room_dict
            
            # add room_dict to mapDictionary 
            mapDictionary[room_id] = room_dict
        else:
            # set room_dict to room at index room_id in mapDictionary
            room_dict = mapDictionary[room_id]

        # will store list of possible exits    
        possible_exits = list()

        # iterate through room_dict
        for direction in room_dict:
            if room_dict[direction] == '?':
                # append all '?'s to possible_exits list 
                possible_exits.append(direction)

        # if '?'s found 
        if len(possible_exits) != 0:
            random.shuffle(possible_exits)      # reorganize order of list 
            direction = possible_exits[0]       # set direction to possible direction at index[0]  
            traversal_path.append(direction)    # append that direction to the traversal path
           
            # move player in new direction using travel function and update mapDictionary with room_move id 
            player.travel(direction)
            room_move = player.current_room
            mapDictionary[current_room.id][direction] = room_move.id
            visited_rooms = current_room.id
        else:
            # BFS to search for next exits/possible rooms using room_id
            next_room = bfs(room_id)
           
            # if the path of next_room has results from bfs
            if next_room is not None and len(next_room) > 0:
                # iterate the length of the room to get room id's
                for i in range(len(next_room) - 1):
                    # iterate the mapDictionary's next_room at current to get cardinal directions 
                    for direction in mapDictionary[next_room[i]]:
                        # if direction of next_room[i] == the following room's, then found through bfs
                        if mapDictionary[next_room[i]][direction] == next_room[i + 1]:
                            # append travel path and move player 
                            traversal_path.append(direction)
                            player.travel(direction)
            else:
                break

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
