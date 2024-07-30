# TripRouterTSP
Provides a route for road trip by taking in real world locations.

Asks for user input for different locations. Computes road distances between them using Google DistanceMatrix API. Solves a Traveling Salesman Problem using an integer program (Miller-Tucker-Zemlin) formulation to get the shortest distance path from a starting location, visiting all locations once, and terminating back at the starting location.

You would need your Google DistanceMatrix API key and a Gurobi license.

Just did it to see how a big road trip across the continental United States would look like.

TO DO:
1. Try alternate methods to compute distances. Possibly approximate with Euclidean distances if only location data (i.e. latitude and longitude, maybe elevation) is freely available.
2. Substitute PuLP instead of Gurobi. Or other free alternatives?
3. Include heuristic or approximation methods if there are a large number of locations. Seems to work upto ~20 locations just fine. If not, consider removing locations too close to one another (when compared to others) if the solver takes too long to converge. 
