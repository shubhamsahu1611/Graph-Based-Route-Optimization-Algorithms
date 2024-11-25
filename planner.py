from flight import Flight

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def is_empty(self):
        return self.size == 0

    def append_at_end(self, data):
        new_node = self.Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
        self.size += 1

    def append_at_left(self, data):
        new_node = self.Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
        self.size += 1

    def pop_from_end(self):
        if self.is_empty():
            raise IndexError("pop from an empty deque")
        value = self.rear.data
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.rear = self.rear.prev
            self.rear.next = None
        self.size -= 1
        return value

    def pop_from_left(self):
        if self.is_empty():
            raise IndexError("pop from an empty deque")
        value = self.front.data
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty deque")
        return self.rear.data

    def peek_from_left(self):
        if self.is_empty():
            raise IndexError("peek from an empty deque")
        return self.front.data

    def __len__(self):
        return self.size

class Heap:
    def __init__(self, comparison_function, init_array=[]):
        self.arr = [-1]
        self.size = 0
        self.comp = comparison_function
        for item in init_array:
            self.insert(item)

    def insert(self, value):
        self.size += 1
        self.arr.append(value)
        idx = self.size

        while idx > 1:
            parent_idx = idx // 2
            if self.comp(self.arr[idx], self.arr[parent_idx]):
                self.arr[parent_idx], self.arr[idx] = self.arr[idx], self.arr[parent_idx]
                idx = parent_idx
            else:
                return

    def extract(self):
        if self.size == 0:
            return None
        root_value = self.arr[1]
        self._remove_root()
        return root_value

    def top(self):
        if self.size == 0:
            return None
        return self.arr[1]

    def _remove_root(self):
        if self.size == 0:
            return

        self.arr[1] = self.arr[self.size]
        self.size -= 1
        self.arr.pop()

        idx = 1
        while idx <= self.size:
            left_idx = 2 * idx
            right_idx = 2 * idx + 1
            largest = idx

            if left_idx <= self.size and self.comp(self.arr[left_idx], self.arr[largest]):
                largest = left_idx

            if right_idx <= self.size and self.comp(self.arr[right_idx], self.arr[largest]):
                largest = right_idx

            if largest != idx:
                self.arr[idx], self.arr[largest] = self.arr[largest], self.arr[idx]
                idx = largest
            else:
                break

    def is_empty(self):
        return self.size == 0

