from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
paths=['assets/working.png','assets/ready-confirmed.png','assets/error-retry.png','.pixl/assets/queue.ready/artifacts/80d2b823cf1ad6f255987aebc990c184d4be0600b04c965258dfaa54a4f72d92.png']
canvas=Image.new('RGB',(500,180),'#172336'); draw=ImageDraw.Draw(canvas)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA'); x=10; y=8+i*42
 draw.text((230,y),Path(p).name[:22],fill='white')
 bg=Image.new('RGBA',im.size,'#172336'); bg.alpha_composite(im)
 canvas.paste(bg.convert('RGB'),(x,y));canvas.paste(bg.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).convert('RGB'),(x+70,y))
canvas.save('work/focused-successor/specialist-native-3x.png')
canvas.convert('L').convert('RGB').save('work/focused-successor/specialist-grayscale.png')
