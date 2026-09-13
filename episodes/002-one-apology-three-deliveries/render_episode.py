#!/usr/bin/env python3
"""Reproducible voiced, limited-animation episode. Generated art is composited by FFmpeg."""
from pathlib import Path
import json, math, shutil, subprocess, sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parent
B=R/'build'/'episode'; B.mkdir(parents=True,exist_ok=True)
O=R/'deliverables'; O.mkdir(exist_ok=True)
A=R/'assets'
FF=shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
FP=shutil.which('ffprobe') or '/opt/homebrew/bin/ffprobe'
W,H,FPS,DUR=1080,1920,30,34.0
INK=(19,27,29); CREAM=(248,237,215); GOLD=(226,182,104); TEAL=(37,92,91)
META=json.loads((R/'audio/dialogue.json').read_text())
VOICES={'grand':.42,'okay':3.77,'note':6.38,'through':9.65,'sweet':15.02,'two':20.02,'payoff':24.03,'reveal':26.8}

def run(cmd):
    subprocess.run([str(x) for x in cmd],check=True)
def font(n,bold=False):
    return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',n)
def canvas(): return Image.new('RGBA',(W,H))
def save(im,name):
    p=B/(name+'.png'); im.save(p); return p
def lines_for(text,f,maxw):
    d=ImageDraw.Draw(canvas()); out=[]; cur=''
    for word in text.split():
        test=(cur+' '+word).strip()
        if d.textlength(test,font=f)<=maxw: cur=test
        else: out.append(cur); cur=word
    if cur: out.append(cur)
    return out
def caption(text,name,speaker=None):
    im=canvas(); d=ImageDraw.Draw(im); f=font(47,True)
    lines=lines_for(text,f,830)
    y=1555; h=34+len(lines)*58+(30 if speaker else 0)
    d.rounded_rectangle((78,y,974,y+h),radius=20,fill=(*INK,232))
    if speaker:
        d.text((112,y+15),speaker,font=font(21,True),fill=GOLD)
        y+=30
    for i,line in enumerate(lines): d.text((526,y+19+i*58),line,font=f,fill=CREAM,anchor='ma')
    return save(im,name)
