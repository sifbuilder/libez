
# **Libez: Beziers for Lips Conforming**

**Libez** is a Python-based application designed for interactive lip shape modeling using Bézier curves. This application leverages OpenCV and `tkinter` to allow users to control lip curvature through adjustable parameters.

## **Features**

- Draws Bézier curves for lip shapes.
- Interactive user interface with adjustable trackbars to control parameters like width, amplitude, and control points.
- Visualizes upper and lower lip shapes using quadratic, quintic, and heptatic Bézier curves.

## **Requirements**

Before running the project, ensure the following dependencies are installed:

\`\`\`bash
pip install numpy opencv-python Pillow
\`\`\`

## **Usage**

1. Clone or download the project to your local machine.
2. Navigate to the `libez` directory.
3. Run the Python script:

    \`\`\`bash
    python libez.py
    \`\`\`

4. A window titled `Drawing` will open, with trackbars to adjust various parameters:
   - **width**: Controls the width of the lips.
   - **amplitude**: Adjusts the curve’s height.
   - **px0, py0**: Adjusts the position of control points.
   - **fc, fp**: Fine-tune control over the curve shape.
   - **vu, vc, vp, vl**: Parameters for varying curvature and positioning of the lips.

5. Watch as the curves update in real time as you adjust the parameters.

## **Functionality Overview**

- **Bézier Curve Calculations**:
  - The app provides multiple Bézier curve models, including quadratic, quintic, and heptatic Bézier curves, to model both upper and lower lips.
  
- **Trackbars**:
  - Trackbars allow for real-time adjustment of the parameters influencing lip curvature.

## **Future Work**

The current version focuses on basic lip modeling using Bézier curves. Future versions will add:
- Additional control points for more complex curves.
- Enhanced interaction with the model through a graphical interface.

## **License**

This project is licensed under the MIT License.
