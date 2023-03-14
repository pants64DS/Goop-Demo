# Requirement Specification

## Motivation

In some video games, paint or other opaque liquid is used as a game mechanic, allowing the player or enemies to cover areas on different surfaces. The best example of this might be the *Splatoon* series, but it has been used in at least *Super Mario Sunshine* as well.

However, it's not at all obvious how a mechanic like this should be implemented optimally. Since paint tends to form rather round shapes, just using triangles of a single color to form the paint would either look too rugged or it would require rendering a lot of triangles. Another option could be giving each surface its own texture on which the paint is drawn, but this would require a lot of memory, especially in large areas.

## Objective

The goal of this project is to create a demo application that simulates and renders paint on an even surface. The application will mainly consist of a canvas, on which the user can add drops of paint using the mouse. Each new droplet is merged with the painted areas already on the canvas. There may even be simulated interaction like surface tension around the edges of the painted areas, but since that might make the project overly complicated, I consider that optional for now.

## Algorithms and Data Structures

The functionality of the application and the algorithms and data structures it uses can be split into three parts:

### 1. Finding the points of intersections of two quadratic Bézier curves
The edges of the areas covered by paint, as well as the outlines of each new paint droplet are defined as quadratic beziergons (i.e. closed loops made of quadratic Bézier curves). Before a new droplet can be merged with the previously painted areas, the points of intersection between each curve in the new droplet and the existing curves need to be calculated. See [Weekly Report \#1](Weekly%20Report%201.md) for details about how this is to be done. Since I'm going to use an algebraic approach rather than iterative, the points of intersection between any two curves can most likely be found in constant time.

### 2. Merging quadratic beziergons with each other
Once the points of intersection between each curve in the new droplet and each existing curve on the canvas have been calculated, both splines are merged into one and the redundant parts of the new spline are removed. Since the painted area can have all kinds of weird concave shapes, and it might even holes in it, this is the part where the problem becomes algorithmically interesting. Unfortunately, I couldn't find any existing algorithms for this purpose, but I do have a pretty solid idea of my own.

The time complexity of this might be something like $O(nm)$, where $m$ is the number of curves in the new droplet and $n$ is the number of curves already on the canvas. However, in any practical application of the algorithm, using 3-5 curves for each new droplet should be sufficient, which effectively brings the complexity down to $O(n)$. This may be reduced further by using a quadtree for the existing curves, but that would be redundant when the algorithm is applied to a 3D game since the game's collision planes would serve the same purpose.

### 3. Converting the painted areas defined by Bézier curves into triangles (not included in this demo)
The edges of the painted area can be rendered as triangles with a quadratic Bézier curve shaped texture on them. Each triangle at the edge of the beziergon will be defined by the control points of the corresponsing curve. There needs to be two different textures, one for a convex edge and one for a concave edge. The area enclosed by the edge triangles is a polygon that may contain holes. This polygon needs to be triangulated, but the specific algorithm for this will be decided later.

## Course Details
Programme: TKT</br>
Project language: English</br>
Programming languages: This project will use Python, but I can also peer review projects that use C, C++, C# or Java, in both English and Finnish.</br>
