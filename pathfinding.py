from collections import deque


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]    #ways of getting to neighboring tiles
        #allows 8 way movement for enemy (current position is always 0, 0)
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):    #path becomes from start to goal but it only focuses on one step at a time
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}
        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:    #stop if current node is the goal (the player position)
                break
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node) #add the next adjacent node to the queue and move there if it hasnt been visited
                    visited[next_node] = cur_node   #the new node appended is now the current node
        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y+ dy) not in self.game.map.world_map]

    def get_graph(self):    #build graph of adjacent tiles
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)