class Planner:
    def __init__(self, flights):
        self.total_flights = len(flights) + 1
        self.no_of_city = max(max(flight.start_city, flight.end_city) for flight in flights)
        self._initialize_graph(flights)

    def _initialize_graph(self, flights):
        self.flight_city_graph = [[] for _ in range(self.no_of_city + 1)]
        idx = 0
        while idx < len(flights):
            flight = flights[idx]
            self.flight_city_graph[flight.start_city].append(flight)
            idx += 1

    def _backtrack_path(self, prev_flight, end_city, start_city):
        if prev_flight[end_city] is None:
            return []
        path = []
        current_city = end_city
        while True:
            if current_city == start_city:
                i, j = 0, len(path) - 1
                while i < j:
                    path[i], path[j] = path[j], path[i]
                    i += 1
                    j -= 1
                return path
            flight = prev_flight[current_city]
            path.append(flight)
            current_city = flight.start_city

    def _process_least_flights(self, start_city, end_city, t1, t2):
        best_arrival = [(float('inf'), float('inf'))] * (self.no_of_city + 1)
        best_arrival[start_city] = (t1 - 20, 0)
        prev_flight = [None] * (self.no_of_city + 1)

        queue = Deque()
        queue.append_at_end((start_city, t1 - 20, 0))
        visited=[False]*(self.total_flights+5)
        while not queue.is_empty():
            city, arrival, flight_count = queue.pop_from_left()

            if (arrival, flight_count) != best_arrival[city]:
                continue

            for flight in self.flight_city_graph[city]:
                if visited[flight.flight_no]:
                    continue
                if (flight.departure_time >= t1 and flight.arrival_time <= t2 and flight.departure_time >= arrival + 20):
                    new_arrival = flight.arrival_time
                    new_count = flight_count + 1

                    curr_arrival, curr_count = best_arrival[flight.end_city]
                    if (new_count < curr_count or (new_count == curr_count and new_arrival < curr_arrival)):
                        visited[flight.flight_no]=True
                        best_arrival[flight.end_city] = (new_arrival, new_count)
                        prev_flight[flight.end_city] = flight
                        queue.append_at_end((flight.end_city, new_arrival, new_count))

        return self._backtrack_path(prev_flight, end_city, start_city)

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        if start_city==end_city or t1>t2:
            return []
        return self._process_least_flights(start_city, end_city, t1, t2)

    class PathNode:
        def __init__(self, city, cost, time, prev_node=None, flight=None):
            self.city = city
            self.cost = cost
            self.time = time
            self.prev_node = prev_node
            self.flight = flight

    def reconstruct_path(self, destination_node):
        path = []
        node = destination_node
        while True:
            if node.prev_node is None:
                i, j = 0, len(path) - 1
                while i < j:
                    path[i], path[j] = path[j], path[i]
                    i += 1
                    j -= 1
                return path
            path.append(node.flight)
            node = node.prev_node

    def _process_cheapest_route(self, source_city, target_city, start_time, end_time):
        heap = Heap(lambda a, b: a[0] < b[0] , [])
        start_node = self.PathNode(source_city, 0, start_time - 20)
        heap.insert((0, start_time - 20, start_node))

        min_cost = float('inf')
        destination_node = None
        visited=[False]*(self.total_flights+5)

        while not heap.is_empty():
            current_cost, arrival_time, node = heap.extract()
            city = node.city

            if city == target_city:
                if current_cost < min_cost:
                    destination_node = node
                    min_cost= current_cost
                    break

            self._explore_flights(heap, node, start_time, end_time, visited)

        return self.reconstruct_path(destination_node) if destination_node else []

    def _explore_flights(self, heap, node, start_time, end_time, visited):
        for flight in self.flight_city_graph[node.city]:
            if visited[flight.flight_no]:
                continue
            if flight.departure_time >= start_time and flight.arrival_time <= end_time and flight.departure_time >= node.time + 20:
                new_cost = node.cost + flight.fare
                visited[flight.flight_no]=True
                next_node = self.PathNode(flight.end_city, new_cost, flight.arrival_time, prev_node=node, flight=flight)
                heap.insert((new_cost, flight.arrival_time, next_node))

    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city==end_city or t1>t2:
            return []
        return self._process_cheapest_route(start_city, end_city, t1, t2)

    class HeapEntry:
        def __init__(self, flight_count, cost, city, arrival_time, node):
            self.flight_count = flight_count
            self.cost = cost
            self.city = city
            self.arrival_time = arrival_time
            self.node = node

    class FlightNode:
        def __init__(self, city, flight_count, cost, time, prev_node=None, flight=None):
            self.city = city
            self.flight_count = flight_count
            self.cost = cost
            self.time = time
            self.prev_node = prev_node
            self.flight = flight

    def _process_least_flights_cheapest_route(self, source_city, target_city, start_time, end_time):
        heap = Heap(lambda a, b: (a.flight_count, a.cost)<(b.flight_count, b.cost), [])
        start_node = self.FlightNode(source_city, 0, 0, start_time - 20)
        heap.insert(self.HeapEntry(0, 0, source_city, start_time - 20, start_node))
        visited=[False]*(self.total_flights+5)
        destination_node = None
        min=(float('inf'), float('inf'))

        while not heap.is_empty():
            current_entry = heap.extract()
            city, arrival_time, node = current_entry.city, current_entry.arrival_time, current_entry.node

            if city == target_city and arrival_time <= end_time:
                if (node.flight_count, node.cost) < min:
                    destination_node = node
                    min = (node.flight_count, node.cost) 
                    break                

            self._explore_least_cost_flights(heap, node, start_time, end_time, visited)

        return self.reconstruct_path(destination_node) if destination_node else []

    def _explore_least_cost_flights(self, heap, node, start_time, end_time, visited):
        for flight in self.flight_city_graph[node.city]:
            if visited[flight.flight_no]:
                continue
            if flight.departure_time >= start_time and flight.arrival_time <= end_time and flight.departure_time >= node.time + 20:
                visited[flight.flight_no]=True
                new_cost = node.cost + flight.fare
                new_flight_count = node.flight_count + 1
                next_node = self.FlightNode(flight.end_city, new_flight_count, new_cost, flight.arrival_time, prev_node=node, flight=flight)
                heap.insert(self.HeapEntry(new_flight_count, new_cost, flight.end_city, flight.arrival_time, next_node))

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city==end_city or t1>t2:
            return []
        return self._process_least_flights_cheapest_route(start_city, end_city, t1, t2)
