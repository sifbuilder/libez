import numpy as np
import cv2
import math

doc = """
Draw a parametric model of human lips.

Parameters:
- px0, py0: Central point of the lips (200, 200 by default)

- lipWidth: Total width of the mouth (100 by default)
    Sets the overall scale of the lip model. Affects UL0, UR0, LL0, LR0.

- upperCornerSpread: Horizontal spread of upper lip corners (0.5 by default)
    Controls the horizontal position of UL1 and UR1.
    A smaller value creates a narrower upper lip, while a larger value creates a wider upper lip.

- lowerCornerSpread: Horizontal spread of lower lip corners (0.8 by default)
    Controls the horizontal position of LL1 and LR1.
    The default is larger because human lower lips are typically fuller.

- upperBowCurve: Curvature of the upper lip bow (0.5 by default)
    Affects UMR1, UMR2, UMR3, UML3, UML2, UML1.
    Controls the fullness and shape of the Cupid's bow.

- lowerLipFullness: Fullness of the lower lip (0.8 by default)
    Affects LMR1, LMR2, LMR3, LML3, LML2, LML1.
    Controls the protrusion and fullness of the lower lip's middle section.

- upperLipLift: Vertical lift of outer upper lip (100 by default)
    Affects UL1 and UR1. Controls the height of the lip at its outer edges.

- upperLipCurve: Curvature of upper lip vermilion border (40 by default)
    Affects CL0, CL1, CR1, CR0. Controls the shape of the upper lip's colored part.

- lowerLipDrop: Downward curve of lower lip edges (50 by default)
    Affects LL1, LR1, PL0, PR0. Controls how much the lower lip drops at its edges.

- lowerLipProtrusion: Central protrusion of lower lip (50 by default)
    Affects PL1 and PR1. Controls how much the center of the lower lip pushes forward.

- lipAmplitude: Overall vertical scaling of lip shape (1.0 by default)
    Allows for dynamic adjustment of lip openness, simulating speech or expressions.

- amplitude: Overall vertical scaling factor (1.0 by default)
    Allows for dynamic adjustment of lip openness, simulating speech or expressions.

Control Point Naming Convention:
U/L: Upper/Lower
L/M/R: Left/Middle/Right
C: Central (upper lip)
P: Protrusion (lower lip)

Additional Parameters:
- x_distribution: [1, 2, 3, 6, 6, 3, 2, 1]
    Creates a non-linear horizontal distribution of control points.
    Larger central values (6) concentrate points in the middle, mimicking the complex curvature of the vermillion border.

- y_factors: [0, 0.7, 0.9, 1.1, 1.1, 0.9, 0.7, 0]
    Creates the vertical curve of the lips.
    The peak at the center (1.1) forms the Cupid's bow shape of the upper lip and the fullness of the lower lip.
    The gradual decrease towards the edges simulates the thinning of the lips at the corners.

This combination of parameters allows for a wide range of lip shapes,
accommodating variations in human anatomy and different expressions.
"""


