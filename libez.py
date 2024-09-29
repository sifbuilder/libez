import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL
import numpy as np
import cv2
from PIL import Image, ImageTk  # to display the frame on tkinter canvas
import numpy as np
import cv2
import math

trackbars_ready = False  # Flag to check if trackbars are ready

def tag_point(frame, point, tag):
    x, y = int(point[0]), int(point[1])
    cv2.putText(frame, tag, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)

def bezier_quadratic(t, P0, P1, P2):
    """Compute the x and y values of a quadratic Bézier curve at parameter t"""
    x = (1 - t)**2 * P0[0] + 2*(1 - t) * t * P1[0] + t**2 * P2[0]
    y = (1 - t)**2 * P0[1] + 2*(1 - t) * t * P1[1] + t**2 * P2[1]
    return x, y

def bezier_quintic(t, P):
    """Compute the x and y values of a quintic Bézier curve at parameter t"""
    x = sum(math.comb(5, i) * ((1 - t) ** (5 - i)) * (t ** i) * P[i][0] for i in range(6))
    y = sum(math.comb(5, i) * ((1 - t) ** (5 - i)) * (t ** i) * P[i][1] for i in range(6))
    return x, y


def bezier_heptatic(t, P):
    try:
        x = sum(math.comb(7, i) * ((1 - t) ** (7 - i)) * (t ** i) * P[i][0] for i in range(8))
        y = sum(math.comb(7, i) * ((1 - t) ** (7 - i)) * (t ** i) * P[i][1] for i in range(8))
        return x, y
    except:
        return 0, 0
    

def print_params():
    width = cv2.getTrackbarPos('width', 'Drawing')
    amplitude = cv2.getTrackbarPos('amplitude', 'Drawing')
    px0 = cv2.getTrackbarPos('px0', 'Drawing')
    py0 = cv2.getTrackbarPos('py0', 'Drawing')
    fc = cv2.getTrackbarPos('fc', 'Drawing') / 100
    fp = cv2.getTrackbarPos('fp', 'Drawing') / 100
    vu = cv2.getTrackbarPos('vu', 'Drawing')
    vc = cv2.getTrackbarPos('vc', 'Drawing')
    vp = cv2.getTrackbarPos('vp', 'Drawing')
    vl = cv2.getTrackbarPos('vl', 'Drawing')
    
    print(f"Parameters: width={width}, amplitude={amplitude}, px0={px0}, py0={py0}, fc={fc}, fp={fp}, vu={vu}, vc={vc}, vp={vp}, vl={vl}")


def on_change(x):
    global trackbars_ready

    if not trackbars_ready:
        return


    width = cv2.getTrackbarPos('width', 'Drawing')
    amplitude = cv2.getTrackbarPos('amplitude', 'Drawing')
    
    px0 = cv2.getTrackbarPos('px0', 'Drawing')
    py0 = cv2.getTrackbarPos('py0', 'Drawing')

    fc = cv2.getTrackbarPos('fc', 'Drawing') / 100
    fp = cv2.getTrackbarPos('fp', 'Drawing') / 100

    vu = cv2.getTrackbarPos('vu', 'Drawing')
    vc = cv2.getTrackbarPos('vc', 'Drawing')

    vp = cv2.getTrackbarPos('vp', 'Drawing')
    vl = cv2.getTrackbarPos('vl', 'Drawing')


    frame = np.zeros((800, 800, 3), dtype=np.uint8)
    frame += 255  # Set to white background

    # Draw the curves
    draw_lips(frame, px0, py0, fc, fp, width, vu, vc, vl, vp, amplitude)

    cv2.imshow('Drawing', frame)


    print_params()  # Print the current state of the parameters


