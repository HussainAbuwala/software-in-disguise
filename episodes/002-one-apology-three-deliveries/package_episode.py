from pathlib import Path
from PIL import Image, ImageDraw
from render_episode import B,O,FF,font,run,INK,CREAM,GOLD

im=Image.new('RGBA',(1080,1920)); d=ImageDraw.Draw(im)
for y in range(1180,1920):
    alpha=round(245*min(1,(y-1180)/240))
    d.line((0,y,1080,y),fill=(*INK,alpha))
d.rounded_rectangle((63,65,800,133),18,fill=(*INK,230))
d.text((90,84),'SOFTWARE IN DISGUISE  /  02',font=font(31,True),fill=CREAM)
d.text((82,1390),'ONE APOLOGY.',font=font(81,True),fill=CREAM)
d.text((78,1505),'THREE',font=font(112,True),fill=GOLD)
d.text((80,1630),'DELIVERIES.',font=font(103,True),fill=GOLD)
p=B/'cover-type.png'; im.save(p)
run([FF,'-y','-loglevel','error','-ss','0.35','-i',B/'14-payoff.mp4','-i',p,'-filter_complex','[0:v][1:v]overlay=0:0','-frames:v','1',O/'thumbnail.png'])
print(O/'thumbnail.png')