def series():
    im=canvas(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((66,67,744,127),14,fill=(*INK,218))
    d.text((87,84),'SOFTWARE IN DISGUISE   /   02',font=font(28,True),fill=CREAM)
    return save(im,'series')
def header(text,name):
    im=canvas(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((74,100,975,190),18,fill=(*INK,230))
    d.text((524,145),text,font=font(38,True),fill=GOLD,anchor='mm')
    return save(im,name)

def phone(mode,typed=99):
    im=canvas(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((104,183,976,1729),radius=88,fill=(7,16,20,245))
    d.rounded_rectangle((128,217,952,1698),radius=66,fill=(247,240,225))
    d.rounded_rectangle((402,234,678,272),18,fill=INK)
    d.text((174,325),'FLOWER DELIVERY',font=font(31,True),fill=TEAL)
    d.text((174,405),'A little apology.',font=font(51,True),fill=INK)
    d.rounded_rectangle((174,511,906,750),24,fill=(229,218,194))
    d.text((210,554),'Small bouquet',font=font(44,True),fill=INK)
    d.text((210,620),'Cream daisies · Kraft wrap',font=font(28),fill=(76,79,67))
    d.text((210,674),'Quantity: 1',font=font(30,True),fill=TEAL)
    d.text((182,809),'Make it grand',font=font(30),fill=INK)
    d.rounded_rectangle((795,806,887,851),23,fill=(177,179,164))
    d.ellipse((801,812,834,845),fill=CREAM)
    d.text((181,899),'YOUR NOTE',font=font(26,True),fill=TEAL)
    d.rounded_rectangle((174,947,906,1162),20,fill=(255,251,240),outline=(193,187,169),width=2)
    text="I'm learning not to overdo it."[:typed]
    for i,line in enumerate(lines_for(text,font(39),650)):
        d.text((203,983+i*57),line,font=font(39),fill=INK)
    if mode=='note':
        d.rounded_rectangle((174,1245,906,1351),22,fill=TEAL)
        d.text((540,1298),'Send one bouquet',font=font(38,True),fill=CREAM,anchor='mm')
    else:
        d.text((540,1235),'Confirmation unavailable',font=font(35,True),fill=(159,74,43),anchor='mm')
        d.text((540,1293),'We couldn’t confirm your order.',font=font(26),fill=(93,87,71),anchor='mm')
        d.rounded_rectangle((174,1360,906,1466),22,fill=TEAL if mode=='error' else (52,119,110))
        d.text((540,1413),'Retry' if mode=='error' else 'Sending…',font=font(39,True),fill=CREAM,anchor='mm')
    d.rounded_rectangle((409,1647,671,1656),5,fill=INK)
    return save(im,f'phone-{mode}-{typed}')

def notes_card():
    im=canvas(); d=ImageDraw.Draw(im)
    for i,y in enumerate((485,828,1171)):
        d.rounded_rectangle((127+i*17,y,913+i*17,y+280),20,fill=(246,231,198,250),outline=(192,164,118),width=3)
        d.ellipse((161+i*17,y+31,178+i*17,y+48),fill=(87,67,43))
        d.text((532+i*17,y+93),'“I’m learning',font=font(47,True),fill=INK,anchor='mm')
        d.text((532+i*17,y+158),'not to overdo it.”',font=font(47,True),fill=INK,anchor='mm')
    return save(im,'three-notes')

def reveal_card(stage):
    im=canvas(); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,H),fill=(*INK,135))
    d.rounded_rectangle((64,125,990,1460),32,fill=(*INK,235),outline=(93,116,105),width=2)
    d.text((526,213),'THE MISSING SAFEGUARD',font=font(31,True),fill=CREAM,anchor='mm')
    if stage:
        d.text((526,329),'IDEMPOTENCY',font=font(78,True),fill=GOLD,anchor='mm')
        d.text((526,435),'Same order. Safe to retry.',font=font(39),fill=CREAM,anchor='mm')
        for i,y in enumerate((577,715,853)):
            d.rounded_rectangle((120,y,505,y+91),15,fill=(40,68,68),outline=(116,150,136),width=2)
            d.text((313,y+44),f'TRY {i+1}  ·  ORDER 104',font=font(26,True),fill=CREAM,anchor='mm')
            d.line((505,y+46,584,y+46,584,759,633,759),fill=GOLD,width=5)
        d.polygon(((632,747),(650,759),(632,771)),fill=GOLD)
        d.rounded_rectangle((657,683,938,838),20,fill=TEAL)
        d.text((797,728),'ONE',font=font(37,True),fill=CREAM,anchor='mm')
        d.text((797,789),'BOUQUET',font=font(31,True),fill=CREAM,anchor='mm')
        d.text((526,1069),'Reuse the same order ID.',font=font(39,True),fill=CREAM,anchor='mm')
        d.text((526,1140),'Don’t create another order.',font=font(35),fill=(189,201,188),anchor='mm')
    d.text((526,1335),'SOFTWARE IN DISGUISE',font=font(36,True),fill=CREAM,anchor='mm')
    d.text((526,1398),'EPISODE 02',font=font(26,True),fill=GOLD,anchor='mm')
    return save(im,'reveal-'+str(stage))

class Shot:
    def __init__(self,name,duration,base):
        self.name=name; self.duration=duration
        self.cmd=[FF,'-y','-loglevel','error','-filter_complex_threads','2']
        self.n=0; self.filters=[]; self.cur='base'
        self.add(base)
        self.filters=['[0:v]scale=1080:1920,setsar=1,format=rgba[base]']
    def add(self,path):
        i=self.n; self.n+=1
        self.cmd+=['-loop','1','-framerate','30','-i',path]
        return i
    def layer(self,path,fx='',x='0',y='0',enable=None):
        i=self.add(path); inp=f'in{i}'; out=f'out{i}'
        self.filters.append(f'[{i}:v]'+(fx+',' if fx else '')+f'format=rgba[{inp}]')
        self.filters.append(f'[{self.cur}][{inp}]overlay=x=\'{x}\':y=\'{y}\''+(f":enable='{enable}'" if enable else '')+f'[{out}]')
        self.cur=out
        return self
    def effect(self,fx):
        out=f'effect{len(self.filters)}'; self.filters.append(f'[{self.cur}]{fx}[{out}]'); self.cur=out
        return self
    def mouth(self,asset,rect,line,at):
        vals=META[line]['rms_30fps']; threshold=max(vals)*.22
        # Two hand-drawn mouth poses, gated by speech energy on animation twos.
        intervals=[]; start=None
        for j in range(0,len(vals)+2,2):
            active=j<len(vals) and max(vals[j:j+2])>threshold and (j//2)%5!=4
            if active and start is None: start=j
            if not active and start is not None:
                intervals.append((at+start/30,at+j/30)); start=None
        expr='+'.join(f'between(t,{a:.4f},{b:.4f})' for a,b in intervals) or '0'
        x,y,w,h=rect
        self.layer(A/asset,f'scale=1080:1920,crop={w}:{h}:{x}:{y}',str(x),str(y),expr)
        return self
    def finish(self):
        dest=B/(self.name+'.mp4')
        self.filters.append(f'[{self.cur}]format=yuv420p[v]')
        run(self.cmd+['-filter_complex',';'.join(self.filters),'-map','[v]','-an','-t',str(self.duration),'-r','30','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',dest])
        print('rendered',self.name,flush=True)
        return dest

def build_shots():
    shots=[]
    def done(s): shots.append(s.finish())
    s=Shot('01-intro',3.5,A/'intro.png')
    s.layer(A/'intro-down.png','scale=1080:1920,format=rgba,fade=t=in:st=1.35:d=0.22:alpha=1',enable='gte(t,1.35)')
    s.layer(series())
    s.layer(caption("You don’t have to make everything a grand gesture.",'cap-grand','HER'),enable='between(t,.40,3.15)')
    done(s)
    s=Shot('02-sender',2.5,A/'sender.png')
    s.mouth('sender-talk.png',(433,550,178,104),'okay',.27)
    s.layer(A/'sender-blink.png','scale=1080:1920,crop=285:135:430:415','430','415','between(t,2.13,2.25)')
    s.layer(caption('Okay. One little bouquet.','cap-okay'),enable='between(t,.24,2.22)')
    done(s)
    s=Shot('03-note',2.7,A/'sender.png').effect('gblur=sigma=18')
    s.layer(phone('note',12))
    s.layer(phone('note',23),enable='gte(t,.42)')
    s.layer(phone('note'),enable='gte(t,.9)')
    done(s)
    for ix,name,start in ((1,'florist-one.png',0),):
        s=Shot('04-print1',.7,A/name)
        s.layer(header('ORDER RECEIVED','order1'),'','0','18*(1-min(t/.18,1))')
        done(s)
    s=Shot('05-through',1.7,A/'sender.png')
    s.mouth('sender-talk.png',(433,550,178,104),'through',.25)
    s.effect('crop=880:1564:100:120,scale=1080:1920')
    s.layer(caption('Did it go through?','cap-through'),enable='between(t,.22,1.60)')
    done(s)
    for name,duration,kind in (('06-retry1',.9,'retry'),('07-print2',.7,'print'),('08-retry2',.8,'retry'),('09-print3',.7,'last')):
        if kind=='retry':
            s=Shot(name,duration,A/'sender.png').effect('gblur=sigma=18')
            s.layer(phone('error')); s.layer(phone('sending'),enable='gte(t,.48)')
        else:
            s=Shot(name,duration,A/('florist-two.png' if kind=='print' else 'florist.png'))
            s.layer(header('ANOTHER ORDER RECEIVED','order-'+kind),'','0','18*(1-min(t/.18,1))')
        done(s)
    s=Shot('10-sweet',3.3,A/'relief.png')
    s.mouth('sweet-talk.png',(421,415,135,95),'sweet',.82)
    s.layer(caption('That’s actually sweet.','cap-sweet'),enable='between(t,.78,2.48)')
    done(s)
    s=Shot('11-delivery',2.3,A/'relief.png')
    s.layer(A/'reaction.png','scale=1080:1920,crop=260:255:330:265,format=rgba,fade=t=in:st=0.95:d=0.20:alpha=1','330','265','gte(t,.95)')
    s.layer(A/'blink.png','scale=1080:1920,crop=260:115:330:305','330','305','between(t,1.70,1.83)')
    s.layer(A/'delivery-arm.png','scale=760:-1',"if(lt(t,.12),1200,if(lt(t,.95),1200-610*(1-pow(1-(t-.12)/.83,3)),590+8*exp(-5*(t-.95))*sin(14*(t-.95))))","740+3*sin(t*2)")
    done(s)
    s=Shot('12-courier',2,A/'courier.png')
    s.mouth('courier-talk.png',(510,325,150,95),'two',.22)
    s.layer(caption('And these two.','cap-two'),enable='between(t,.18,1.58)')
    done(s)
    s=Shot('13-notes',1.5,A/'florist.png').effect('gblur=sigma=8')
    s.layer(notes_card(),'','0','22*(1-min(t/.18,1))')
    done(s)
    s=Shot('14-payoff',3.1,A/'reaction.png')
    s.mouth('dry-talk.png',(421,415,135,95),'payoff',.73)
    s.layer(A/'blink.png','scale=1080:1920,crop=260:115:330:305','330','305','between(t,2.24,2.37)')
    s.layer(A/'delivery-arm.png','scale=760:-1','590','740+2*sin(t*1.7)')
    s.effect('crop=810:1440:125:120,scale=1080:1920')
    s.layer(caption('Not to overdo it.','cap-payoff'),enable='between(t,.69,2.35)')
    done(s)
    s=Shot('15-reveal',7.6,A/'florist.png')
    s.layer(reveal_card(0))
    s.layer(reveal_card(1),enable='gte(t,1.20)')
    for text,n,a,b in [('The missing safeguard?','a',.35,1.42),('Idempotency.','b',1.42,2.45),('Retrying the same order','c',2.45,3.85),("shouldn’t create another bouquet.",'d',3.85,6.3)]:
        s.layer(caption(text,'cap-reveal-'+n),enable=f'between(t,{a},{b})')
    done(s)
    return shots

def mix_sound():
    sr=48000; count=int(sr*DUR); t=np.arange(count)/sr
    rng=np.random.default_rng(92)
    music=np.zeros((count,2)); effects=np.zeros((count,2)); dialogue=np.zeros((count,2))
    def put(dest,at,a,pan=0):
        start=round(at*sr); n=min(len(a),count-start)
        dest[start:start+n,0]+=a[:n]*(1-.25*pan)
        dest[start:start+n,1]+=a[:n]*(1+.25*pan)
    def pluck(at,freq,amp=.035,dur=.7):
        q=np.arange(round(sr*dur))/sr
        a=amp*(np.sin(2*np.pi*freq*q)+.18*np.sin(4*np.pi*freq*q))*np.exp(-6*q)*(1-np.exp(-90*q))
        put(music,at,a)
    # Small distinct motifs, each serving a scene; no continuous musical bed.
    for at,f in ((.05,392),(.26,494),(.48,587),(3.53,330),(3.89,440),(5.50,523),(6.15,392),(6.48,494),(8.35,587),(9.48,220),(10.88,208),(11.5,196),(12.75,185),(14.4,440),(14.77,554),(15.2,659),(26.5,330),(27.2,440),(28.0,554),(32.2,392),(32.65,494),(33.10,587)):
        pluck(at,f,.024 if at<26 else .03)
    # Barely audible original room tone under the whole scene.
    n=rng.normal(0,1,count)
    ambient=np.convolve(n,np.ones(120)/120,mode='same')*.008
    effects[:,0]+=ambient; effects[:,1]+=ambient
    def rustle(at,dur=.3,amp=.04):
        q=np.arange(round(sr*dur))/sr; n=rng.normal(0,1,len(q))
        a=np.convolve(n,[1,-.65],mode='same')*amp*np.sin(np.pi*q/dur)**2*(.3+.7*np.sin(q*82)**2)
        put(effects,at,a,.5)
    for args in ((.12,.28,.032),(1.35,.36,.033),(14.25,.35,.035),(17.64,.70,.038),(18.50,.22,.03),(20.05,.26,.025),(21.85,.4,.026)):
        rustle(*args)
    def click(at,amp=.07):
        q=np.arange(round(sr*.045))/sr
        put(effects,at,amp*rng.normal(0,1,len(q))*np.exp(-120*q))
    for at in (6.12,6.28,6.42,6.56,6.71,7.05,7.22,8.28,11.59,13.19):click(at,.025 if at<8 else .065)
    for at in (8.72,12.02,13.52):
        q=np.arange(round(sr*.4))/sr
        a=.024*(np.sin(2*np.pi*180*q)+.45*rng.normal(0,1,len(q)))*np.sin(np.pi*q/.4)**2
        put(effects,at,a,-.5)
        click(at+.29,.036)
    # Speech normalized by active RMS; leave headroom before final loudness pass.
    duck=np.ones(count)
    for name,at in VOICES.items():
        p=B/(name+'-48k.wav')
        run([FF,'-y','-loglevel','error','-i',R/'audio'/f'{name}.wav','-ar','48000',p])
        a,_=sf.read(p); active=a[np.abs(a)>.025]
        gain=min(2.2,.14/max(np.sqrt(np.mean(active**2)),.01))
        a=a*gain
        put(dialogue,at,a)
        st=max(0,round((at-.06)*sr)); en=min(count,round((at+len(a)/sr+.13)*sr))
        duck[st:en]=.32
    # Smooth duck boundaries over 25ms.
    duck=np.convolve(np.pad(duck,(600,600),mode='edge'),np.ones(1201)/1201,mode='valid')
    mix=dialogue+music*duck[:,None]+effects
    mix*=np.minimum(1,t/.04)[:,None]*np.minimum(1,(DUR-t)/.16)[:,None]
    peak=float(np.max(np.abs(mix)))
    if peak>.9: mix*=.9/peak
    sf.write(B/'mix.wav',mix,sr,subtype='PCM_24')
    return {'raw_mix_peak':peak,'saved_mix_peak':float(abs(mix).max()),'voices':len(VOICES)}

def stamp(t):
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def main():
    shots=build_shots()
    audioqa=mix_sound()
    cat=B/'shots.ffconcat'
    cat.write_text('ffconcat version 1.0\n'+''.join("file '"+str(p).replace("'","'\\''")+"'\n" for p in shots))
    run([FF,'-y','-loglevel','error','-f','concat','-safe','0','-i',cat,'-i',B/'mix.wav','-map','0:v','-map','1:a','-t',str(DUR),'-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',O/'short.mp4'])
    data=json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(O/'short.mp4')]))
    v=next(s for s in data['streams'] if s['codec_type']=='video'); a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1080,1920,'h264','30/1')
    assert a['codec_name']=='aac' and a['sample_rate']=='48000'
    assert abs(float(data['format']['duration'])-DUR)<.10
    for i,(name,at) in enumerate(VOICES.items()):
        assert at+META[name]['duration']<=DUR
    (O/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(at)} --> {stamp(at+META[name]["duration"])}\n{META[name]["text"]}' for i,(name,at) in enumerate(VOICES.items()))+'\n')
    (O/'production-qa.json').write_text(json.dumps({'duration':data['format']['duration'],'video':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'audio':a['codec_name'],'sample_rate':a['sample_rate'],'audio_mix':audioqa,'animation':'Limited animation with audio-driven two-pose mouths, blink drawings, prop motion and reaction keyframes; not phoneme-level facial animation.'},indent=2)+'\n')
    for i,t in enumerate((1.9,4.5,7.5,8.95,10.1,11.35,12.3,13.75,15.6,18.8,20.4,22.5,24.6,28.5,32.8)):
        run([FF,'-y','-loglevel','error','-ss',str(t),'-i',O/'short.mp4','-frames:v','1',B/f'qa-{i:02}.jpg'])
    shutil.copyfile(O/'short.mp4',O/'story-cut.mp4')
    shutil.copyfile(O/'subtitles.srt',B/'story-subtitles.srt')
    run([sys.executable,R/'add_intro.py'])
    print(O/'short.mp4')

if __name__=='__main__': main()
