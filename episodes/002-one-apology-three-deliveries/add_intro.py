"""Add the Episode 1 series-cover layout before the complete Episode 2 story."""
from pathlib import Path
import json, subprocess, re
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parent; B=R/'build/intro'; B.mkdir(parents=True,exist_ok=True)
O=R/'deliverables'; FF='/opt/homebrew/bin/ffmpeg'; FP='/opt/homebrew/bin/ffprobe'
def run(args): subprocess.run([str(x) for x in args],check=True)
def font(size,bold=False):
    return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',size)
im=Image.new('RGB',(1080,1920),(14,17,24)); d=ImageDraw.Draw(im)
cream=(244,235,211); yellow=(246,196,65)
d.text((540,105),'SOFTWARE IN DISGUISE',font=font(56,True),fill=yellow,anchor='mm')
d.rounded_rectangle((395,165,685,225),14,fill=cream)
d.text((540,195),'EPISODE 02',font=font(28,True),fill=(14,17,24),anchor='mm')
d.rectangle((92,277,988,1173),fill=cream)
d.text((540,1310),'ONE APOLOGY.',font=font(70,True),fill=cream,anchor='mm')
d.text((540,1392),'THREE DELIVERIES.',font=font(65,True),fill=yellow,anchor='mm')
d.line((220,1500,860,1500),fill=cream,width=3)
d.text((540,1570),'Everyday stories. Software revealed.',font=font(29),fill=(200,202,208),anchor='mm')
im.save(B/'layout.png')
run([FF,'-y','-loglevel','error','-i',B/'layout.png','-i',R/'assets/reaction.png','-filter_complex','[1:v]crop=iw:iw:0:100,scale=880:880[art];[0:v][art]overlay=100:285','-frames:v','1',O/'opening.png'])
sr=48000; t=np.arange(round(sr*1.4))/sr; a=np.zeros_like(t)
for at,f in ((.06,392),(.28,494),(.52,587)):
    q=np.maximum(0,t-at)
    a+=.05*np.sin(2*np.pi*f*q)*np.exp(-6*q)*(t>=at)*(1-np.exp(-85*q))
a*=np.minimum(1,(1.4-t)/.18)
sf.write(B/'cue.wav',np.column_stack((a,a)),sr)
run([FF,'-y','-loglevel','error','-loop','1','-framerate','30','-i',O/'opening.png','-i',B/'cue.wav','-t','1.4','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000',B/'intro.mp4'])
run([FF,'-y','-loglevel','error','-i',B/'intro.mp4','-i',O/'story-cut.mp4','-filter_complex','[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',O/'short.mp4'])
# Read the unshifted captions so repeat runs never accumulate the offset.
src=R/'build/episode/story-subtitles.srt'
def shift(m):
    h,mi,s,ms=map(int,m.groups()); total=((h*60+mi)*60+s)*1000+ms+1400
    return f'{total//3600000:02}:{total//60000%60:02}:{total//1000%60:02},{total%1000:03}'
(O/'subtitles.srt').write_text(re.sub(r'(\d\d):(\d\d):(\d\d),(\d\d\d)',shift,src.read_text()))
meta=json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(O/'short.mp4')]))
assert abs(float(meta['format']['duration'])-35.4)<.1
v=next(s for s in meta['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'])==(1080,1920,'30/1')
(O/'opening-qa.json').write_text(json.dumps({'duration':meta['format']['duration'],'intro_seconds':1.4,'story_seconds':34,'subtitle_offset_seconds':1.4,'width':1080,'height':1920,'fps':30,'reference':'Episode 1 actual video opening; matching title-card layout'},indent=2)+'\n')
print(O/'short.mp4')
