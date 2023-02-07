# Weekly report #3

**Time used:** around 20 hours

I didn't find any existing algorithms that would fit very well for the problem of merging a new loop made of curves with existing loops, so I opted to design my own algorithm for this purpose. I didn't have enough time to implement it yet, but I described it with a reasonable level of detail in the [implementation document](doc/Implementation.md). The general idea is that because painted areas can contain holes, which can contain smaller painted areas, which can contain smaller holes, etc., a recursive algorithm and a recursive tree-like data structure are needed.

I also learned about a new possible method of finding the intersections of quadratic Bézier curves. In his book *Perspectives on Projective Geometry: A Guided Tour Through Real and Complex Geometry*, Jürgen Richter-Gebert presents an algebraic technique for finding the intersections of any two conic sections, including two parabolas. The technique uses projective geometry and matrix operations to turn the two conics into a single degenerate conic, which intersects both original conics at the same points where they intersect each other. This requires solving a cubic equation, rather than quartic. Currently there are more important aspects of this project to focus on, but it would be interesting to try this technique in practice.

Even though I didn't really add any new functionality this week, I wrote tests for the existing code. I also added an option to generate a coverage report. See the [testing document](doc/Testing.md) for details.

Next week I'm planning to implement (at least the central parts of) the algorithm I described in the implementation document.
