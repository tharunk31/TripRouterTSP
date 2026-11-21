# TripRouterTSP
Provides a route for road trip by taking in real world locations.

Asks for user input for different locations. Obtains their latitudes and longitudes from [Open Street Map's nominatim](https://nominatim.openstreetmap.org/). Gets the distances between them using [Open Source Routing Machine](https://project-osrm.org/). Solves a Traveling Salesman Problem using an integer program (Dantzig-Fulkerson-Johnson) formulation to get the shortest distance path from a starting location, visiting all locations once, and terminating back at the starting location.

Just did it to see how a big road trip across the continental United States and Canada would look like 乁(ツ)ㄏ.
