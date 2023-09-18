# def test_decorator():
#     print('test decorator is running')

# def decor(func):
#     def wrapper(*args, **kwargs):
#         print('args - ',args)
#         print('kwargs - ',kwargs)
#         print(kwargs['data_1'])
#         # return func(*args, **kwargs)
#         return test_decorator()
#     return wrapper

# @decor
# def a(*a, **b):
#     print("In a")
#     print(a)
#     print(b)

# a('test', 'test_2', data_1=1, data_2 = 2)


import PIL
from PIL import Image

test_image = Image.open('myfiles/test.png')
print(test_image)
print(test_image.filename.replace('test', 'anurag'))

# print(test_image)