class LipModel:
    def __init__(self, px0=200, py0=200, upperCornerSpread=0.5, lowerCornerSpread=0.8, upperBowCurve=0.5, lowerLipFullness=0.8, lipWidth=100, upperLipLift=100, upperLipCurve=40, lowerLipDrop=50, lowerLipProtrusion=50, lipAmplitude=1.0):
        self.px0 = px0
        self.py0 = py0
        self.upperCornerSpread = upperCornerSpread  # Factor for UL1 and UR1
        self.lowerCornerSpread = lowerCornerSpread  # Factor for LL1 and LR1
        self.upperBowCurve = upperBowCurve  # Factor for Upper Medials (UMR1, UMR2, UMR3, UML3, UML2, UML1)
        self.lowerLipFullness = lowerLipFullness  # Factor for Lower Medials (LMR1, LMR2, LMR3, LML3, LML2, LML1)
        self.lipWidth = lipWidth
        self.upperLipLift = upperLipLift
        self.upperLipCurve = upperLipCurve
        self.lowerLipDrop = lowerLipDrop
        self.lowerLipProtrusion = lowerLipProtrusion
        self.lipAmplitude = lipAmplitude

        self.x_distribution = [1, 2, 3, 6, 6, 3, 2, 1]
        self.y_factors = [0, 0.7, 0.9, 1.1, 1.1, 0.9, 0.7, 0]

    def generate_points(self):
        upper_points = self._generate_lip_points(self.upperBowCurve, -1, True)
        lower_points = self._generate_lip_points(self.lowerLipFullness, 1, False)
        return upper_points, lower_points

    def _generate_lip_points(self, g, sign, is_upper):
        points = []
        for i, (x_div, y_factor) in enumerate(zip(self.x_distribution, self.y_factors)):
            if i == 0:
                x = self.px0 - self.lipWidth
            elif i == 7:
                x = self.px0 + self.lipWidth
            else:
                factor = g if 1 <= i <= 6 else 1.0
                if i < 4:
                    x = self.px0 - factor * self.lipWidth // x_div
                else:
                    x = self.px0 + factor * self.lipWidth // self.x_distribution[7-i]
            
            y = self.py0 + sign * self.lipAmplitude * y_factor
            points.append((int(x), int(y)))
        return points

    def get_control_points(self, upper_points, lower_points):
        UMR0, UMR1, UMR2, UMR3, UML3, UML2, UML1, UML0 = upper_points
        LMR0, LMR1, LMR2, LMR3, LML3, LML2, LML1, LML0 = lower_points

        control_points = {
            'UL0': (UMR0[0], UMR0[1]),
            'UL1': (int(self.px0 - self.upperCornerSpread * self.lipWidth // 2), UMR1[1] - self.upperLipLift),
            'CL0': (UMR2[0], UMR2[1] - int(self.upperLipCurve // 3)),
            'CL1': (UMR3[0], UMR3[1] - int(self.upperLipCurve // 2)),
            'CR1': (UML3[0], UML3[1] - int(self.upperLipCurve // 2)),
            'CR0': (UML2[0], UML2[1] - int(self.upperLipCurve // 3)),
            'UR1': (int(self.px0 + self.upperCornerSpread * self.lipWidth // 2), UML1[1] - self.upperLipLift),
            'UR0': (UML0[0], UML0[1]),
            'LL0': (LMR0[0], LMR0[1]),
            'LL1': (int(self.px0 - self.lowerCornerSpread * self.lipWidth // 2), LMR1[1] + self.lowerLipDrop),
            'PL0': (LMR2[0], LMR2[1] + int(self.lowerLipDrop // 3)),
            'PL1': (LMR3[0], LMR3[1] + int(self.lowerLipProtrusion // 2)),
            'PR1': (LML3[0], LML3[1] + int(self.lowerLipProtrusion // 2)),
            'PR0': (LML2[0], LML2[1] + int(self.lowerLipDrop // 3)),
            'LR1': (int(self.px0 + self.lowerCornerSpread * self.lipWidth // 2), LML1[1] + self.lowerLipDrop),
            'LR0': (LML0[0], LML0[1])
        }
        return control_points

class LipDrawer:
    @staticmethod
    def bezier_heptatic(t, P):
        if len(P) != 8:
            raise ValueError("P must contain 8 control points.")
        x = sum(math.comb(7, i) * ((1 - t) ** (7 - i)) * (t ** i) * P[i][0] for i in range(8))
        y = sum(math.comb(7, i) * ((1 - t) ** (7 - i)) * (t ** i) * P[i][1] for i in range(8))
        return x, y

    @staticmethod
    def compute_curve_points(control_points, num_points=50):
        t_values = np.linspace(0, 1, num_points)
        curve_points = [(int(x), int(y)) for x, y in [LipDrawer.bezier_heptatic(t, control_points) for t in t_values]]
        return np.array(curve_points, dtype=np.int32).reshape((-1, 1, 2))

    @staticmethod
    def draw_lips(frame, model):
        upper_points, lower_points = model.generate_points()
        control_points = model.get_control_points(upper_points, lower_points)

        # Compute curve points
        upper_lip = LipDrawer.compute_curve_points([control_points[k] for k in ['UL0', 'UL1', 'CL0', 'CL1', 'CR1', 'CR0', 'UR1', 'UR0']])
        lower_lip = LipDrawer.compute_curve_points([control_points[k] for k in ['LL0', 'LL1', 'PL0', 'PL1', 'PR1', 'PR0', 'LR1', 'LR0']])
        midup_lip = LipDrawer.compute_curve_points(upper_points)
        midlow_lip = LipDrawer.compute_curve_points(lower_points)

        # Draw curves
        cv2.polylines(frame, [upper_lip], isClosed=False, color=(0, 0, 255), thickness=2)
        cv2.polylines(frame, [lower_lip], isClosed=False, color=(0, 255, 0), thickness=2)
        cv2.polylines(frame, [midup_lip], isClosed=False, color=(0, 0, 255), thickness=2)
        cv2.polylines(frame, [midlow_lip], isClosed=False, color=(0, 255, 0), thickness=2)

        # Draw control points
        all_points = list(control_points.values()) + upper_points + lower_points
        amplitude_points = upper_points[1:-1] + lower_points[1:-1]
        for point in all_points:
            color = (255, 0, 0) if point in amplitude_points else (139, 69, 19)
            cv2.circle(frame, point, 3, color, -1)

        # Label control points
        for label, point in control_points.items():
            x, y = point
            cv2.putText(frame, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, cv2.LINE_AA)

        # Draw amplitude range indicators
        max_amplitude = 100
        for point, factor in zip(amplitude_points, model.y_factors[1:-1] * 2):
            x = int(point[0])
            y_min = int(model.py0 - max_amplitude * factor) if point in upper_points else int(model.py0)
            y_max = int(model.py0 + max_amplitude * factor) if point in lower_points else int(model.py0)
            cv2.line(frame, (x, y_min), (x, y_max), (200, 200, 200), 1)


class LipApp:
    def __init__(self):
        self.window_name = 'Lip Model and Controls'
        cv2.namedWindow(self.window_name)
        self.model = LipModel(px0=300)  # Set initial px0 to 300 (100 to the left)
        self.trackbars = {}
        self.create_layout()
        cv2.setMouseCallback(self.window_name, self.on_mouse)

    def create_layout(self):
        self.frame = np.ones((900, 1200, 3), dtype=np.uint8) * 240  # Light gray background
        self.drawing_area = [400, 50, 1150, 800]  # [x1, y1, x2, y2]
        cv2.rectangle(self.frame, (self.drawing_area[0], self.drawing_area[1]),
                      (self.drawing_area[2], self.drawing_area[3]), (200, 200, 200), 2)

        # Reorganized parameters with new names
        params = [
            ('lipWidth', 100, 200), ('lipAmplitude', 10, 100),
            ('upperBowCurve', 50, 100), ('lowerLipFullness', 80, 100),
            ('upperLipLift', 100, 200), ('upperCornerSpread', 33, 100),
            ('lowerLipDrop', 50, 100), ('lowerCornerSpread', 80, 100),
            ('upperLipCurve', 66, 100), ('lowerLipProtrusion', 40, 100),
            ('px0', 300, 400), ('py0', 200, 400)
        ]

        for i, (name, default, max_value) in enumerate(params):
            x = 50 if i % 2 == 0 else 220
            y = 50 + (i // 2) * 80
            self.create_trackbar(name, default, max_value, x, y)

        self.update_model_from_trackbars()
        self.update_display()

    def create_trackbar(self, name, default, max_value, x, y):
        self.trackbars[name] = {'x': x, 'y': y, 'value': default, 'max': max_value}
        self.draw_trackbar(name)

    def clear_text_area(self, x, y, width, height):
        cv2.rectangle(self.frame, (x, y), (x + width, y + height), (240, 240, 240), -1)

    def draw_trackbar(self, name):
        tb = self.trackbars[name]
        # Clear the entire trackbar area
        self.clear_text_area(tb['x'], tb['y'] - 30, 150, 50)
        
        # Draw trackbar background
        cv2.rectangle(self.frame, (tb['x'], tb['y']), (tb['x'] + 150, tb['y'] + 20), (150, 150, 150), 1)
        
        # Draw trackbar value
        position = int(tb['value'] / tb['max'] * 150)
        cv2.rectangle(self.frame, (tb['x'], tb['y']), (tb['x'] + position, tb['y'] + 20), (100, 100, 100), -1)
        
        # Draw trackbar name and value
        cv2.putText(self.frame, f"{name}: {tb['value']}", (tb['x'], tb['y'] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def redraw_all_trackbars(self):
        for name in self.trackbars:
            self.draw_trackbar(name)

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON):
            for name, tb in self.trackbars.items():
                if tb['x'] <= x <= tb['x'] + 150 and tb['y'] <= y <= tb['y'] + 20:
                    new_value = int((x - tb['x']) / 150 * tb['max'])
                    if new_value != tb['value']:
                        tb['value'] = new_value
                        self.redraw_all_trackbars()
                        self.update_model_from_trackbars()
                        self.update_display()
                    break

    def update_model_from_trackbars(self):
        self.model.lipWidth = self.trackbars['lipWidth']['value']
        self.model.lipAmplitude = self.trackbars['lipAmplitude']['value']
        self.model.px0 = self.trackbars['px0']['value']
        self.model.py0 = self.trackbars['py0']['value']
        self.model.upperCornerSpread = self.trackbars['upperCornerSpread']['value'] / 100
        self.model.lowerCornerSpread = self.trackbars['lowerCornerSpread']['value'] / 100
        self.model.upperBowCurve = self.trackbars['upperBowCurve']['value'] / 100
        self.model.lowerLipFullness = self.trackbars['lowerLipFullness']['value'] / 100
        self.model.upperLipLift = self.trackbars['upperLipLift']['value']
        self.model.upperLipCurve = self.trackbars['upperLipCurve']['value']
        self.model.lowerLipProtrusion = self.trackbars['lowerLipProtrusion']['value']
        self.model.lowerLipDrop = self.trackbars['lowerLipDrop']['value']


    def update_display(self):
        drawing = self.frame.copy()
        lip_frame = np.zeros((self.drawing_area[3] - self.drawing_area[1],
                              self.drawing_area[2] - self.drawing_area[0], 3), dtype=np.uint8)
        lip_frame += 255  # White background
        LipDrawer.draw_lips(lip_frame, self.model)
        drawing[self.drawing_area[1]:self.drawing_area[3],
                self.drawing_area[0]:self.drawing_area[2]] = lip_frame
        cv2.imshow(self.window_name, drawing)

    def run(self):
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = LipApp()
    app.run()
