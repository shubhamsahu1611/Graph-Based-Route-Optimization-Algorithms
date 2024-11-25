# Flight Planner

## Overview

The **Flight Planner** is a program designed to efficiently plan flight routes based on diverse user preferences, such as minimizing connections, reducing costs, or optimizing for the earliest arrival. It models real-world flight planning challenges with constraints like connecting times and flight capacity at airports.

---

## Features

The planner supports three main route optimization goals:

1. **Fewest Flights and Earliest Arrival**: Finds a route with the minimum number of flights and the earliest possible arrival.
2. **Cheapest Trip**: Finds the route with the lowest total fare.
3. **Fewest Flights and Cheapest Trip**: Finds a route with the minimum number of flights, choosing the cheapest among equivalent options.

---

## How It Works

The planner operates on a dataset of flights with the following attributes:
- **Flight No.**: Unique identifier for each flight.
- **Start City**: Departure city of the flight.
- **End City**: Arrival city of the flight.
- **Departure Time**: Time of departure (in minutes).
- **Arrival Time**: Time of arrival (in minutes).
- **Fare**: Cost of the flight.

### Constraints
- Maximum of 100 flights arriving at or leaving from any single city.
- A minimum gap of 20 minutes between consecutive connecting flights.

---

## Key Methods in `Planner` Class

- **`__init__(flights)`**: Initializes the planner with a list of `Flight` objects.
- **`least_flights_earliest_route(start_city, end_city, t1, t2)`**: Finds the route with the fewest flights and the earliest arrival.
- **`cheapest_route(start_city, end_city, t1, t2)`**: Finds the cheapest route.
- **`least_flights_cheapest_route(start_city, end_city, t1, t2)`**: Finds the route with the fewest flights and the lowest cost.

---

## Time Optimizations

- **Initialization**: `O(m)`
- **Route Finding**:
  - Fewest Flights & Earliest: `O(m)`
  - Cheapest: `O(m log m)`
  - Fewest Flights & Cheapest: `O(m log m)`

---
