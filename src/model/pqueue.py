import heapq


class PriorityQueue(object):
    def __init__(self):
        self.elements = []

    @property
    def empty(self):
        """
        Return true if there are no elements in the queue, False otherwise.
        """
        return not self.elements

    def put(self, item, priority):
        """
        Add new item with priority to the queue.
        Item is placed in priority order.
        """
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """
        Return coordinates of the point with smallest priority.
        """
        return heapq.heappop(self.elements)[1]
