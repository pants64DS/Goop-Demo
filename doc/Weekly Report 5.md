# Weekly report #5
**Time used:** around 28 hours

The application now supports merging loops with each other, as long as the following constraints are met:
1. Both loops must be non-self-intersecting.
2. Both loops must have the same *turning number*, i.e. either both loops are clockwise or both loops are counterclockwise.
3. Merging the loops doesn't leave any holes in the merged area (the functionality for this is partially implemented, but not quite ready yet).
4. The loops don't contain parabolas with parallel axes, unless both parabolas are part of the same loop.

Constraints 1 and 2 will be met naturally in the final version of the algorithm, and constraints 3 and 4 can be removed with a bit more work.

The loop view now shows the sum of *turning angles*:

![image](https://user-images.githubusercontent.com/39012306/220096974-4dbaad49-016d-4ae1-bb4a-9f218170b8cd.png)

When the loop view is active, pressing 3 on the keyboard changes to *cell view* where the user can move a new loop over the old one using the mouse:

![image](https://user-images.githubusercontent.com/39012306/220097420-d3138cb9-f5d8-442d-8914-cbd7d9c56348.png)

When the mouse is clicked, the new loop is merged with the old loop:

![image](https://user-images.githubusercontent.com/39012306/220097473-4f044912-ff80-4cde-9ef5-2b77a393a9bc.png)

However, if the above constraints aren't met, unpredictable things may happen. The new loop has the same turning number as the other one when the app starts, but  the user might change it manually by moving the control points.

Besides the work I did during the previous weeks, merging loops with each other required solving the following subproblems:
1. Calculating the *turning angles* and *turning numbers* of the loops
2. Clipping the start of a quadratic Bézier curve up to a certain parameter value
3. Clipping the end of a quadratic Bézier curve starting from a certain parameter value
4. Clipping both the start and the end of a quadratic Bézier curve, so that only the part of the curve that's between two parameter values remains
5. Clipping a part of a loop that's between a certain interval, and returning it as a list of connected curves
6. Given a list of separate loops and a loop that intersects with all of them, constructing a list of intersections so that each intersection knows the next intersection along a new loop, which is either the loop that bounds all previous loops, or one of the "holes" inside the bounding loop
7. Constructing the bounding loop based on the list of intersections using the loop clipping algorithm
8. Implementing algorithm 2.11. from the [implementation document](doc/Implementation.md)

The list of intersections described in subproblem 6. seems to be similar to what's elsewhere known as a *planar map* or a *topoligical map*.

Unfortunately, there was so much functionality to implement that I didn't have time to write unit tests for any of it yet. On the bright side, the main functionality of the project now works to a decent extent. I'm planning to write tests for most of the relevant algorithms, as well as making them more robust during the remaining weeks.
