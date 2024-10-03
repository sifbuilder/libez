
# Libez: Beziers for Lips Conforming

## Features

- Draws parametric Bézier curves to model realistic human lip shapes
- Interactive user interface with adjustable trackbars for real-time control
- Visualizes upper and lower lip shapes dynamically, with the ability to customize various parameters like lip width, curvature, and fullness
- Uses heptatic Bézier curves for detailed lip modeling, allowing fine control over the lip shape

## Requirements

Before running the project, ensure the following dependencies are installed:

```bash
pip install numpy opencv-python
```

## Usage

1. Clone or download the project to your local machine.
2. Navigate to the `libez` directory.
3. Run the Python script: `python libez.py`
4. A window titled `Lip Model and Controls` will open with trackbars to adjust various parameters:
   - **lipWidth**: Adjusts the total width of the lips.
   - **lipAmplitude**: Controls the overall vertical scaling of the lips.
   - **px0, py0**: Defines the central position of the lips.
   - **upperCornerSpread, lowerCornerSpread**: Adjusts the horizontal spread of the lip corners.
   - **upperBowCurve, lowerLipFullness**: Modifies the curvature and fullness of the upper and lower lips.
   - **upperLipLift**: Raises the outer edges of the upper lip.
   - **upperLipCurve**: Controls the curvature of the upper lip vermilion border.
   - **lowerLipDrop, lowerLipProtrusion**: Adjusts the downward curve and protrusion of the lower lip.
5. Watch the lip curves update in real-time as you adjust the parameters using the trackbars.

## Functionality Overview

- **Parametric Lip Modeling**:
  The app offers a parametric model for drawing human lips using Bézier curves. Multiple control points are defined, allowing for detailed lip shapes and expressions.

- **Interactive Real-Time Adjustments**:
  The interface includes multiple trackbars that enable real-time manipulation of lip width, curvature, and fullness. The visual feedback is immediate, allowing you to explore different lip shapes easily.

- **Heptatic Bézier Curves**:
  The tool employs heptatic Bézier curves (seven control points) for the detailed and realistic modeling of upper and lower lips, mimicking the natural curvature and smoothness of lips.

## License

Libez is open-source software licensed under the MIT License.
