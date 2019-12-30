import base64

with open('resource.rcc', mode='rb') as rcc_b:
    data = rcc_b.read()
    
b4 = base64.b64encode(data)

r_data = str(b4)[1:]

new_data = 'rcc=' + r_data

with open('_qmlview_resource_.py', 'w') as o_write:
    
    o_write.write(new_data)
