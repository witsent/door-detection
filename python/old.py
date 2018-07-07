def choose_lines(lines, ch_lines):
	""" Function for choosing of straight lines for getting a figure 
	
	Args:
		lines: horizontal and vertical lines list l = [h_lines = [h_l1, h_l2, ...], v_lines = [v_l1, v_l2, ...]]

	Returns:
		list with figure coordinates [xl, xr, ylt, ylb, yrt, yrb]
	"""
	figure = []
	# Choosing random 2 vertical lines
	v_line2 = 0
	v_line1 = 0
	choose = False
	while not choose:
		v_line1 = random.randint(0, len(lines[1]) - 1)
		v_line2 = v_line1
		while v_line2 == v_line1:
			v_line2 = random.randint(0, len(lines[1]) - 1)
			if v_line2 < v_line1:
				t = v_line1
				v_line1 = v_line2
				v_line2 = t
		#print(v_line1)
		#print(v_line2 - v_line1 - 1)
		#print(ch_lines)
		if not ch_lines[v_line1][v_line2 - v_line1 - 1]:
				choose = True
	print('Vertical lines:')
	print(v_line1)
	print(v_line2)
	ch_lines[v_line1][v_line2 - v_line1 - 1] = 1
	# Choosing 2 horizontal lines
	intersect_points = []
	for line in lines[0]:
		intersect_points.append([])
		intersect_points[len(intersect_points) - 1].append(get_intersect_point(line, lines[1][v_line1]))
		intersect_points[len(intersect_points) - 1].append(get_intersect_point(line, lines[1][v_line2]))
	#print('Intersection points:')
	#print(intersect_points)
	h_line1 = []
	h_line2 = []
	is_find = False
	for i in range(len(intersect_points)):
		for j in range(i + 1, len(intersect_points)):
			if (intersect_points[i][0] is not None) and (intersect_points[i][1] is not None) and (intersect_points[j][0] is not None) and (intersect_points[j][1] is not None) and ((intersect_points[i][0][1] - intersect_points[j][0][1]) * (intersect_points[i][1][1] * intersect_points[j][1][1]) >= 0) and (intersect_points[i][0][1] != intersect_points[j][0][1]) and (intersect_points[i][1][1] != intersect_points[j][1][1]):
				is_find = True
				h_line1.append(i)
				h_line2.append(j)
	if is_find:
		for i in range(len(h_line1)):
			figure.append([])
			last = len(figure) - 1
			figure[last].append(lines[1][v_line1][0])
			figure[last].append(lines[1][v_line2][0])
			figure[last].append(intersect_points[h_line1[i]][0][1])
			figure[last].append(intersect_points[h_line2[i]][0][1])
			figure[last].append(intersect_points[h_line1[i]][1][1])
			figure[last].append(intersect_points[h_line2[i]][1][1])
	else:
		figure = None
	return figure



			count = 0
			for i in vert:
				if type(i) is list:
					c = 0
					for j in i:
						if j != 0:
							c += 1
					if c == len(i):
						count += 1
					continue
				if i != 0:
					count += 1
			if count == len(vert):
				break



"""
# загрузите изображение, смените цвет на оттенки серого и уменьшите резкость
c = 0
i = 1
j = 0
while c != 32 and i < 11:
	if j == 3:
		j = 0
		i += 2
	image = cv2.imread('Test/84.jpg')
	h = 600 / image.shape[0]
	newx, newy = int(image.shape[1] * h), int(image.shape[0] * h)
	image = cv2.resize(image, (newx, newy))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (i, i), j)
	#cv2.imwrite("gray.jpg", gray)
	edged = cv2.Canny(gray, lowThreshold, lowThreshold * ratio, apertureSize = kernel_size) #cv2.Canny(gray, 10, 250)
	cv2.imshow('Door', edged)
	c = cv2.waitKey(0)
	if c == 27:
		cv2.destroyAllWindows()
	j += 1
# создайте и примените закрытие ????
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
cv2.imshow('Door', closed)
if cv2.waitKey(0) == 27:
	cv2.destroyAllWindows()
# найдите контуры в изображении и подсчитайте количество книг
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
total = 0
# цикл по контурам
for c in cnts:
    # аппроксимируем (сглаживаем) контур
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # если у контура 4 вершины, предполагаем, что это книга
    if len(approx) == 4:
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
        total += 1
print(total)
cv2.imshow("output.jpg", image)
if cv2.waitKey(0) == 27:
	cv2.destroyAllWindows()
exit()
"""
#exit()
#doors = [d for d in doors if d[0] != None]
#cv2.imshow('Door', img)
#if cv2.waitKey(0) == 32:
#	cv2.destroyAllWindows()
#if cv2.waitKey(0) == 27:
#	cv2.destroyAllWindows()






flag = 1
		l = [[], []]
		if flag:
			lines = []
			lines = cv2.HoughLines(detected_edges, 1, np.pi/180, 100)
			if len(lines):
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
		else:
			lines = cv2.HoughLinesP(detected_edges, 1, np.pi/180, 50, minLineLength, maxLineGap)