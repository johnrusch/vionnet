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

def draw_trouser_front_pattern(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat):
    # Draw the garment pattern
    plt.plot([])

    # Draw the waistband line
    draw_curved_line(pointA, point11, -.2)

    # Draw the bottoms of the legs
    plt.plot([point13[0], point12[0]], [point13[1], point12[1]], 'k-', label='Trouser bottom')

    # Draw fly curve
    draw_curved_line(point6, point9, 4.5)

    # Draw the fly line
    plt.plot([pointA[0], point6[0]], [pointA[1], point6[1]], 'k-')

    # Draw the inseam and side seam of the bottoms of the legs
    plt.plot([point15[0], point13[0]], [point15[1], point13[1]], 'k-')
    plt.plot([point14[0], point12[0]], [point14[1], point12[1]], 'k-')

    # Draw the inseam
    # draw_curved_line(point9, point13, 4.5)
    # point9_control = find_control_point(point9, point13, 4.5)
    # x_curve, y_curve = bezier_curve(point9, point9_control, point13)
    # plt.plot(x_curve, y_curve, 'k-')

    # Draw the hip curve
    draw_curved_line(point11, point8, .75)
    point11_control = find_control_point(point11, point8, .75)
    x_curve, y_curve = bezier_curve(point11, point11_control, point8)
    plt.plot(x_curve, y_curve, 'k-')

    # Draw the side seam
    plt.plot([point8[0], point14[0]], [point8[1], point14[1]], 'k-')

    plt.title('Trousers Pattern')
    plt.grid(False)
    plt.axis('equal')
    # plt.legend()
    plt.show()

