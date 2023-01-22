## Motivation

In some video games, paint or other opaque liquid is used as a game mechanic, allowing the player or enemies to cower areas on different surfaces. The best example of this might be the *Splatoon*-series, but it has been used in at least *Super Mario Sunshine* as well.

However, it's not obvious at all how a mechanic like this should be implemented optimally. Since paint tends to form rather round shapes, just using triangles of a single color to form the paint would either look too rugged or it would require rendering a lot of triangles. Another option could be giving each surface its own texture on which the paint is drawn, but this would require a lot of memory, especially on large areas.

## Objective

The goal of this project is to create a demo application that simulates and renders paint on an even surface. The application will mainly consist of a canvas, on which the user can add drops of paint using the mouse. Each new droplet is merged with the painted areas already on the canvas. There may even be simulated interaction like surface tension around the edges of the painted areas, but since that might make the project overly complicated, I'd consider that optional for now.

The edges of the areas covered by paint, as well as the outlines of each new paint droplet are modeled using quadratic Bézier splines. When a new droplet intersects with existing paint on the canvas, the intersection points of the two splines are calculated, both splines are merged into one and the redundant parts of the new spline are removed. Since the painted area can have all kinds of weird concave shapes, and it might even holes in it, this is the part where the problem becomes algorithmically interesting. Unfortunately, I couldn't find any existing algorithms for this purpose, but I do have a pretty solid idea of my own.

The edges of the painted area can be rendered as triangles with a quadratic Bézier curve -shaped texture on them. The area inside the edges can be triangulated using an existing algorithm, but there's many options and I haven't decided which one I'll choose yet.
