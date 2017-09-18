from kaldi.matrix import *
from kaldi.cudamatrix.device import CuDevice
from kaldi.cudamatrix.matrix import CuMatrix
from kaldi.base import math as kaldi_math
from kaldi.base import Timer 

# import unittest

def aux(size_multiple):
	num_matrices = 256
	time_in_secs = 0.2
	sizes = []

	for i in range(num_matrices):
		num_rows = kaldi_math.rand_int(1, 10)
		num_rows *= num_rows
		num_rows *= size_multiple

		num_cols = kaldi_math.rand_int(1, 10)
		num_cols *= num_cols
		num_cols *= size_multiple

		# There is a typo in kaldi
		sizes.append((num_rows, num_rows))

	matrices = [CuMatrix() for _ in range(num_matrices)]

	tim = Timer()
	num_floats_processed = 0
	while tim.elapsed() < time_in_secs:
		matrix = kaldi_math.rand_int(0, num_matrices - 1)
		if matrices[matrix].NumRows() == 0:
			num_rows, num_cols = sizes[matrix]

			matrices[matrix].Resize(num_rows, num_cols, MatrixResizeType.UNDEFINED)
			num_floats_processed += num_rows * num_cols

		else:
			matrices[matrix].Resize(0, 0)

	gflops = num_floats_processed / (tim.elapsed() * 1.0e9)
	print("For CuMatrix::Reize float, for size multiple {}, speed was {} gigaflops".format(size_multiple, gflops))

def testCudaMatrixResize():
	sizes = [1, 2, 4, 8, 16, 32]
	for s in sizes:
		aux(s)

if __name__ == '__main__':
	for loop in range(2):
		CuDevice.Instantiate().SetDebugStrideMode(True)
		if loop == 0:
			CuDevice.Instantiate().SelectGpuId("no")
		else:
			CuDevice.Instantiate().SelectGpuId("yes")

		testCudaMatrixResize()

		CuDevice.Instantiate().PrintProfile()
