# User Guide

## Installation
After making sure that [Poetry](https://python-poetry.org/docs/#installation) and Python 3.8 or later are installed, run the command `poetry install` in the root folder of this repository to install the required dependencies. If no error occurs, you will be able to start the application by running the command `poetry run python src/main.py`.

## Usage
The demo application currently has three different views, each of which allows testing different subproblems of the project visually.

### Curve View
Curve View shows the points of intersection between four different curves. Two of them are quadratic Bézier curves, and the other two are line segments. All of their control points can be moved by dragging them with the mouse. This allows testing the intersections between any arbitrary curves, as long as their control points fit on the screen. Curve View can be entered at any time by pressing 1 on the keyboard, and its contents don't depend on any other views.

### Loop View
Loop View allows the user to modify a loop made of 6 quadratic Bézier curves. Just like in Curve View, this is done by moving their control points. The application determines whether the mouse cursor is inside the loop or not, and displays a text saying either "inside" or "outside" near the cursor. Note that if the loop intersects itself, some regions 
bounded by intersecting parts of loop are considered to be outside. Loop View also displays the sum of turning angles in the loop, which should be ±360° for non-self-intersecting loops, ignoring an error of a degree or two. Loop View can be entered at any time by pressing 2 on the keyboard, and its contents don't currently depend on any other views.

### Cell view
When Cell View is entered, a copy of the loop from Loop View is displayed on screen. A different loop made of four quadratic Bézier curves is drawn on top of it centered around the mouse cursor. The size of the second loop can be adjusted using the scroll wheel. When the left mouse button is clicked, the areas bounded by the two loops are merged together, and a new set of loops is created. The created loops bound the same areas as the two previous loops, but there shouldn't be any intersections (or self-intersections) between them. New loops can be merged with the existing ones by clicking different spots, as long as the new loop doesn't intersect with any holes. However, if the new loop covers a hole completely or is inside one, it should still work.

Cell View is only expected to work properly under the following conditions:
* The sum of turning angles in the loop created in Loop View is approximately 360°.
* The loop created in Loop View doesn't intersect itself.

Cell View can be entered from Loop View by pressing 3 on the keyboard. Any changes to the loop done in Cell View are reverted when Loop View is entered again.
