
# Weekly report \#2

**Time used:** around 30 hours

Finding the intersections of two quadratic Bézier curves by factoring a quartic polynomial turned out to be harder than I expected. Even though I systematically explored virtually all computationally viable ways in which a quartic polynomial can be factored, it's still quite unclear whether translation and scaling alone can change the quartic to a factorizable form. After spending several hours on this problem without getting any practically usable results, I decided to solve the quartic numerically instead.

I implemented an algorithm that calculates the intersections of two curves by solving a quartic polynomial using NumPy. I didn't have time to come up with good unit tests for it yet, but I made a simple GUI that lets the user edit two quadratic Bézier curves on the screen by dragging their control points with the mouse while their intersections are calculated in real time and indicated visually to the user.

![image](https://user-images.githubusercontent.com/39012306/215633405-be82c269-e05b-4c3d-9917-0c1e99ed463d.png)

Next week I'm planning to write unit tests for the `find_intersections` function and start working on the problem of merging loops made of curves together.
