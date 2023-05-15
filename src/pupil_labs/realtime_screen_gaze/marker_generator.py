import cv2

apriltag_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)

def generate_marker(marker_id, side_pixels=8, flip_x=False, flip_y=False):
	image_data = apriltag_dict.generateImageMarker(marker_id, side_pixels, 0)

	flip_code = None
	if flip_x and not flip_y:
		flip_code = 1
	elif not flip_x and flip_y:
		flip_code = 0
	elif flip_x and flip_y:
		flip_code = -1

	if flip_code is not None:
		image_data = cv2.flip(image_data, flip_code)

	return image_data
