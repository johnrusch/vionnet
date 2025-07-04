import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import numpy as np

def bezier_curve(p0, p1, p2, num_points=100):
    t = np.linspace(0, 1, num_points)
    curve_x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    curve_y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return curve_x, curve_y

def create_diagonal_point(x, y, distance, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    x_new = x - distance * np.cos(angle_radians)
    y_new = y + distance * np.sin(angle_radians)
    return (x_new, y_new)

def find_midpoint(p1, p2):
    """
    Finds the midpoint between two points.
    
    Parameters:
    p1 (tuple): The first point (x1, y1).
    p2 (tuple): The second point (x2, y2).
    
    Returns:
    tuple: The midpoint (x, y) between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # Calculate the midpoint
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    
    return (midpoint_x, midpoint_y)

def find_point_along_line(p1, p2, distance):
    """
    Finds a point that is a certain distance from p1 along the line connecting p1 and p2.
    
    Parameters:
    p1 (tuple): The starting point (x1, y1).
    p2 (tuple): The end point (x2, y2).
    distance (float): The distance from p1 along the line.
    
    Returns:
    tuple: The new point (x, y) that is the specified distance from p1 along the line.
    """
    # Convert points to numpy arrays
    p1 = np.array(p1)
    p2 = np.array(p2)

    # Calculate the direction vector from p1 to p2
    direction = p2 - p1

    # Normalize the direction vector
    direction_norm = direction / np.linalg.norm(direction)

    # Scale the direction vector by the desired distance
    scaled_vector = direction_norm * distance

    # Calculate the new point
    new_point = p1 + scaled_vector

    return tuple(new_point)

def find_control_point(p1, p2, offset_distance):
    # Convert points to numpy arrays
    p1 = np.array(p1)
    p2 = np.array(p2)

    # Calculate the midpoint
    midpoint = (p1 + p2) / 2

    # Calculate the direction vector from p1 to p2
    direction = p2 - p1

    # Calculate the perpendicular vector (rotate 90 degrees)
    perpendicular = np.array([-direction[1], direction[0]])

    # Normalize the perpendicular vector
    perpendicular = perpendicular / np.linalg.norm(perpendicular)

    # Offset the midpoint by the perpendicular vector
    control_point = midpoint + offset_distance * perpendicular

    return control_point

def draw_curved_line(p1, p2, offset_distance):
    # Calculate the control point
    control_point = find_control_point(p1, p2, offset_distance)

    # Calculate the Bezier curve points
    x_curve, y_curve = bezier_curve(p1, control_point, p2)

    # Plot the Bezier curve
    plt.plot(x_curve, y_curve, 'k-')

def point_at_distance(p1, p2, distance):
    """
    Finds a point that is a certain distance along the continuation of the line from p1 to p2.

    Parameters:
    p1 (tuple): The starting point (x1, y1).
    p2 (tuple): The end point (x2, y2).
    distance (float): The distance from p2 along the line.

    Returns:
    tuple: The new point (x, y) that is the specified distance from p2 along the line.
    """
    # Convert points to numpy arrays
    p1 = np.array(p1)
    p2 = np.array(p2)

    # Calculate the direction vector from p1 to p2
    direction = p2 - p1

    # Normalize the direction vector
    direction_norm = direction / np.linalg.norm(direction)

    # Scale the direction vector by the desired distance
    scaled_vector = direction_norm * distance

    # Calculate the new point
    new_point = p2 + scaled_vector

    return tuple(new_point)

def point_at_distance_with_fixed_x(reference_point, x_fixed_point, distance):
    """
    Finds a point that is a certain distance diagonally from a reference point
    but has the same x value as another point.

    Parameters:
    reference_point (tuple): The reference point (x1, y1).
    x_fixed_point (tuple): The point providing the fixed x value (x2, y2).
    distance (float): The diagonal distance from the reference point.

    Returns:
    tuple: The new point (x_fixed, y) that is the specified distance from the reference point.
    """
    x1, y1 = reference_point
    x_fixed, y2 = x_fixed_point
    
    # The distance formula for a point at a certain distance with a fixed x is:
    # distance^2 = (x_fixed - x1)^2 + (y - y1)^2
    # Solving for y:
    # (y - y1)^2 = distance^2 - (x_fixed - x1)^2
    # y - y1 = ±√(distance^2 - (x_fixed - x1)^2)
    
    # Calculate the squared distance from the reference point to the fixed x
    squared_x_distance = (x_fixed - x1) ** 2
    
    # Check if the desired distance is achievable
    if squared_x_distance > distance ** 2:
        raise ValueError("Distance is too small to reach the fixed x value.")
    
    # Calculate the y-offset (could be positive or negative)
    y_offset = (distance ** 2 - squared_x_distance) ** 0.5
    
    # Calculate the two possible y values
    y_up = y1 + y_offset  # Moving up
    y_down = y1 - y_offset  # Moving down
    
    # Return both options (typically you'll choose one based on your pattern needs)
    return [(x_fixed, y_up), (x_fixed, y_down)]

def point_at_distance_with_fixed_y(reference_point, y_fixed_point, distance):
    """
    Finds a point that is a certain distance diagonally from a reference point
    but has the same y value as another point.

    Parameters:
    reference_point (tuple): The reference point (x1, y1).
    y_fixed_point (tuple): The point providing the fixed y value (x2, y2).
    distance (float): The diagonal distance from the reference point.

    Returns:
    tuple: The new point (x, y_fixed) that is the specified distance from the reference point.
    """
    x1, y1 = reference_point
    _, y_fixed = y_fixed_point

    # Calculate the horizontal distance (dx)
    dx = distance

    # Determine the new x coordinate
    new_x = x1 + dx

    # Return the new point with the fixed y value
    return (new_x, y_fixed)


    """
    Draw a perpendicular line to the line defined by (x1, y1) and (x2, y2).

    Parameters:
    - x1, y1: Coordinates of the first point of the existing line.
    - x2, y2: Coordinates of the second point of the existing line.
    - length: Length of the perpendicular line to be drawn.
    - color: Color of the perpendicular line.
    - kwargs: Additional keyword arguments for plt.plot().

    Returns:
    - The matplotlib Line2D object representing the perpendicular line.
    """
    # Calculate the direction vector of the existing line
    dx = x2 - x1
    dy = y2 - y1
    
    # Normalize the direction vector
    length_existing = np.sqrt(dx**2 + dy**2)
    dx /= length_existing
    dy /= length_existing
    
    # Calculate the direction vector of the perpendicular line
    perp_dx = -dy
    perp_dy = dx
    
    # Calculate the midpoint of the existing line
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    # Calculate the endpoints of the perpendicular line
    perp_x1 = mid_x + perp_dx * length / 2
    perp_y1 = mid_y + perp_dy * length / 2
    perp_x2 = mid_x - perp_dx * length / 2
    perp_y2 = mid_y - perp_dy * length / 2
    
    # Plot the perpendicular line
    plt.plot([perp_x1, perp_x2], [perp_y1, perp_y2], 'k-')

def perpendicular_angle(point1, point2):
    """
    Calculate the angles (in degrees) of the lines perpendicular to the line defined by (x1, y1) and (x2, y2).

    Parameters:
    - x1, y1: Coordinates of the first point of the existing line.
    - x2, y2: Coordinates of the second point of the existing line.

    Returns:
    - A tuple containing the two possible angles (in degrees) of the perpendicular lines.
    """
    # Calculate the direction vector of the existing line
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    print(dx, dy)
    
    # Calculate the angle of the existing line
    angle = np.arctan2(dy, dx)
    print(angle)
    # Calculate the angles of the perpendicular lines (90 degrees added or subtracted)
    perp_angle1 = angle + np.pi / 2
    perp_angle2 = angle - np.pi / 2
    
    # Convert the angles from radians to degrees
    perp_angle1_degrees = np.degrees(perp_angle1)
    perp_angle2_degrees = np.degrees(perp_angle2)
    
    return perp_angle1_degrees, perp_angle2_degrees

def draw_trouser_front_pattern(points: dict, show_plot=True):
    # Draw the garment pattern
    plt.plot([])

    # Draw the waistband line
    print(points)
    draw_curved_line(points["A"], points["11"], -.2)

    # Draw the bottoms of the legs
    plt.plot([points["13"][0], points["12"][0]], [points["13"][1], points["12"][1]], 'k-', label='Trouser bottom')

    # Draw fly curve
    draw_curved_line(points["6"], points["9"], 4.5)

    # Draw the fly line
    plt.plot([points["A"][0], points["6"][0]], [points["A"][1], points["6"][1]], 'k-')

    # Draw the inseam and side seam of the bottoms of the legs
    plt.plot([points["15"][0], points["13"][0]], [points["15"][1], points["13"][1]], 'k-')
    plt.plot([points["14"][0], points["12"][0]], [points["14"][1], points["12"][1]], 'k-')

    # Draw the inseam
    draw_curved_line(points["9"], points["13"], 4.5)
    point9_control = find_control_point(points["9"], points["13"], 4.5)
    x_curve, y_curve = bezier_curve(points["9"], point9_control, points["13"])
    plt.plot(x_curve, y_curve, 'k-')

    # Draw the hip curve
    draw_curved_line(points["11"], points["8"], .75)
    point11_control = find_control_point(points["11"], points["8"], .75)
    x_curve, y_curve = bezier_curve(points["11"], point11_control, points["8"])
    plt.plot(x_curve, y_curve, 'k-')

    # Draw the side seam
    plt.plot([points["8"][0], points["14"][0]], [points["8"][1], points["14"][1]], 'k-')

    plt.title('Trousers Pattern')
    plt.grid(False)
    plt.axis('equal')
    # plt.legend()
    plt.show()

def draw_trouser_back_pattern(points: dict, show_plot=True):
    # Draw the garment pattern
    plt.plot([])

    # Draw in back fork 23, 19, 21 to touch a point 4.5cm from 16
    points["back_fork"] = create_diagonal_point(points["16"][0], points["16"][1], 4.5, 45)
    
    # Create control points for a smooth curve from point23 to point19 passing near back_fork_point
    # First control point - between point23 and back_fork_point
    control1_x = points["23"][0] + (points["back_fork"][0] - points["23"][0]) * 0.3
    control1_y = points["23"][1] + (points["back_fork"][1] - points["23"][1]) * 0.5
    control1 = (control1_x, control1_y)
    
    # Second control point - between back_fork_point and point19
    control2_x = points["back_fork"][0] + (points["19"][0] - points["back_fork"][0]) * 0.3
    control2_y = points["back_fork"][1] - (points["back_fork"][1] - points["19"][1]) * 0.2
    control2 = (control2_x, control2_y)
    
    # Draw the first segment of the back fork curve (point23 to point19)
    x_curve1 = []
    y_curve1 = []
    t_values = np.linspace(0, 1, 50)
    for t in t_values:
        # Cubic Bezier formula
        x = (1-t)**3 * points["23"][0] + 3*(1-t)**2*t * control1[0] + 3*(1-t)*t**2 * control2[0] + t**3 * points["19"][0]
        y = (1-t)**3 * points["23"][1] + 3*(1-t)**2*t * control1[1] + 3*(1-t)*t**2 * control2[1] + t**3 * points["19"][1]
        x_curve1.append(x)
        y_curve1.append(y)
    plt.plot(x_curve1, y_curve1, 'k-', linewidth=2)
    
    # Control point for the curve from point19 to point21
    control3_x = points["19"][0] + (points["21"][0] - points["19"][0]) * 0.5
    control3_y = points["19"][1] + (points["21"][1] - points["19"][1]) * 0.3
    control3 = (control3_x, control3_y)
    
    # End control point
    control4_x = points["21"][0] - (points["21"][0] - points["19"][0]) * 0.2
    control4_y = points["21"][1]
    control4 = (control4_x, control4_y)
    
    # Draw the second segment of the back fork curve (point19 to point21)
    x_curve2 = []
    y_curve2 = []
    for t in t_values:
        # Cubic Bezier formula
        x = (1-t)**3 * points["19"][0] + 3*(1-t)**2*t * control3[0] + 3*(1-t)*t**2 * control4[0] + t**3 * points["21"][0]
        y = (1-t)**3 * points["19"][1] + 3*(1-t)**2*t * control3[1] + 3*(1-t)*t**2 * control4[1] + t**3 * points["21"][1]
        x_curve2.append(x)
        y_curve2.append(y)
    plt.plot(x_curve2, y_curve2, 'k-', linewidth=2)

    # Draw the waistband line, from 21 to 24
    plt.plot([points["21"][0], points["24"][0]], [points["21"][1], points["24"][1]], 'k-')

    # Construct a dart on the waistband line
    # Draw a line from 25 down 12cm, perpendicular to the waistband line
    angle = perpendicular_angle(points["21"], points["24"])
    print(angle)
    points["dart_point"] = create_diagonal_point(points["25"][0], points["25"][1], 12, angle[0])
    plt.plot([points["25"][0], points["dart_point"][0]], [points["25"][1], points["dart_point"][1]], 'k-')

    print("Point 25:", points["25"])
    print("Dart Point:", points["dart_point"])

    # # Draw fly curve
    # draw_curved_line(points["6"], points["9"], 4.5)

    # # Draw the fly line
    # plt.plot([points["A"][0], points["6"][0]], [points["A"][1], points["6"][1]], 'k-')

    # # Draw the inseam and side seam of the bottoms of the legs
    # plt.plot([points["15"][0], points["13"][0]], [points["15"][1], points["13"][1]], 'k-')
    # plt.plot([points["14"][0], points["12"][0]], [points["14"][1], points["12"][1]], 'k-')

    # # Draw the inseam
    # draw_curved_line(points["9"], points["13"], 4.5)
    # point9_control = find_control_point(points["9"], points["13"], 4.5)
    # x_curve, y_curve = bezier_curve(points["9"], point9_control, points["13"])
    # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the hip curve
    # draw_curved_line(points["11"], points["8"], .75)
    # point11_control = find_control_point(points["11"], points["8"], .75)
    # x_curve, y_curve = bezier_curve(points["11"], point11_control, points["8"])
    # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the side seam
    # plt.plot([points["8"][0], points["14"][0]], [points["8"][1], points["14"][1]], 'k-')

    plot_points = [points["0"], points["1"], points["2"], points["3"], points["4"], points["5"], points["6"], points["7"], points["8"], points["9"], points["10"], points["11"], points["12"], points["13"], points["14"], points["15"], points["A"], points["5"], points["16"], points["17"], points["18"], points["19"], points["20"], points["21"], points["22"], points["23"], points["24"], points["25"], points["26"], points["27"], points["28"], points["29"], points["30"], points["back_fork"], points["dart_point"]]
    x_coords, y_coords = zip(*plot_points)
    plt.scatter(x_coords, y_coords, color='blue', label='Pattern Points')

    # Annotate points
    for i, (x, y) in enumerate(plot_points, start=0):
        print()
        plt.text(x, y, f'{i}', fontsize=12, ha='right')

    plt.title('Trousers Pattern')
    plt.grid(False)
    plt.axis('equal')
    # plt.legend()
    plt.show()

def draw_trouser_pattern_points(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat, show_plot=True):
    plt.figure(figsize=(10, 10))

    # Initialize dictionary to store points
    points = {}
    # Define the first point (Point 1)
    points["0"] = (0, 0)

    # Define the center reference points
    points["1"] = (points["0"][0], points["0"][1] - ((body_rise + 1) - waistband_depth))
    points["2"] = (points["0"][0], points["1"][1] - inseam)
    points["3"] = (points["0"][0], points["2"][1] + ((inseam / 2) + 5))
    points["4"] = (points["0"][0], points["1"][1] + (body_rise / 4))

    # Define the fly reference point and fly curve point
    points["fly_ref"] = (points["0"][0] - ((seat / 8) - 1), points["1"][1])
    points["5"] = points["fly_ref"]
    # points["5"] = (x2, y2)
    points["fly_curve"] = create_diagonal_point(points["fly_ref"][0], points["fly_ref"][1], 3, 45)

    # Define the remaining points
    points["6"] = (points["fly_ref"][0], points["4"][1])
    points["7"] = (points["fly_ref"][0], points["0"][1])
    points["8"] = (points["6"][0] + ((seat / 4) + 2), points["4"][1])
    points["9"] = (points["fly_ref"][0] - ((seat / 16) + .5), points["1"][1])
    points["10"] = (points["7"][0] + 1, points["0"][1])
    points["11"] = (points["10"][0] + ((waist / 4) + 2.5), points["0"][1])
    points["12"] = (points["2"][0] + (trouser_bottom_width / 2), points["2"][1])
    points["13"] = (points["2"][0] - (trouser_bottom_width / 2), points["2"][1])
    points["14"] = (points["3"][0] + ((trouser_bottom_width / 2) + 1.5), points["3"][1])
    points["15"] = (points["3"][0] - ((trouser_bottom_width / 2) + 1.5), points["3"][1])
    points["16"] = (points["5"][0] + (((seat / 8) - 1) / 4), points["5"][1])
    points["17"] = (points["16"][0], points["6"][1])
    points["18"] = (points["16"][0], points["0"][1])
    points["19"] = (points["16"][0],((points["16"][1] + points["18"][1]) / 2))
    points["20"] = (points["18"][0] + 2, points["18"][1])
    points["21"] = point_at_distance(points["19"], points["20"], 1)
    points["22"] = (points["9"][0] - ((((seat / 16) + .5) / 2) + .5), points["9"][1])
    points["23"] = (points["22"][0], points["22"][1] - .5)
    points["24"] = point_at_distance_with_fixed_y(points["21"], points["0"], (waist / 4) + 4.5)
    points["25"] = find_point_along_line(points["21"], points["24"], ((waist / 4) + 4.5) / 2)
    points["26"] = (points["17"][0] + ((seat / 4) + 3), points["17"][1])
    points["27"] = (points["12"][0] + 2, points["12"][1])
    points["28"] = (points["13"][0] - 2, points["13"][1])
    points["29"] = (points["14"][0] + 2, points["14"][1])
    points["30"] = (points["15"][0] - 2, points["15"][1])

    # Define the waistband adjustment point
    points["A"] = find_point_along_line(points["10"], points["6"], 1)

    # Plot the points
    # points = [points["0"], points["1"], points["2"], points["3"], points["4"], points["5"], points["6"], points["7"], points["8"], points["9"], points["10"], points["11"], points["12"], points["13"], points["14"], points["15"], points["A"], points["5"], points["16"], points["17"], points["18"], points["19"], points["20"], points["21"], points["22"], points["23"], points["24"], points["25"], points["26"], points["27"], points["28"], points["29"], points["30"]]
    # x_coords, y_coords = zip(*points)
    # plt.scatter(x_coords, y_coords, color='blue', label='Pattern Points')

    # Annotate points
    # for i, (x, y) in enumerate(points, start=0):
    #     print()
    #     plt.text(x, y, f'{i}', fontsize=12, ha='right')


    # Draw the garment pattern
    # plt.plot([])

    # # Draw the waistband line
    # draw_curved_line(points["A"], point11, -.2)

    # # Draw the bottoms of the legs
    # plt.plot([points["13"][0], points["12"][0]], [points["13"][1], points["12"][1]], 'k-', label='Trouser bottom')

    # # Draw fly curve
    # draw_curved_line(points["6"], points["9"], 4.5)

    # # Draw the fly line
    # plt.plot([pointA[0], points["6"][0]], [pointA[1], points["6"][1]], 'k-')

    # # Draw the inseam and side seam of the bottoms of the legs
    # # plt.plot([points["15"][0], points["13"][0]], [points["15"][1], point13[1]], 'k-')
    # plt.plot([points["14"][0], points["12"][0]], [points["14"][1], points["12"][1]], 'k-')

    # # Draw the inseam
    # draw_curved_line(points["9"], point13, 4.5)
    # # point9_control = find_control_point(points["9"], point13, 4.5)
    # # x_curve, y_curve = bezier_curve(points["9"], point9_control, point13)
    # # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the hip curve
    # draw_curved_line(point11, points["8"], .75)
    # point11_control = find_control_point(point11, points["8"], .75)
    # x_curve, y_curve = bezier_curve(point11, point11_control, points["8"])
    # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the side seam
    # plt.plot([points["8"][0], points["14"][0]], [points["8"][1], points["14"][1]], 'k-')

    # plt.title('Trousers Pattern')
    # plt.grid(False)
    # plt.axis('equal')
    # # plt.legend()
    # plt.show()

    # Return the points in a dictionary
    return points

def save_to_pdf(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat, filename):
    # Convert measurements from cm to points (1 cm = 28.35 points)
    body_rise_pts = body_rise * cm
    waist_pts = waist * cm
    waistband_depth_pts = waistband_depth * cm
    trouser_bottom_width_pts = trouser_bottom_width * cm
    inseam_pts = inseam * cm
    seat_pts = seat * cm

    # Calculate the overall height and width of the pattern
    pattern_height = body_rise_pts + inseam_pts + (5 * cm)
    pattern_width = max(waist_pts / 2, seat_pts / 2) + (3 * cm)

    # Create a PDF canvas
    page_width, page_height = pattern_width + (2 * cm), pattern_height + (2 * cm)
    # page_width, page_height = 300 * cm, 300 * cm
    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    # Calculate the offsets to center the pattern on the canvas
    x_offset = page_width / 2
    y_offset = (page_height - pattern_height) / 2

    # Define the first point (Point 1)
    point0 = (x_offset, y_offset + pattern_height)

    # Define the center reference points
    point1 = (point0[0], point0[1] - ((body_rise_pts + cm) - waistband_depth_pts))
    point2 = (point0[0], point1[1] - inseam_pts)
    point3 = (point0[0], point2[1] + ((inseam_pts / 2) + (5 * cm)))
    point4 = (point0[0], point1[1] + (body_rise_pts / 4))

    # Define the fly reference point and fly curve point
    point5 = (point0[0] - ((seat_pts / 8) - cm), point1[1])
    point_fly_curve = create_diagonal_point(point5[0], point5[1], 3 * cm, 45)

    # Define the remaining points
    point6 = (point5[0], point4[1])
    point7 = (point5[0], point0[1])
    point8 = (point6[0] + ((seat_pts / 4) + (2 * cm)), point4[1])
    point9 = (point5[0] - ((seat_pts / 16) + (0.5 * cm)), point1[1])
    point10 = (point7[0] + cm, point0[1])
    point11 = (point10[0] + ((waist_pts / 4) + (2.5 * cm)), point0[1])
    point12 = (point2[0] + (trouser_bottom_width_pts / 2), point2[1])
    point13 = (point2[0] - (trouser_bottom_width_pts / 2), point2[1])
    point14 = (point3[0] + ((trouser_bottom_width_pts / 2) + (1.5 * cm)), point3[1])
    point15 = (point3[0] - ((trouser_bottom_width_pts / 2) + (1.5 * cm)), point3[1])
    # point16 is 1/4 of the distance between point1 and point5 to the right of point5
    point16 = find_point_along_line(point5, point1, 1/4)
    # point17 has the x value of point16 and the y value of point4
    point17 = (point16[0], point4[1])
    point18 = (point16[0], point0[1])
    # point19 is the midway point between point16 and point18
    point19 = find_midpoint(point16, point18)
    # point20 is 2cm to the right of point18
    point20 = (point18[0] + 2 * cm, point18[1])
    # point21 is 1cm away from point20 continuing in the direction of point19 to point20
    point21 = (point20[0], point20[1] + 1 * cm)
    # point22 is 1/2 the distance between point5 to point9 plus .5cm to the left of point9
    x_distance = abs(point9[0] - point5[0])  # Get the absolute x distance
    half_x_distance_plus_half_cm = (x_distance / 2) + (0.5 * cm)
    point22 = (point9[0] - half_x_distance_plus_half_cm, point9[1])  # Assuming we're moving left from point9
    # point23 is .5cm below point22 
    point23 = (point22[0], point22[1] - 0.5 * cm)
    # the back_fork_point has the x value of point5 and is 4.5cm away from point16
    back_fork_options = point_at_distance_with_fixed_x(point16, point5, 4.5 * cm)
    # Choose the upward option for back fork (first option in the returned list)
    back_fork_point = back_fork_options[0]  # This will be the point that's 4.5cm from point16 with the same x as point5
    point24 = point_at_distance_with_fixed_y(point21, point0, (waist_pts / 4) + 4.5)
    point25 = find_midpoint(point21, point24)

    # Create the dart from point25
    # First, find the perpendicular angle to the line between point21 and point24
    # We'll use the downward direction for the dart
    dart_angles = perpendicular_angle(point21, point24)
    dart_angle_downward = dart_angles[0]  # Use the first angle (typically downward)

    # Create the dart point 12cm away from point25 at the perpendicular angle
    dart_point = create_diagonal_point(point25[0], point25[1], 12 * cm, dart_angle_downward)

    # Calculate the dart width points by finding points at distances along point21-point24 line
    # Calculate the total distance between point21 and point24
    total_distance = ((point24[0] - point21[0])**2 + (point24[1] - point21[1])**2)**0.5

    # Calculate the distance from point21 to point25 (which is half of total_distance)
    dist_to_point25 = total_distance / 2

    # Find dart width points by adjusting distance from point21
    dart_left_point = find_point_along_line(point21, point24, dist_to_point25 - (1.25 * cm))
    dart_right_point = find_point_along_line(point21, point24, dist_to_point25 + (1.25 * cm))

    # point26 is 1/4 of the seat measurement plus 3cm to the right of point17
    point26 = (point17[0] + ((seat_pts / 4) + (3 * cm)), point17[1])
    # point27 is 2cm to the right of point12
    point27 = (point12[0] + (2 * cm), point12[1])
    # point28 is 2cm to the left of point13
    point28 = (point13[0] - (2 * cm), point13[1])
    # point29 is 2cm to the right of point14
    point29 = (point14[0] + (2 * cm), point14[1])
    # point30 is 2cm to the left of point15
    point30 = (point15[0] - (2 * cm), point15[1])
    
    
    # Draw the front pattern
    
    # Define the waistband adjustment point
    pointA = find_point_along_line(point10, point6, cm)

    # Draw points
    points = [point0, point1, point2, point3, point4, point5, point_fly_curve, point6, point7, point8, point9, point10, point11, point12, point13, point14, point15, pointA]
    for point in points:
        c.circle(point[0], point[1], 2, stroke=1, fill=0)

    # Draw the waistband line
    pointA_control = find_control_point(pointA, point11, -0.2 * cm)
    c.bezier(pointA[0], pointA[1], pointA_control[0], pointA_control[1], point11[0], point11[1], point11[0], point11[1])

    # Draw the bottoms of the legs
    c.line(point13[0], point13[1], point12[0], point12[1])

    # Draw the fly curve
    point6_control = find_control_point(point6, point9, 4.5 * cm)
    c.bezier(point6[0], point6[1], point6_control[0], point6_control[1], point9[0], point9[1], point9[0], point9[1])

    # Draw the fly line
    c.line(pointA[0], pointA[1], point6[0], point6[1])

    # Draw the inseam and side seam of the bottoms of the legs
    c.line(point14[0], point14[1], point12[0], point12[1])

    # Draw the inseam
    point9_control = find_control_point(point9, point13, 4.5 * cm)
    c.bezier(point9[0], point9[1], point9_control[0], point9_control[1], point13[0], point13[1], point13[0], point13[1])

    # Draw the hip curve
    point11_control = find_control_point(point11, point8, 0.75 * cm)
    c.bezier(point11[0], point11[1], point11_control[0], point11_control[1], point8[0], point8[1], point8[0], point8[1])

    # Draw the side seam
    c.line(point8[0], point8[1], point14[0], point14[1])

    # Save the PDF
    c.showPage()

    # Draw the back pattern
    # Define a reference point for the curve
    # This is a point 4.5cm away from point16 in a diagonal direction
    back_curve_ref = create_diagonal_point(point16[0], point16[1], 4.5 * cm, 45)  # 45 degrees is up and to the right
    
    # Draw back fork curve from point23 to point21, passing near back_fork_point and through point19
    # We'll use a smooth continuous bezier curve for the entire back fork
    
    # Start a new path for the back fork curve
    p = c.beginPath()
    p.moveTo(point23[0], point23[1])  # Start at point23
    
    # Create control points for a smooth curve
    # First control point - between point23 and back_fork_point
    # Position it to create a gentle curve from point23 toward back_fork_point
    control1_x = point23[0] + (back_fork_point[0] - point23[0]) * 0.3
    control1_y = point23[1] + (back_fork_point[1] - point23[1]) * 0.5
    control1 = (control1_x, control1_y)
    
    # Second control point - between back_fork_point and point19
    # Position it to create a curve that passes near back_fork_point but continues smoothly to point19
    control2_x = back_fork_point[0] + (point19[0] - back_fork_point[0]) * 0.3
    control2_y = back_fork_point[1] - (back_fork_point[1] - point19[1]) * 0.2
    control2 = (control2_x, control2_y)
    
    # Create a smooth curve from point23 to point19 passing near back_fork_point
    p.curveTo(control1[0], control1[1], control2[0], control2[1], point19[0], point19[1])
    
    # For the segment from point19 to point21, we'll use another bezier curve for smoothness
    # Calculate the control point for this segment
    # Position it to create a gentle curve from point19 to point21
    control3_x = point19[0] + (point21[0] - point19[0]) * 0.5
    control3_y = point19[1] + (point21[1] - point19[1]) * 0.3
    control3 = (control3_x, control3_y)
    
    # Continue the path with a curve from point19 to point21
    p.curveTo(control3[0], control3[1], 
              point21[0] - (point21[0] - point19[0]) * 0.2, point21[1], 
              point21[0], point21[1])
    
    # Draw the entire smooth path
    c.setLineWidth(2.0)  # Make the back fork curve slightly thicker for visibility
    c.drawPath(p)
    c.setLineWidth(1.0)  # Reset line width
    
    # Optionally, mark the control points for reference (useful for debugging)
    c.setStrokeColorRGB(0, 0.7, 0)  # Green for control points
    c.circle(control1[0], control1[1], 1, stroke=1, fill=0)
    c.circle(control2[0], control2[1], 1, stroke=1, fill=0)
    c.circle(control3[0], control3[1], 1, stroke=1, fill=0)
    c.setStrokeColorRGB(0, 0, 0)  # Reset to black
    
    # Mark all the back pattern points for reference with numbers
    c.setFont("Helvetica", 8)  # Set smaller font for point labels
    
    # Dictionary of points to mark with their names
    point_labels = {
        "16": point16,
        "17": point17,
        "18": point18,
        "19": point19,
        "20": point20,
        "21": point21,
        "22": point22,
        "23": point23,
        "24": point24,
        "25": point25,
        "26": point26,
        "27": point27,
        "28": point28,
        "29": point29,
        "30": point30,
        "REF": back_curve_ref
    }
    
    # Draw circles and labels for all points
    for label, point in point_labels.items():
        # Draw circle
        c.circle(point[0], point[1], 2, stroke=1, fill=0)
        # Draw label slightly offset from the point
        c.drawString(point[0] + 3, point[1] + 3, label)
    
    # Highlight the reference point in a different color
    c.setStrokeColorRGB(0.7, 0, 0)  # Red
    c.circle(back_curve_ref[0], back_curve_ref[1], 3, stroke=1, fill=0)
    c.setStrokeColorRGB(0, 0, 0)  # Reset to black
    
    # Draw the waistband line from point21 to point24
    c.line(point21[0], point21[1], point24[0], point24[1])

    # Construct a dart on the waistband line
    # draw a line from point25 to dart_point
    c.line(point25[0], point25[1], dart_point[0], dart_point[1])
    # draw a line from dart_point to dart_left_point
    c.line(dart_point[0], dart_point[1], dart_left_point[0], dart_left_point[1])
    # draw a line from dart_point to dart_right_point
    c.line(dart_point[0], dart_point[1], dart_right_point[0], dart_right_point[1])

    # Draw the side seam through points 24, 26, 29, and 27
    # First segment: straight line from point24 to point26
    c.line(point24[0], point24[1], point26[0], point26[1])
    
    # Second segment: curved line from point26 to point29, curving inward by 0.3cm
    # Calculate the midpoint between point26 and point29
    midpoint_x = (point26[0] + point29[0]) / 2
    midpoint_y = (point26[1] + point29[1]) / 2
    
    # Find the angle perpendicular to the line connecting point26 and point29
    # We need to move inward (typically to the left for the back pattern)
    perpendicular_angles = perpendicular_angle(point26, point29)
    # Choose the angle that points inward (typically the second angle)
    inward_angle = perpendicular_angles[1]  # This might need adjustment based on your coordinate system
    
    # Create a control point 0.3cm inward from the midpoint
    control_point = create_diagonal_point(midpoint_x, midpoint_y, 0.3 * cm, inward_angle)
    
    # Draw the curved line with the control point
    c.bezier(point26[0], point26[1],
             control_point[0], control_point[1],
             point29[0], point29[1],
             point29[0], point29[1])
    
    # Third segment: straight line from point29 to point27
    c.line(point29[0], point29[1], point27[0], point27[1])
    
    # Mark the key points for reference
    for point in [point24, point26, point29, point27]:
        c.circle(point[0], point[1], 2, stroke=1, fill=0)

    # Draw the inside leg seam
    # First segment: straight line from point28 to point30
    c.line(point28[0], point28[1], point30[0], point30[1])
    
    # Second segment: curved line from point23 to point30, curving inward by 1.2cm
    # Calculate the midpoint between point23 and point30
    midpoint_x = (point23[0] + point30[0]) / 2
    midpoint_y = (point23[1] + point30[1]) / 2
    
    # Find the angle perpendicular to the line connecting point23 and point30
    perpendicular_angles = perpendicular_angle(point23, point30)
    # Choose the angle that points inward (we need to test which one works for this case)
    # Try the first angle initially
    inward_angle = perpendicular_angles[0]  # Might need to use [1] instead depending on coordinate orientation
    
    # Create a control point 1.2cm inward from the midpoint
    control_point = create_diagonal_point(midpoint_x, midpoint_y, 1.2 * cm, inward_angle)
    
    # Draw the curved line with the control point
    c.bezier(point23[0], point23[1],
             control_point[0], control_point[1],
             point30[0], point30[1],
             point30[0], point30[1])
    
    # Mark the key points for the inside leg seam
    for point in [point23, point28, point30]:
        c.circle(point[0], point[1], 2, stroke=1, fill=0)

    # Draw the curved hem line between point28 and point27, curving down 1cm
    # Calculate the midpoint between point28 and point27
    midpoint_x = (point28[0] + point27[0]) / 2
    midpoint_y = (point28[1] + point27[1]) / 2
    
    # For a downward curve, we need to move down 1cm
    # In most coordinate systems, "down" means increasing the y-coordinate
    curve_point = (midpoint_x, midpoint_y + (1 * cm))
    
    # Draw the curved hem line using a bezier curve
    c.bezier(point28[0], point28[1],
             curve_point[0], curve_point[1],
             point27[0], point27[1],
             point27[0], point27[1])
    
    # Mark the control point if needed for debugging
    c.setStrokeColorRGB(0.7, 0.7, 0.7)  # Use a lighter color for control points
    c.circle(curve_point[0], curve_point[1], 1, stroke=1, fill=0)
    c.setStrokeColorRGB(0, 0, 0)  # Reset to black

    c.showPage()

    c.save()

def prompt_save_to_pdf(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat):
    response = input("Would you like to save the pattern to a PDF? (y/n): ")
    if response.lower() == 'y':
        filename = input("Enter the filename (without extension): ")
        if filename:
            save_to_pdf(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat, f"{filename}.pdf")
            print(f"The pattern has been saved as {filename}.pdf")

# Input your measurements (example values)
waist_measurement = 100.33  # cm
seat_measurement = 107.95  # cm
body_rise_measurement = 29.21 # cm
inseam_measurement = 86.36  # cm
trouser_bottom_width = 22.6  # cm
waistband_depth = 4  # cm

# draw_trouser_front_pattern(body_rise_measurement, waist_measurement, waistband_depth, trouser_bottom_width, inseam_measurement, seat_measurement)
trouser_points = draw_trouser_pattern_points(body_rise_measurement, waist_measurement, waistband_depth, trouser_bottom_width, inseam_measurement, seat_measurement)
draw_trouser_back_pattern(trouser_points)


# Prompt user to save to PDF
# prompt_save_to_pdf(body_rise_measurement, waist_measurement, waistband_depth, trouser_bottom_width, inseam_measurement, seat_measurement)
