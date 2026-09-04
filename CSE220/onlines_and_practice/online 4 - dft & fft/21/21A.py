
import numpy as np
import bigmul

# Example usage
x = 65767879797907
y = 765454532435435345

x = str(x)
y = str(y)

#converting to digit arrays(discrete signal)
# sign_x, x_digits = bigmul.to_limbs(x, 1)
# sign_y, y_digits = bigmul.to_limbs(y, 1)

# engine = bigmul.FFTTransformer()
# limbs, N = bigmul.multiply_transform(x_digits, y_digits, engine)
# ans = bigmul.from_limbs(sign_x * sign_y, limbs, 1)

ans1, N, limbs_a, limbs_b = bigmul.multiply(x, y, "fft")
ans2, N, limbs_a, limbs_b = bigmul.multiply(x, y, "dft")
ans3, N, limbs_a, limbs_b = bigmul.multiply(x, y, "schoolbook")

print(ans1)
print(ans2)
print(ans3)

