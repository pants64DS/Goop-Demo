# Weekly report #6
**Time used:** around 24 hours

My goal this week was making things more robust by covering more edge cases. I started this by splitting the `Curve` class into `ParabolicCurve` and `LinearCurve`, and adding a function called `make_curve` that chooses the appropriate curve type based on whether the control points lie on a single line or not. This removes the need to deal with degenerate parabolas in all the other functions since they're turned into line segments right after they're created. However, it implied that all functionality in the `ParabolicCurve` class had to be given a seperate implementation in the `LinearCurve` class, which took more time than I expected. That functionality inlcuded the following:

* Calculating the value of the curve (a point) at a given parameter value
* Calculating the derivative of the curve
* Counting the parity of the intersection points between the curve and a vertical line
* Finding the intersection points between the curve and a vertical line
* Finding the intersections between a linear curve and a parabolic curve
* Finding the intersections between two linear curves
* Determining the horizontal direction in which the curve goes when it starts / ends
* Calculating the turning number of a loop that includes both types of curves
* Determining the bounding box of the curve
* Clipping the start of the curve until a certain parameter value
* Clipping the end of the curve after a certain parameter value
* Clipping the start and the end of the curve leaving a part between two parameter values

These changes solved multiple edge cases. On top of them, I also added support for calculating the intersections of two parabolic curves whose axes are parallel, i.e. that open to the same or opposite direction, which also took more time than I expected. I was hoping to add tests for all these cases to make sure they work, but seems like I'll have to do that during the remaining weeks.
