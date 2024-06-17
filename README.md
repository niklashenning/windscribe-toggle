# Windscribe Toggle Button

Example of creating an animated PyQt three-state toggle button like the one used in the Windscribe
desktop app

![windscribe-toggle](https://github.com/niklashenning/windscribe-toggle/assets/58544929/13b839ac-5e8b-401a-9f21-6a910c3e86c7)

## Overview
The `ToggleButton` is a button that can be in 3 different states:`OFF`, `TURNING_ON`, and `ON`.
- By default, it is `OFF` and just looks like a white filled circle with an upside-down power symbol in the center.
- If the button is clicked, it changes state to `TURNING_ON`. The icon rotates by 180° with an animation,
so it's not upside-down anymore and two animated spinning half circles appear on the outside of the white circle.
- This is where some turning on functionality is executed depending on your application and once that is finished,
you set the state of the button to `ON`. This will turn the spinning half circles to a full circle in a different color
to indicate that the button is now turned on.
- If the button is clicked again, the button changes state to `OFF`. The full circle fades out and the icon rotates
back to its original position with an animation.

## Implementation
The base class of the `ToggleButton` is `QWidget`. At the top, I define the signals `clicked` and `stateChanged`
that will be emitted later when the button is clicked or its state changes.
I also define static color constants that will be used later for the color of the outer circle.
<br>
In the `__init__()` method, I start by defining attributes like the `state` that is set to `OFF` by default.
(The 3 possible states of the button are contained in an enum called `ToggleButtonState`).
<br>
Then I create multiple instances of `QTimeLine`, which will be used to create the different animations:
- **Outer circle rotation**: Frame range of `0-170` because each half circle has a span of 170°
- **Outer circle width**: Frame range of `0-40` to animate a width from 0.0 to 4.0 with a step of 0.1
- **Outer circle opacity**: Frame range of `0-255` to animate the alpha value of an RGBA color
- **Icon rotation**: Frame range of `0-180` since the icon rotates by 180°

The timelines call the `update()` method every frame change to trigger the `paintEvent()` which redraws the button.
They can be started in forward and backward mode depending on if the button is toggled on or off.
<br>Since the outer circle rotation timeline should run infinitely until the button is either turned on or off,
it's set to restart every time it finishes.
> **EXAMPLE**:<br> If the button is currently turned off and the state changes to `TURNING_ON`, the timelines are
> started in forward mode, so the icon rotation timeline would start at 0 and end at 180 with a step of 1.
> These values can then be used in the `paintEvent()` to calculate the angle to draw the icon at, which creates an animation.

As mentioned before, all the visual elements are drawn in the overridden `paintEvent()` method, where the
`QPainter` is initialized and the render hint is set to `Antialiasing` for better quality.

- The first element that is drawn is the <ins>filled white circle</ins>, the main element of the button.
For that, I simply use the `drawEllipse()` method of the painter, passing the center of the button
and a radius, in this case 35. To fill the circle, I set a `QBrush` instead of a `QPen`.

After that, the power icon is drawn onto the white circle. It's made up of a straight line and an arched line
that are drawn separately:

- The <ins>straight line</ins> is drawn between two points, the center and a second point that depends on the angle at which
the icon is to be drawn. If the button is turned off and the timeline value is 0, this is 90°, meaning the second
point is directly below the center. If the timeline value is 90 (animation half done), the second point would be
directly left of the center at an angle of 180°. The painter method used to draw the line is `drawLine()`
and a pen with `PenCapStyle.RoundCap` is used to make the line rounded at the ends.
<br>The static method `get_point_on_circle()` from the `Utils` class is used to calculate the second point based
on the center point, line length, and angle in degrees.

- The <ins>arched line</ins> is drawn with the `drawArc()` method of the painter with `PenCapStyle.FlatCap` for flat line ends.
It takes a `QRectF`, a start angle, and a span angle as parameters. The rect is simply made up of a width and height
that determine the space the arched line will take up, and x and y offsets used to center the rect on the button.
The line has a span angle of 326° and an initial angle of -73°, meaning the circle has a gap at the bottom to form
the classic power symbol. The timeline value for the icon rotation gets subtracted from the initial angle, so when the
timeline value is 180 (animation done), the angle would be -253°, meaning the circle has rotated by 180° and the gap
is now at the top.

The last step is drawing either two half circles, one full circle, or no circle, depending on the state of the button:

- The <ins>half circles</ins> are also drawn with the `drawArc()` method of the painter. A `QRectF` is once
again passed along with a start angle and a span angle. The span angle is 170° for both half circles
and the start angle is -95° for the first once and 85° for the second one. The value of the outer circle
rotation timeline (0-170) is also subtracted which creates an infinite spinning animation if the timeline is running.
<br>The width of the circle is animated by setting the width of the `QPen` to the value of the timeline for the
outer circle width divided by 10. `QTimeLine` can only handle integer values and I wanted an animation from 0.0 
to 4.0 with a step of 0.1, so using a frame range of 0-40 and then dividing by 10 is necessary.
<br>The color opacity of the circle is animated by setting the alpha value of the RGBA color to the value of the
timeline for the outer circle opacity. So if the animation starts in forward mode, the color will fade in
until it has reached full opacity and if the animation starts in backward mode, the color will fade out
from full opacity.

- The <ins>full circle</ins> is once again drawn with the `drawArc()` method of the painter, similarly to the half circles.
The only difference is, that start angle is 0° and the span angle is 360° for a full circle.

There is a `setState()` method to set the state of the button, which handles starting the timelines
in the right mode to show the correct animations.
<br>
This method is also used in the overridden `mousePressEvent()` to toggle the state of the button with every left click.

## License
This software is licensed under the [MIT license](LICENSE).
