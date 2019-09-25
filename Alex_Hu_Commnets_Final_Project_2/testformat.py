'''
a = '{:<8}'.format('10')
print(a)

lel = a + "lel"
print(lel)

b = int(a)
print(b)

c = b + 10
print(c)

clel = str(c)
print(clel)

d = '{:<8}'.format(clel)
print(d)

e = bytearray(a, 'ascii', 'strict')
print(e)

f = bytearray(d, 'ascii', 'strict')
print(f)

g = e + f
print(g)
'''

testarr = [0,1,2,3,4,5,6,7,8,9,10]
print testarr[4:8]
