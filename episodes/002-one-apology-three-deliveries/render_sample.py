#!/usr/bin/env python3
"""Eight-second limited-animation test. All art transforms use FFmpeg."""
from pathlib import Path
import json, math, shutil, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FF = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
PROBE = shutil.which('ffprobe') or '/opt/homebrew/bin/ffprobe'
BUILD = ROOT / 'build'
BUILD.mkdir(exist_ok=True)
OUT = ROOT / 'deliverables'
OUT.mkdir(exist_ok=True)

def run(args):
    subprocess.run([str(x) for x in args], check=True)

def caption(name, lines):
    # Original typography layer, not an edit of generated artwork.
    im = Image.new('RGBA', (1080, 1920))
    d = ImageDraw.Draw(im)
    regular = '/System/Library/Fonts/Supplemental/Arial.ttf'
    bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    f = ImageFont.truetype(bold, 45)
    small = ImageFont.truetype(regular, 23)
    d.rounded_rectangle((110, 1550, 940, 1735), radius=18, fill=(18, 23, 27, 225))
    d.text((525, 1582), 'THE NOTE', font=small, fill=(221, 185, 119), anchor='mm')
    for i, line in enumerate(lines):
        d.text((525, 1630+i*53), line, font=f, fill=(250, 240, 224), anchor='mm')
    im.save(BUILD / name)

def sound():
    sr=48000
    rng=np.random.default_rng(20260913)
    t=np.arange(sr*8)/sr
    s=np.zeros((len(t), 2), dtype=np.float64)
    # Quiet original apartment/corridor ambience.
    noise=rng.normal(0,1,len(t))
    soft=np.convolve(noise,np.ones(140)/140,mode='same')*.013
    s[:,0]=soft+0.0012*np.sin(2*np.pi*95*t)
    s[:,1]=soft+0.0010*np.sin(2*np.pi*98*t)
    def put(at, data, pan=0):
        a=round(at*sr); n=min(len(data),len(s)-a)
        s[a:a+n,0]+=data[:n]*(1-pan*.35)
        s[a:a+n,1]+=data[:n]*(1+pan*.35)
    # A warm two-note opening, ending before the interruption.
    for at,f in ((.1,440),(.4,554.37)):
        q=np.arange(int(sr*1.2))/sr
        put(at,.024*np.sin(2*np.pi*f*q)*np.exp(-5*q)*(1-np.exp(-60*q)))
    # Soft knock at the open doorway, from screen right.
    for at in (1.95,2.11):
        q=np.arange(int(sr*.17))/sr
        a=(.09*np.sin(2*np.pi*155*q)+.025*rng.normal(0,1,len(q)))*np.exp(-36*q)
        put(at,a,.8)
    # Paper rustle follows approach and settle, with little dry crackles.
    for at,dur,amp in ((2.22,.7,.042),(3.02,.22,.026),(5.15,.28,.025)):
        q=np.arange(int(sr*dur))/sr
        n=rng.normal(0,1,len(q))
        n=np.convolve(n,[1,-.7],mode='same')
        env=np.sin(np.pi*q/dur)**2*(.4+.6*np.sin(q*70)**2)
        put(at,amp*n*env,.7)
    # Leave the final reaction mostly silent; no laugh-track or sting.
    fade=np.minimum(1,t/.08)*np.minimum(1,(8-t)/.12)
    s*=fade[:,None]
    assert abs(s).max()<.95
    with wave.open(str(BUILD/'sound.wav'),'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((s*32767).astype('<i2').tobytes())
    return float(abs(s).max())

caption('note.png', ['“I’m learning', 'not to overdo it.”'])
peak=sound()
# Image layers are sampled at 30 fps. Only the face crop changes for expression
# and blink; the apartment, hair, hands and existing bouquet remain anchored.
cmd=[FF,'-y','-loglevel','warning','-filter_complex_threads','2']
for name in ('relief.png','reaction.png','blink.png','delivery-arm.png'):
    cmd+=['-loop','1','-framerate','30','-i',ROOT/'assets'/name]
cmd+=['-loop','1','-framerate','30','-i',BUILD/'note.png','-i',BUILD/'sound.wav']
filters=[
    '[0:v]scale=1080:1920,setsar=1,format=rgba[base]',
    '[1:v]scale=1080:1920,format=rgba,crop=260:255:330:265,fade=t=in:st=3.10:d=0.20:alpha=1[face]',
    "[base][face]overlay=330:265:enable='gte(t,3.10)'[acted]",
    '[2:v]scale=1080:1920,format=rgba,crop=260:115:330:305[eyes]',
    "[acted][eyes]overlay=330:305:enable='between(t,3.87,4.00)+between(t,6.57,6.70)'[blinked]",
    '[3:v]scale=760:-1,format=rgba[arm]',
    "[blinked][arm]overlay=x='if(lt(t,2.20),1200,if(lt(t,3.05),1200-610*(1-pow(1-(t-2.20)/0.85,3)),590+9*exp(-5*(t-3.05))*sin(14*(t-3.05))))':y='740+if(gte(t,3.05),3*sin((t-3.05)*2.0),18*(1-min(1,max(0,(t-2.20)/0.85))))'[delivery]",
    '[delivery]split=2[wide][forclose]',
    '[forclose]crop=810:1440:125:120,scale=1080:1920[close]',
    "[wide][close]overlay=0:0:enable='gte(t,5.55)'[scene]",
    "[scene][4:v]overlay=0:0:enable='between(t,0.15,1.85)+between(t,6.0,7.95)',format=yuv420p[v]"
]
cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map','5:a','-t','8','-r','30',
      '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
      '-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart',OUT/'look-test.mp4']
run(cmd)
data=json.loads(subprocess.check_output([PROBE,'-v','error','-show_streams','-show_format','-of','json',str(OUT/'look-test.mp4')]))
v=next(s for s in data['streams'] if s['codec_type']=='video')
a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1080,1920,'h264','30/1')
assert a['codec_name']=='aac' and a['sample_rate']=='48000'
assert abs(float(data['format']['duration'])-8)<.1
(OUT/'qa.json').write_text(json.dumps({'duration':data['format']['duration'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'video':v['codec_name'],'audio':a['codec_name'],'sample_rate':a['sample_rate'],'source_audio_peak':peak,'scope':'Limited animation, no voice or lip sync.'},indent=2)+'\n')
for at,label in ((.8,'warm'),(3.5,'delivery'),(6.4,'reaction')):
    run([FF,'-y','-loglevel','error','-ss',str(at),'-i',OUT/'look-test.mp4','-frames:v','1',OUT/f'{label}.jpg'])
print(OUT/'look-test.mp4')
