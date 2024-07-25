# TripRouterTSP
Provides a route for road trip by taking in real world locations.

Asks for user input for different locations. Computes road distances between them using Google DistanceMatrix API. Solves a Traveling Salesman Problem using MTZ (https://dl.acm.org/doi/abs/10.1145/321043.321046) formulation to get the shortest distance path from a starting location, visiting all locations once, and terminating back at the starting location.

TO DO:
try alternate methods to compute distances. Possibly approximate with Euclidean distances if only location data (i.e. latitude and longitude, maybe elevation) is freely available.
