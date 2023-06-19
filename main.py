import numpy as np
import sys


#splitting into quadrants
def split(matrix):
  row, col = matrix.shape
  row2, col2 = row // 2, col // 2
  return matrix[:row2, :col2], matrix[:row2, col2:], matrix[
    row2:, :col2], matrix[row2:, col2:]


#main calcs, returns C the product of matrices- signature per instructions
def StrassenMultiply(A, B):
  if len(A) == 1:
    return A * B

  A11, A12, A21, A22 = split(A)
  B11, B12, B21, B22 = split(B)

  P1 = StrassenMultiply(A11 + A22, B11 + B22)
  P2 = StrassenMultiply(A21 + A22, B11)
  P3 = StrassenMultiply(A11, B12 - B22)
  P4 = StrassenMultiply(A22, B21 - B11)
  P5 = StrassenMultiply(A11 + A12, B22)
  P6 = StrassenMultiply(A21 - A11, B11 + B12)
  P7 = StrassenMultiply(A12 - A22, B21 + B22)

  C11 = P1 + P4 - P5 + P7
  C12 = P3 + P5
  C21 = P2 + P4
  C22 = P1 + P3 - P2 + P6

  C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

  return C


#padding to ensure that n is not assumed as power of 2
def nextPowerOfTwo(n):
  return int(2**np.ceil(np.log2(n)))


#this creates the padded matrices A' and B'
def padMatrix(matrix, n):
  matrix = np.pad(matrix, [(0, n - matrix.shape[0]), (0, n - matrix.shape[1])],
                  mode='constant')
  return matrix


#getting an INT demsion greater than or equal to 1
def getDimensionFromUser():
  while True:
    try:
      n = int(input("Enter the dimension (n x n): "))
      if n >= 1:
        return n
      else:
        print(
          "\nError! Dimension should be greater than or equal to 1, please try again."
        )
    except ValueError:
      print("\nError! Dimension must be a valid integer, please try again.")


#user inputs (this is where the float requirement is met)
def getMatrixFromUser(n):
  matrix = []
  print(
    "Enter the elements of the matrix row-wise, press enter to input each new row, and a space between each input:"
  )
  for _ in range(n):
    row = list(map(float, input().split()))

    #checking if entered row has same number of columns as the entered dimension
    if len(row) != n:
      print(
        "\nError! Number of entered elements does not match the entered dimensions."
      )
      sys.exit(1)

    matrix.append(row)
  return np.array(matrix)


def main():
  print("Welcome to Mrinisha's Strassen Multiplication Program :)\n")

  print("Please enter the dimension for the first square matrix")
  n1 = getDimensionFromUser()
  print("Please enter the first square matrix values")
  A = getMatrixFromUser(n1)

  print("\nPlease enter the dimension for the second square matrix")
  n2 = getDimensionFromUser()

  #checking that the number of columns in matrix A is equal to the number of rows in matrix B
  if n1 != n2:
    print(
      "\nError! Number of columns from first matrix must equal number of rows in the second matrix."
    )
    sys.exit(1)

  print("Please enter the second square matrix values")
  B = getMatrixFromUser(n2)

  #checking that matrices are not empty
  if A.size == 0 or B.size == 0:
    print("\nError! Either matrix must not be empty.")
    sys.exit(1)

  #padding calls for power
  n = max(n1, n2)
  n2 = nextPowerOfTwo(n)

  A = padMatrix(A, n2)
  B = padMatrix(B, n2)

  result = StrassenMultiply(A, B)

  #extrapolate the result C form padded C'
  result = result[:n, :n]

  #making sure that the result is also in float form
  print("\nThe final result is:")
  for row in result:
    print('[' + ' '.join(f'{num:.1f}' for num in row) + ']')


if __name__ == "__main__":
  main()
