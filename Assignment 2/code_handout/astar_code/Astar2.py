import heapq
import Map


class Node:
    """
    A node class for A* search algorithm
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.neighbors = []
        self.g = 0
        self.h = 0
        self.f = 0

    # defining equal for purposes of heap queue
    def __eq__(self, other):
        return self.position == other.position
    
    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def astar(map, start, end):
    """
    Returns a list of cells as a path from the given start to the given end in the given Samfundet map
    """
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)
    
    # Loop until you find the end
    while len(open_list) > 0: 
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # what squares do we search (no diagonals)
        (x,y) = current_node.position
        neighbors = ([x-1, y], [x+1, y], [x, y-1], [x, y+1])
        current_node.neighbors = neighbors

        # Loop neighbors
        for next in neighbors:
            # Get value from map
            map_value = map[next[0]][next[1]]
            # Check if the node is a wall
            if(map_value == ' # '):
                continue

            # Create a neighbor node
            neighbor = Node(current_node, next)

            # Check if the neighbor is in the closed list
            if (neighbor in closed_list):
                continue
            
            # Generate temporal g(n), keeping in mind the cells weight 
            if (map_value == " . "):
                temp_g = current_node.g + 1
            elif (map_value == " , "):
                temp_g = current_node.g + 2
            elif (map_value == " ; "):
                temp_g = current_node.g + 3
            else:
                temp_g = current_node.g + 4
            
            control_flag = 0
            for k in range(len(open_list)):
                # Neighbor is in the open list
                if neighbor.position == open_list[k].position:
                    # Update g(n) if it's less cost
                    if temp_g < open_list[k].g:
                        # Generate g(n) and h(n)(Manhattan distance)
                        open_list[k].g = temp_g
                        open_list[k].h= abs(open_list[k].position[0] - end_node.position[0]) + abs(open_list[k].position[1] - end_node.position[1])
                        open_list[k].f = open_list[k].g + open_list[k].h
                        open_list[k].parent = current_node
                    control_flag = 1

            # Neighbor not in the open list
            if control_flag != 1:
                # Generate g(n)and h(n)(Manhattan distance)
                neighbor.g = temp_g
                neighbor.h = abs(neighbor.position[0] - end_node.position[0]) + abs(neighbor.position[1] - end_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                if add_to_open(open_list, neighbor):
                    # Add neighbor to open list
                    heapq.heappush(open_list, neighbor)
    
    # Return None, no path is found
    return None

# Check if a neighbor should be added to open list
def add_to_open(open_list, neighbor):
    for node in open_list:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

# Draw the result path in the string map
def draw_path(map, path):
    for step in path:
        map[step[0]][step[1]] = ' X '
    return map

def main():

    map_obj = Map.Map_Obj(task=4)
    string_map = map_obj.get_maps()[1]
    start = map_obj.get_start_pos()
    end = map_obj.get_end_goal_pos()

    path = astar(string_map, start, end)
    map_obj.show_map(draw_path(string_map, path))
    
if __name__ == '__main__':
    main()