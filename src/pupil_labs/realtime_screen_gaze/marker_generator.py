import cv2

apriltag_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)

def generate_marker(marker_id, side_pixels=8):
	flipped = apriltag_dict.generateImageMarker(marker_id, side_pixels, 0)
	return cv2.rotate(flipped, cv2.ROTATE_180)
