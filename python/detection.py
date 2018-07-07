#!/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
import random

def get_intersect_point(l1, l2):
	""" Function for search two direct pieces intersection point 
	
	Args:
		l1: line1 coordinates list [x0, y0, x1, y1]
		l2: line2 coordinates list [x0, y0, x1, y1]
	
	Returns:
		intersection point [x, y] or None if doesn't exist
	"""
	res = []
	t = 0
	if l1[2] == l1[0]:
		t = 0.0000001
	else:
		t = l1[2] - l1[0]
	a1 = 1.0 * (l1[3] - l1[1]) / t 
	if l2[2] == l2[0]:
		t = 0.0000001
	else:
		t = l2[2] - l2[0]
	a2 = 1.0 * (l2[3] - l2[1]) / t
	b1 = -1.0 * l1[0] * a1 + l1[1]
	b2 = -1.0 * l2[0] * a2 + l2[1]
	if a2 != a1:
		t = (a2 - a1)
	else:
		t = 0.0000001
	res.append(round(1.0 * (b1 - b2) / t, 5))
	res.append(a1 * res[0] + b1)
	#if (res[0] > l1[0]) and (res[0] < l1[2]) and (res[0] > l2[0]) and (res[0] < l2[2]) and (res[1] > l1[1]) and (res[1] < l1[3]) and (res[1] > l2[1]) and (res[1] < l2[3]):
	if ((l1[1] - res[1]) * (l1[3] - res[1]) <= 0) and ((l2[1] - res[1]) * (l2[3] - res[1]) <= 0) and ((l1[0] - res[0]) * (l1[2] - res[0]) <= 0) and ((l2[0] - res[0]) * (l2[2] - res[0]) <= 0):
	#if (math.fabs(l1[2] - l1[0]) >= res[0]) and (math.fabs(l2[2] - l2[0]) >= res[0]) and (math.fabs(l1[3] - l1[1]) >= res[1]) and (math.fabs(l2[3] - l2[1]) >= res[1]):
		return res
	else:
		return None

def get_figure(lines, v_line1, v_line2):
	""" Function for getting figure(s) between vertical lines v_line1 and v_line2
	
	Args:
		lines: horizontal and vertical lines list l = [h_lines = [h_l1, h_l2, ...], v_lines = [v_l1, v_l2, ...]]

	Returns:
		list with figure coordinates [[xl, xr, ylt, ylb, yrt, yrb], ...]
	"""
	figure = []
	intersect_points = []
	for line in lines[0]:
		intersect_points.append([])
		intersect_points[len(intersect_points) - 1].append(get_intersect_point(line, lines[1][v_line1]))
		intersect_points[len(intersect_points) - 1].append(get_intersect_point(line, lines[1][v_line2]))
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
			figure[last].append(intersect_points[h_line1[i]][0][0])
			figure[last].append(intersect_points[h_line1[i]][0][1])
			figure[last].append(intersect_points[h_line2[i]][0][0])#(lines[1][v_line1][0])
			figure[last].append(intersect_points[h_line2[i]][0][1])#(lines[1][v_line2][0])
			figure[last].append(intersect_points[h_line1[i]][1][0])
			figure[last].append(intersect_points[h_line1[i]][1][1])
			figure[last].append(intersect_points[h_line2[i]][1][0])
			figure[last].append(intersect_points[h_line2[i]][1][1])
	else:
		figure = None
	return figure

