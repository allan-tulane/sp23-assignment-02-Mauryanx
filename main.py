"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time


class BinaryNumber:
    """ done """

    def __init__(self, n):
        self.decimal_val = n
        self.binary_vec = list('{0:b}'.format(n))

    def __repr__(self):
        return ('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))


## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec):
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))


def split_number(vec):
    return (binary2int(vec[:len(vec) // 2]),
            binary2int(vec[len(vec) // 2:]))


def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)


def pad(x, y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y) - len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x) - len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x, y


def subquadratic_multiply_rec(x, y):
    #Obtain xvec and yvec, the binary_vec values of x and y
    x = x.binary_vec
    y = y.binary_vec

    #Pad xvec and yvec so they are the same length by adding leading 0s if necessary
    if len(x) != len(y):
        x, y = pad(x, y)

    # Base case: If both and are then just return their product.
    if len(x) == 1 or len(y) == 1:
        return BinaryNumber(int(''.join(x), 2) * int(''.join(y), 2))

    # Otherwise, split xvec and yvec into two halves each. Call them x_left x_right y_left y_right.
    x_left, x_right = split_number(x)
    y_left, y_right = split_number(y)
    #Now you can apply the formula above directly. Anywhere there is a multiply, call _quadratic_multiply
    ac = subquadratic_multiply_rec(x_left, y_left)
    bd = subquadratic_multiply_rec(x_right, y_right)
    ad_bc = subquadratic_multiply_rec(BinaryNumber(int(''.join(x_left.binary_vec), 2) + int(''.join(x_right.binary_vec), 2)),
                                    BinaryNumber(int(''.join(y_left.binary_vec), 2) + int(''.join(y_right.binary_vec), 2)))
    ad_bc = BinaryNumber(
        int(''.join(ad_bc.binary_vec), 2) - int(''.join(ac.binary_vec), 2) - int(''.join(bd.binary_vec), 2))
    #Use bit_shift to do the and multiplications.
    #Finally, you have to do three sums to get the final answer.
    #multiply by 2^n/2
    pow_val=pow(2,len(x)//2)
    return BinaryNumber(pow_val*(bit_shift(ac, len(x)//2).decimal_val) + (bit_shift(ad_bc, len(x) // 2).decimal_val) + bd.decimal_val)


def subquadratic_multiply(x, y):
    return subquadratic_multiply_rec(x,y).decimal_val


## Feel free to add your own tests here.
def test_multiply():
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)) == 2 * 2
    assert subquadratic_multiply(BinaryNumber(6), BinaryNumber(6)) == 36
    assert subquadratic_multiply(BinaryNumber(8), BinaryNumber(15)) == 120





def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    subquadratic_multiply(x, y)
    return (time.time() - start) * 1000

print(time_multiply(BinaryNumber(5), BinaryNumber(5), subquadratic_multiply_rec))
print(time_multiply(BinaryNumber(50), BinaryNumber(50), subquadratic_multiply_rec))
print(time_multiply(BinaryNumber(500), BinaryNumber(500), subquadratic_multiply_rec))
print(time_multiply(BinaryNumber(5000), BinaryNumber(5000), subquadratic_multiply_rec))

