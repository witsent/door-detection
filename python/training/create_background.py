#!/bin/env python3

import os

output = open('background.idx', 'w')
for file in os.listdir('../dataset/bad'):
	output.write('../dataset/bad/' + file + '\n')
output.close()
