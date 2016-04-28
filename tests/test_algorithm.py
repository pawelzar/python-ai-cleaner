from src.algorithm import *
from src.draw import draw_grid
from src.graph import *


diagram = GridWithWeights(20, 10)
for point in [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (1, 1), (1, 2), (2, 1), (2, 2)]:
    diagram.add_obstacle(point)
diagram.add_object((5, 5), '?')
diagram.add_object((5, 6), '?')
diagram.add_object((6, 5), '?')

point_start = (0, 0)
point_goal = (4, 8)
came_from, cost_so_far = a_star_search(diagram, point_start, point_goal)

draw_grid(diagram, point_to=came_from, start=point_start, goal=point_goal)
print()
draw_grid(diagram, width=2, number=cost_so_far, start=point_start, goal=point_goal)
print()
draw_grid(diagram, path=reconstruct_path(came_from, start=point_start, goal=point_goal))
print(reconstruct_path(came_from, start=point_start, goal=point_goal))
