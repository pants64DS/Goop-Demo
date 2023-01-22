# Weekly report \#1

During the first week, I mostly worked on finding the intersection points of two quadratic Bézier curves. This may not be the main focus of the project, but most other aspects of the project rely on it. By searching the Internet, I learned that this is commonly done using iterative numerical algorithms. However, in the case of quadratic Bézier curves, I believe that an algebraic solution can be more efficient when implemented well.

Since a quadratic Bézier curve is really just a part of a parabola limited by its control points, one can find the intersections of two quadratic Bézier curves by first finding the intersections of the parabolas they're part of, and then discarding any intersections outside of the specified range on either curve.

If the axes of the parabolas are parallel, finding the intersections is rather trivial; one can choose a coordinate system aligned with both parabolas, so that the equation of either parabola can be written as `y = ax^2 + bx + c` with some `a`, `b` and `c`. Subtracting the quadratic polynomials for both parabolas on the right-hand side yields another quadratic polynomial, which can be solved easily.

If the axes of the parabolas are not parallel, they can be made perpendicular by applying a linear map to their control points. Solving for the intersections of two perpendicular parabolas yields a quartic polynomial, but I discovered that translating and scaling the parabolas in a certain way ensures that the resulting quartic can be factored into two quadratic polynomials.

Next week I'm planning to start implementing this technique in code.