from PIL import Image

imageFile = Image.open("IMG_20171008_095658.jpg")
#imageFile = imageFile.convert('1')

imageFile = imageFile.convert('L')
bw = imageFile.point(lambda x: 0 if x<128 else 255, '1')
bw.save("result_bw.png")

#imageFile.save('bw.jpg')