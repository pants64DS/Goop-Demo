# Weekly report #4

**Time used:** around 25 hours

Both the algorithm for painting an area inside a beziergon and merging it with other painted areas, and the algorithm for removing paint inside one rely on being able to determine whether two beziergons intersect, or if one is inside or outside of another. Given that I already have an algorithm for finding the intersections of two quadratic Bézier curves, determining whether the beziergons intersect is simple. However, given that the beziergons can be arbitrarily detailed and complex, determining whether one is inside or outside of another is not a trivial task.

Assuming two beziergons don't intersect, if a single point on one of them is inside/outside of the other, all other points on that beziergon are inside/outside of the other beziergon as well. Therefore, it's sufficient to determine whether a single point is inside of the other beziergon or not. This week I came up with and implemented an efficient algorithm for this purpose. It draws a vertical line through the given point and counts the number of intersections between the line and the beziergon that are not above that point. It turns out that the point is inside the beziergon if and only if the number of these intersections is odd, assuming that certain edge cases have been taken into account.

My algorithm is efficient because it only really calculates the intersection points between the line and a curve in the beziergon when the given point is inside the bounding box of the curve's control points. If the vertical line is outside of that bounding box, or if the given point is below it, there can't be any intersections that should be counted. If the bounding box is below the given point, the parity of the number of intersections can be determined by checking if the line is between the starting and ending points of the curve, and taking certain edge cases into account.

Even when the given point is inside the bounding box of a curve, possible intersection points between the line and the curve's parabola aren't filtered out if they aren't actually on the curve, i.e. if the parameter for the curve would be either below zero or not below one. Surprisingly, I was able to do this without using division, square root, or anything that causes rounding error by using a couple of formulas I derived. Only after that the y-coordinates of the remaining intersection points are calculated and compared to the y-coordinate of the given point.

I also added a new view to the demo application that allows testing this algorithm visually. It allows the user to modify a beziergon and shows whether the cursor is inside or outside of it.

![image](https://user-images.githubusercontent.com/39012306/218662092-3eb55dc6-94d0-48ab-a787-5fca1137d0f8.png)

Next week I'm planning to write unit tests for this algorithm, and use it in the merging and cutting algorithms I mentioned earlier.