def doors_detection(i, l, left, right):
	""" Function for doors_detection by means of vertical and horizontal lines 
	
	Args:
		i: single color image
		l: horizontal and vertical lines list l = [h_lines = [h_l1, h_l2, ...], v_lines = [v_l1, v_l2, ...]]
	
	Returns:
		number doors on image and their coordinates [k, doors = [d1=[x10, y10, x11, y11] , d2=[...], ..., dk=[...]]]
	"""
	k = 0
	doors = []
	selected_figure = []
	for i1 in range(len(l[1]) - 1):
		for i2 in range(i1 + 1, len(l[1])):
			door = get_figure(l, i1, i2)
			if door is not None:
				for d in door:
					doors.append(d)
					k += 1
	d_min = 1000
	width = i.shape[1]
	for s in doors:
		yr = (math.fabs(s[0]) + math.fabs(s[2])) / 2 # right side of figure
		yl = (math.fabs(s[4]) + math.fabs(s[6])) / 2 # left side of figure (h > 0.5 * i.shape[0]) and (h < i.shape[0]) and 
		h = math.fabs(math.fabs(s[1]) - math.fabs(s[3]))
		y = math.fabs(yr - yl)
		if (y >= 0.9 * (right - left)) and (y <= 1.1 * (right - left)) and (h / y >= 2.0) and (h / y <= 3.5):# 2.2
			d = (math.fabs(yr - right) + math.fabs(yl - left) + math.fabs(h / y - 2.2) + math.fabs(y - 0.80 * width)) / 4
			#d = (math.fabs(yr - right) + math.fabs(yl - left) + math.fabs(h / y - 2.2) + math.fabs(y - 0.8 * width)) ** (1 / 4)
			#d = math.fabs((yr / right + yl / left + h / y / 2.2 + y / 0.8 / width) / 4 - 1)
			#d = math.fabs((yr / right + yl / left + h / y / 2.2 + y / 0.8 / width) ** (1/4) - 1)
			if d < d_min:
				d_min = d
				selected_figure = s
	return [d_min, selected_figure] if selected_figure != [] else [None]

def sort_lines(l):
	""" Function for lines sort 
	
	Args:
		l: horizontal and vertical lines list l = [h_lines = [h_l1, h_l2, ...], v_lines = [v_l1, v_l2, ...]]
	
	Returns:
		sorted list of horizontal and vertical lines l = [h_lines = [h_l1 < h_l2 < h_l3 < ...], v_lines = [v_l1 < v_l2 < v_l3 < ...]]
	"""
	res = [[], []]
	for j in range(2):
		t = l[j]
		while t:
			m = 0
			for i in range(1, len(t)):
				if t[i][1 - j] < t[m][1 - j]:
					m = i
			res[j].append(t[m])
			t.pop(m)
	return res

if __name__ == "__main__":
	""" Test search intersection point
	lines = [[0, 0, 1, 1], [0, 1, 1, 0], [0, -1, 1.5, 0.5], [0, 2, 1, 1]]
	for line in lines:
		plt.plot([line[0], line[2]], [line[1], line[3]])
		for l in lines:
			if line != l:
				p = get_intersect_point(line, l)
				print(p)
				if p is not None:
					plt.scatter(p[0], p[1], color='green')
	plt.show()
	"""
	""" Test choose_lines function
	"""	
	lines = [[[0, 0, 1, 0], [0, 2, 1.5, 2], [0, 2, 2, 3], [0, 0, 2, -1], [-1, -0.5, 4, -0.5]], [[0, -0.5, 0, 2], [1, 0, 1, 2], [2, -1, 2, 3], [1.5, -3, 1.5, 3]]]
	lines = sort_lines(lines)
	vert = [[0] * (len(lines[1]) - i - 1) for i in range(len(lines[1]) - 1)]
	for l in lines:
		for line in l:
			plt.plot([line[0], line[2]], [line[1], line[3]])
	plt.show()
	for l in lines:
		for line in l:
			plt.plot([line[0], line[2]], [line[1], line[3]])
	#f = choose_lines(lines, vert)
	d = doors_detection(1, lines)
	print('Figures:')
	print(d)
	i = 1
	if d is not None:
		for f in d[1]:
			plt.plot([f[0], f[0], f[1], f[1], f[0]], [f[2], f[3], f[5], f[4], f[2]], color = 'black')
			i += 0.5
		plt.show()