import cv2
import numpy as np
import detection
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize, downscale_local_mean

lowThreshold = 30
max_lowThreshold = 100
ratio = 3
kernel_size = 3
left = 0
right = 0

# 84, 68, 28
pictures = ['8', '9', '10', '12', '13', '14', '15', '16', '17', '18', '19']
for p in pictures:
	doors = []
	for m in range(11, 1, -2):
		for n in range(5):
			img = cv2.imread('Test/cut sides/' + p + '.jpg') # 5 84
			h = 600 / img.shape[0]
			newx, newy = int(img.shape[1] * h), int(img.shape[0] * h)
			img = cv2.resize(img, (newx, newy))
			left = 0.10 * img.shape[1]
			right = 0.90 * img.shape[1]
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			detected_edges = cv2.GaussianBlur(gray, (m, m), n)
			detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, apertureSize = kernel_size)
			l = [[], []]
			lines = cv2.HoughLines(detected_edges, 1, np.pi/180, 100)
			if (lines is not None) and len(lines):
				for line in lines:
					rho, theta = line[0]
					a = np.cos(theta)
					b = np.sin(theta)
					x0 = a * rho
					y0 = b * rho
					x1 = int(x0 + 1000 * (-b))
					y1 = int(y0 + 1000 * (a))
					x2 = int(x0 - 1000 * (-b))
					y2 = int(y0 - 1000 * (a))
					if theta > 1.0:
						l[0].append([-x1, -y1, -x2, -y2])
					else:
						l[1].append([-x1, -y1, -x2, -y2])
			doors.append(detection.doors_detection(img, l, left, right))

	doors = [d for d in doors if d != [None]]
	if doors != []:
		d_min = 0
		for k in range(len(doors)):
			if doors[k][0] < doors[d_min][0]:
				d_min = k
		cv2.line(img, (int(-doors[d_min][1][0]), int(-doors[d_min][1][1])), (int(-doors[d_min][1][2]), int(-doors[d_min][1][3])), (255, 0, 0), 2)
		cv2.line(img, (int(-doors[d_min][1][2]), int(-doors[d_min][1][3])), (int(-doors[d_min][1][6]), int(-doors[d_min][1][7])), (255, 0, 0), 2)
		cv2.line(img, (int(-doors[d_min][1][6]), int(-doors[d_min][1][7])), (int(-doors[d_min][1][4]), int(-doors[d_min][1][5])), (255, 0, 0), 2)
		cv2.line(img, (int(-doors[d_min][1][4]), int(-doors[d_min][1][5])), (int(-doors[d_min][1][0]), int(-doors[d_min][1][1])), (255, 0, 0), 2)
		#cv2.line(img, (int(left), 0), (int(left), img.shape[0]), (0, 255, 0), 2)
		#cv2.line(img, (int(right), 0), (int(right), img.shape[0]), (0, 255, 0), 2)
		cv2.imshow('Door', img)
		if cv2.waitKey(0) == 27:
			cv2.destroyAllWindows()
	else:
		print('Дверь не найдена!')