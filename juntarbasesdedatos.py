import pandas as pd 
import json

a = pd.read_json('J10_6yW11_0ruido.json')
b = pd.read_json('J10_6yW11_2ruido.json')
c = pd.read_json('J10_6yW11_4ruido.json')
d = pd.read_json('J10_6yW11_6ruido.json')
e = pd.read_json('J10_6yW11_8ruido.json')
f = pd.read_json('J10_6yW12_0ruido.json')
g = pd.read_json('J10_8yW10_3ruido.json')
h = pd.read_json('J10_8yW10_5ruido.json')
i = pd.read_json('J10_8yW10_7ruido.json')
j = pd.read_json('J10_8yW10_9ruido.json')
k = pd.read_json('J10_8yW11_0ruido.json')
l = pd.read_json('J10_8yW11_2ruido.json')
m = pd.read_json('J10_8yW11_4ruido.json')
n = pd.read_json('J10_8yW11_8ruido.json')
o = pd.read_json('J10_8yW11_6ruido.json')
p = pd.read_json('J10_8yW12_0ruido.json')
"""k = pd.read_json('J1yW7_2ruido.json')
l = pd.read_json('J1yW7_3ruido.json')
m = pd.read_json('J1yW7_4ruido.json')
n = pd.read_json('J1yW7_5ruido.json')
o = pd.read_json('J1yW7_6ruido.json')
p = pd.read_json('J1yW7_7ruido.json')
q = pd.read_json('J1yW7_8ruido.json')
r = pd.read_json('J1yW7_9ruido.json')
s = pd.read_json('J1yW8_0ruido.json')
t = pd.read_json('J1yW8_1ruido.json')
u = pd.read_json('J1yW8_2ruido.json')
v = pd.read_json('J1yW8_3ruido.json')
w = pd.read_json('J1yW8_4ruido.json')
x = pd.read_json('J1yW8_5ruido.json')
y = pd.read_json('J1yW8_6ruido.json')
z = pd.read_json('J1yW8_7ruido.json')

aa = pd.read_json('J1yW8_8ruido.json')
bb = pd.read_json('J1yW8_9ruido.json')
cc = pd.read_json('J1yW9_0ruido.json')
dd = pd.read_json('J1yW9_1ruido.json')
ee = pd.read_json('J1yW9_2ruido.json')
ff = pd.read_json('J1yW9_3ruido.json')
gg = pd.read_json('J1yW9_4ruido.json')
hh = pd.read_json('J1yW9_5ruido.json')
ii = pd.read_json('J1yW9_6ruido.json')
jj = pd.read_json('J1yW9_7ruido.json')
kk = pd.read_json('J1yW9_8ruido.json')
ll = pd.read_json('J1yW9_9ruido.json')
mm = pd.read_json('J1yW10_0ruido.json')
nn = pd.read_json('J1yW10_1ruido.json')
oo = pd.read_json('J1yW10_2ruido.json')
pp = pd.read_json('J1yW10_3ruido.json')
qq = pd.read_json('J1yW10_4ruido.json')
rr = pd.read_json('J1yW10_5ruido.json')
ss = pd.read_json('J1yW10_6ruido.json')
tt = pd.read_json('J1yW10_7ruido.json')
uu = pd.read_json('J1yW10_8ruido.json')
vv = pd.read_json('J1yW10_9ruido.json')
ww = pd.read_json('J1yW11_0ruido.json')
xx = pd.read_json('J1yW11_1ruido.json')
yy = pd.read_json('J1yW11_2ruido.json')
zz = pd.read_json('J1yW11_3ruido.json')
aaa = pd.read_json('J1yW11_4ruido.json')
bbb = pd.read_json('J1yW11_5ruido.json')
ccc = pd.read_json('J1yW11_6ruido.json')
ddd = pd.read_json('J1yW11_7ruido.json')
eee = pd.read_json('J1yW11_8ruido.json')
fff = pd.read_json('J1yW11_9ruido.json')
ggg = pd.read_json('J1yW12_0ruido.json')

dataset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y ,z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy, zz, aaa, bbb, ccc, ddd, eee, fff, ggg], axis=0)
"""
dataset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p], axis=0)
#crear el Json 
def escritura_json (x):
    nombre = f"{x}.json"
    with open(nombre, 'w') as archivo: 
        json.dump(parsed, archivo)
        #print("Archivo exportado con éxito")
    return 

result = dataset.to_json(orient="records")
parsed = json.loads(result)
escritura_json("J10_8y10_6HzW10_3a12_0Hz")