def draw_lips(frame, px0=200, py0=200, fc=0.5, fp=0.8, width=100, vu=100, vc=40, vl=50, vp=50, amplitude = 1.0):

  
    #  UMR0, UMR1, UMR2, UMR3, UML3, UML2, UML1, UML0 

    UMR0 = (px0 - width,             py0)
    UMR1 = (px0 - fc * width // 2,   py0 - amplitude * 0.8)
    UMR2 = (px0 - fc * width // 3,   py0 - amplitude * 0.9)
    UMR3 = (px0 - fc * width // 6,   py0 - amplitude * 1.0)
    UML3 = (px0 + fc * width // 6,   py0 - amplitude * 1.0)
    UML2 = (px0 + fc * width // 3,   py0 - amplitude * 0.9)  
    UML1 = (px0 + fc * width // 2,   py0 - amplitude * 0.8)
    UML0 = (px0 + width,             py0)

    #  LMR0, LMR1, LMR2, LMR3, LML3, LML2, LML1, LML0 

    LMR0 = (px0 - width,             py0)
    LMR1 = (px0 - fp * width // 2,   py0 + amplitude * 0.8)
    LMR2 = (px0 - fp * width // 3,   py0 + amplitude * 0.9)
    LMR3 = (px0 - fp * width // 6,   py0 + amplitude * 1.0)
    LML3 = (px0 + fp * width // 6,   py0 + amplitude * 1.0)
    LML2 = (px0 + fp * width // 3,   py0 + amplitude * 0.9)  
    LML1 = (px0 + fp * width // 2,   py0 + amplitude * 0.8)
    LML0 = (px0 + width,             py0)


# Calculate control points for the upper lip curves with vertical adjustments
    UL0 = (LMR0[0], UMR0[1])
    UL1 = (UMR1[0], UMR1[1] - vu)  
    CL0 = (UMR2[0], UMR2[1] - int(vc // 3))
    CL1 = (UMR3[0], UMR3[1] - int(vc // 2))
    CR1 = (UML3[0], UML3[1] - int(vc // 2))
    CR0 = (UML2[0], UML2[1] - int(vc // 3))
    UR1 = (UML1[0], UML1[1] - vu)
    UR0 = (UML0[0], UML0[1])
  
    # Calculate control points for the lower lip curves with vertical adjustments
    LL0 = (LMR0[0], LMR0[1])
    LL1 = (LMR1[0], LMR1[1] + vl)
    PL0 = (LMR2[0], LMR2[1] + int(vl // 3))
    PL1 = (LMR3[0], LMR3[1] + int(vp // 2))
    PR1 = (LML3[0], LML3[1] + int(vp // 2))
    PR0 = (LML2[0], LML2[1] + int(vl // 3))
    LR1 = (LML1[0], LML1[1] + vl)
    LR0 = (LML0[0], LML0[1])



    # Compute points for curves
    t_values = np.linspace(0, 1, 50)
    upper_lip = [(int(x), int(y)) for x, y in [bezier_heptatic(t, [UL0, UL1, CL0, CL1, CR1, CR0, UR1, UR0]) for t in t_values]]
    upper_lip_np = np.array(upper_lip, dtype=np.int32).reshape((-1, 1, 2))



    lower_lip = [(int(x), int(y)) for x, y in [bezier_heptatic(t, [LL0, LL1, PL0, PL1, PR1, PR0, LR1, LR0]) for t in t_values]]
    lower_lip_np = np.array(lower_lip, dtype=np.int32).reshape((-1, 1, 2))

    midup_lip = [(int(x), int(y)) for x, y in [bezier_heptatic(t, [UMR0, UMR1, UMR2, UMR3, UML3, UML2, UML1, UML0 ]) for t in t_values]]
    midup_lip_np = np.array(midup_lip, dtype=np.int32).reshape((-1, 1, 2))

    midlow_lip = [(int(x), int(y)) for x, y in [bezier_heptatic(t, [LMR0, LMR1, LMR2, LMR3, LML3, LML2, LML1, LML0]) for t in t_values]]
    midlow_lip_np = np.array(midlow_lip, dtype=np.int32).reshape((-1, 1, 2))


    # Tagging control points
    for pt, label in zip(
        [UL0, UL1, CL0, CL1, CR1, CR0, UR1, UR0, LL0, LL1, PL0, PL1, PR1, PR0, LR1, LR0], 
        ["UL0", "UL1", "CL0", "CL1", "CR1", "CR0", "UR1", "UR0", "LL0", "LL1", "PL0", "PL1", "PR1", "PR0", "LR1", "LR0"]):
        tag_point(frame, pt, label)

    # Drawing the curve
    cv2.polylines(frame, [upper_lip_np], isClosed=False, color=(0, 0, 255), thickness=2)  # Red for upper lip
    cv2.polylines(frame, [lower_lip_np], isClosed=False, color=(0, 255, 0), thickness=2)  # Green for full lower lip
    cv2.polylines(frame, [midup_lip_np], isClosed=False, color=(0, 0, 255), thickness=2)
    cv2.polylines(frame, [midlow_lip_np], isClosed=False, color=(0, 255, 0), thickness=2)



# Create the window
cv2.namedWindow('Drawing')

# Create Trackbars
cv2.createTrackbar('width', 'Drawing', 100, 200, on_change)
cv2.createTrackbar('amplitude', 'Drawing', 0, 100, on_change)
cv2.createTrackbar('px0', 'Drawing', 200, 400, on_change)
cv2.createTrackbar('py0', 'Drawing', 200, 400, on_change)
cv2.createTrackbar('fc', 'Drawing', 50, 100, on_change)
cv2.createTrackbar('fp', 'Drawing', 80, 100, on_change)

cv2.createTrackbar('vu', 'Drawing', 100, 200, on_change)
cv2.createTrackbar('vc', 'Drawing', 40, 100, on_change)
cv2.createTrackbar('vp', 'Drawing', 40, 100, on_change)
cv2.createTrackbar('vl', 'Drawing', 50, 100, on_change)

trackbars_ready = True

# Initialize
on_change(0)

cv2.waitKey(0)
cv2.destroyAllWindows()