def draw_trouser_pattern_points(body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat):
    plt.figure(figsize=(10, 10))

    # Define the first point (Point 1)
    point0 = (0, 0)

    # Define the center reference points
    point1 = (point0[0], point0[1] - ((body_rise + 1) - waistband_depth))
    point2 = (point0[0], point1[1] - inseam)
    point3 = (point0[0], point2[1] + ((inseam / 2) + 5))
    point4 = (point0[0], point1[1] + (body_rise / 4))

    # Define the fly reference point and fly curve point
    point_fly_ref = (point0[0] - ((seat / 8) - 1), point1[1])
    point5 = point_fly_ref
    # point5 = (x2, y2)
    point_fly_curve = create_diagonal_point(point_fly_ref[0], point_fly_ref[1], 3, 45)

    # Define the remaining points
    point6 = (point_fly_ref[0], point4[1])
    point7 = (point_fly_ref[0], point0[1])
    point8 = (point6[0] + ((seat / 4) + 2), point4[1])
    point9 = (point_fly_ref[0] - ((seat / 16) + .5), point1[1])
    point10 = (point7[0] + 1, point0[1])
    point11 = (point10[0] + ((waist / 4) + 2.5), point0[1])
    point12 = (point2[0] + (trouser_bottom_width / 2), point2[1])
    point13 = (point2[0] - (trouser_bottom_width / 2), point2[1])
    point14 = (point3[0] + ((trouser_bottom_width / 2) + 1.5), point3[1])
    point15 = (point3[0] - ((trouser_bottom_width / 2) + 1.5), point3[1])
    point16 = (point5[0] + (((seat / 8) - 1) / 4), point5[1])
    point17 = (point16[0], point6[1])
    point18 = (point16[0], point0[1])
    point19 = (point16[0],((point16[1] + point18[1]) / 2))
    point20 = (point18[0] + 2, point18[1])
    point21 = point_at_distance(point19, point20, 1)
    point22 = (point9[0] - ((((seat / 16) + .5) / 2) + .5), point9[1])
    point23 = (point22[0], point22[1] - .5)
    point24 = point_at_distance_with_fixed_y(point21, point0, (waist / 4) + 4.5)
    point25 = find_point_along_line(point21, point25, ((waist / 4) + 4.5) / 2)
    point26 = (point17[0] + ((seat / 4) + 3), point17[1])
    point27 = (point12[0] + 2, point12[1])
    point28 = (point13[0] - 2, point13[1])
    point29 = (point14[0] + 2, point14[1])
    point30 = (point15[0] - 2, point15[1])

    # Define the waistband adjustment point
    pointA = find_point_along_line(point10, point6, 1)

    # Plot the points
    points = [point0, point1, point2, point3, point4, point_fly_ref, point_fly_curve, point6, point7, point8, point9, point10, point11, point12, point13, point14, point15, pointA, point5, point16, point17, point18, point19, point20, point21, point22, point23, point24]
    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords, y_coords, color='blue', label='Pattern Points')

    # Annotate points
    for i, (x, y) in enumerate(points, start=0):
        plt.text(x, y, f'{i}', fontsize=12, ha='right')


    # Draw the garment pattern
    # plt.plot([])

    # # Draw the waistband line
    # draw_curved_line(pointA, point11, -.2)

    # # Draw the bottoms of the legs
    # plt.plot([point13[0], point12[0]], [point13[1], point12[1]], 'k-', label='Trouser bottom')

    # # Draw fly curve
    # draw_curved_line(point6, point9, 4.5)

    # # Draw the fly line
    # plt.plot([pointA[0], point6[0]], [pointA[1], point6[1]], 'k-')

    # # Draw the inseam and side seam of the bottoms of the legs
    # # plt.plot([point15[0], point13[0]], [point15[1], point13[1]], 'k-')
    # plt.plot([point14[0], point12[0]], [point14[1], point12[1]], 'k-')

    # # Draw the inseam
    # draw_curved_line(point9, point13, 4.5)
    # # point9_control = find_control_point(point9, point13, 4.5)
    # # x_curve, y_curve = bezier_curve(point9, point9_control, point13)
    # # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the hip curve
    # draw_curved_line(point11, point8, .75)
    # point11_control = find_control_point(point11, point8, .75)
    # x_curve, y_curve = bezier_curve(point11, point11_control, point8)
    # plt.plot(x_curve, y_curve, 'k-')

    # # Draw the side seam
    # plt.plot([point8[0], point14[0]], [point8[1], point14[1]], 'k-')

    plt.title('Trousers Pattern')
    plt.grid(False)
    plt.axis('equal')
    # plt.legend()
    plt.show()

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
    point_fly_ref = (point0[0] - ((seat_pts / 8) - cm), point1[1])
    point_fly_curve = create_diagonal_point(point_fly_ref[0], point_fly_ref[1], 3 * cm, 45)

    # Define the remaining points
    point6 = (point_fly_ref[0], point4[1])
    point7 = (point_fly_ref[0], point0[1])
    point8 = (point6[0] + ((seat_pts / 4) + (2 * cm)), point4[1])
    point9 = (point_fly_ref[0] - ((seat_pts / 16) + (0.5 * cm)), point1[1])
    point10 = (point7[0] + cm, point0[1])
    point11 = (point10[0] + ((waist_pts / 4) + (2.5 * cm)), point0[1])
    point12 = (point2[0] + (trouser_bottom_width_pts / 2), point2[1])
    point13 = (point2[0] - (trouser_bottom_width_pts / 2), point2[1])
    point14 = (point3[0] + ((trouser_bottom_width_pts / 2) + (1.5 * cm)), point3[1])
    point15 = (point3[0] - ((trouser_bottom_width_pts / 2) + (1.5 * cm)), point3[1])

    # Define the waistband adjustment point
    pointA = find_point_along_line(point10, point6, cm)

    # Draw points
    points = [point0, point1, point2, point3, point4, point_fly_ref, point_fly_curve, point6, point7, point8, point9, point10, point11, point12, point13, point14, point15, pointA]
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
draw_trouser_pattern_points(body_rise_measurement, waist_measurement, waistband_depth, trouser_bottom_width, inseam_measurement, seat_measurement)

# Prompt user to save to PDF
# prompt_save_to_pdf(body_rise_measurement, waist_measurement, waistband_depth, trouser_bottom_width, inseam_measurement, seat_measurement)
