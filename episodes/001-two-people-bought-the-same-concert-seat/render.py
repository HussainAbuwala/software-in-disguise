#!/usr/bin/env python3
"""Assemble the approved vertical comic cut from two four-panel pages."""
from pathlib import Path
import subprocess, shutil, math
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "render"
FINAL = ROOT / "deliverables" / "short.mp4"
W, H, FPS, DURATION = 1080, 1920, 30, 30.0
INK = (14, 17, 24)
CREAM = (244, 235, 211)
YELLOW = (246, 196, 65)

def run(args):
    subprocess.run(args, cwd=ROOT, check=True)

def font(size, bold=False):
    choices = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Verdana.ttf",
    ]
    for p in choices:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def crop_panels(page, stem):
    """Use ffmpeg for all generated-art cropping/reframing."""
    probe = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0:s=x",str(page)], text=True)
    pw, ph = map(int, probe.strip().split("x")); cw, ch = pw//2, ph//2
    files=[]
    for i,(x,y) in enumerate(((0,0),(cw,0),(0,ch),(cw,ch))):
        dst=OUT/f"{stem}_{i}.png"
        run(["ffmpeg","-y","-loglevel","error","-i",str(page),"-vf",f"crop={cw}:{ch}:{x}:{y}","-frames:v","1",str(dst)])
        files.append(dst)
    return files

def fit_panel(path, box):
    im=Image.open(path).convert("RGB")
    x,y,w,h=box
    scale=min(w/im.width,h/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    return im,(x+(w-im.width)//2,y+(h-im.height)//2)

def wrap(draw, text, f, maxw):
    words=text.split(); lines=[]; cur=""
    for word in words:
        test=(cur+" "+word).strip()
        if draw.textbbox((0,0),test,font=f)[2] <= maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines

def bubble(im, text, anchor="bottom", size=48, speaker="center", y_override=None):
    d=ImageDraw.Draw(im); f=font(size, True)
    maxw=880; lines=wrap(d,text,f,maxw-72)
    lh=size+10; bw=max(d.textbbox((0,0),ln,font=f)[2] for ln in lines)+72; bh=lh*len(lines)+46
    if speaker == "left": x=70
    elif speaker == "right": x=W-bw-70
    else: x=(W-bw)//2
    y=(H-bh-94 if anchor=="bottom" else 74) if y_override is None else y_override
    d.rounded_rectangle((x,y,x+bw,y+bh),radius=34,fill=CREAM,outline=INK,width=7)
    # Short comic tail gives dialogue a clear speaker direction.
    tipx = x+80 if speaker=="left" else (x+bw-80 if speaker=="right" else x+bw//2)
    if anchor == "bottom":
        d.polygon(((tipx-25,y),(tipx+25,y),(tipx,y-40)),fill=CREAM)
        d.line(((tipx-25,y),(tipx,y-40),(tipx+25,y)),fill=INK,width=7,joint="curve")
    else:
        d.polygon(((tipx-25,y+bh),(tipx+25,y+bh),(tipx,y+bh+40)),fill=CREAM)
        d.line(((tipx-25,y+bh),(tipx,y+bh+40),(tipx+25,y+bh)),fill=INK,width=7,joint="curve")
    tx=x+bw//2
    for j,ln in enumerate(lines):
        d.text((tx,y+22+j*lh),ln,font=f,fill=INK,anchor="ma")
    return im

def label(im, text, y=62):
    d=ImageDraw.Draw(im); f=font(31,True); bb=d.textbbox((0,0),text,font=f)
    x=(W-(bb[2]-bb[0]+48))//2
    d.rounded_rectangle((x,y,W-x,y+56),radius=8,fill=YELLOW,outline=INK,width=4)
    d.text((W//2,y+28),text,font=f,fill=INK,anchor="mm")

def stacked(top, bottom=None, text=None, tag=None, bottom_text=False, speaker="center"):
    im=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(im)
    # slim cream gutters, page art dominates
    boxes=[(20,20,1040,895),(20,935,1040,895)]
    for n,p in enumerate((top,bottom)):
        x,y,w,h=boxes[n]
        d.rectangle((x-5,y-5,x+w+5,y+h+5),fill=CREAM)
        if p:
            art,pos=fit_panel(p,(x,y,w,h)); im.paste(art,pos)
        else:
            d.rectangle((x,y,x+w,y+h),fill=(20,24,32))
            d.line((x+100,y+h//2,x+w-100,y+h//2),fill=(43,47,55),width=3)
    if tag: label(im,tag)
    if text: bubble(im,text,"bottom" if bottom_text else "top",speaker=speaker)
    return im

def focus(p, text=None, tag=None, speaker="center"):
    im=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(im)
    box=(20,130,1040,1040); d.rectangle((15,125,1065,1175),fill=CREAM)
    art,pos=fit_panel(p,box); im.paste(art,pos)
    if tag: label(im,tag,48)
    if text:
        bubble(im,text,"bottom",speaker=speaker,y_override=1215)
        # A narrow page rule closes the composition below the dialogue beat.
        d.line((150,1585,930,1585),fill=CREAM,width=4)
        d.ellipse((522,1575,542,1595),fill=YELLOW)
    return im

def final_card(stage):
    im=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(im)
    # subtle radial concert glow
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    for r in range(620,20,-20): gd.ellipse((W//2-r,H//2-r,W//2+r,H//2+r),fill=(42,54,76,max(0,2)))
    im=Image.alpha_composite(im.convert("RGBA"),glow).convert("RGB"); d=ImageDraw.Draw(im)
    if stage==1:
        f=font(42,True); d.text((W//2,260),"BOTH CHECK A12",font=f,fill=CREAM,anchor="mm")
        for x in (250,610):
            d.rounded_rectangle((x,340,x+220,500),25,fill=CREAM,outline=YELLOW,width=8)
            d.text((x+110,395),"A12",font=font(50,True),fill=INK,anchor="mm")
            d.text((x+110,458),"AVAILABLE",font=font(22,True),fill=(36,126,81),anchor="mm")
        d.text((W//2,610),"at the same time",font=font(35,True),fill=(188,190,196),anchor="mm")
    if stage>=2:
        f=font(42,True); d.text((W//2,260),"BOTH CONFIRMED",font=f,fill=CREAM,anchor="mm")
        for x in (250,610):
            d.rounded_rectangle((x,340,x+220,500),25,fill=CREAM,outline=YELLOW,width=8)
            d.text((x+110,395),"A12",font=font(50,True),fill=INK,anchor="mm")
            d.text((x+110,458),"CONFIRMED",font=font(20,True),fill=(36,126,81),anchor="mm")
    if stage>=2:
        d.text((W//2,650),"ONE SEAT",font=font(42,True),fill=CREAM,anchor="mm")
        d.rounded_rectangle((390,730,690,940),35,fill=(90,55,40),outline=CREAM,width=10)
        d.rectangle((420,930,450,1110),fill=CREAM); d.rectangle((630,930,660,1110),fill=CREAM)
    if stage>=3:
        d.text((W//2,1260),"A RACE CONDITION",font=font(74,True),fill=YELLOW,anchor="mm")
        lines=wrap(d,"Both checked before either booking marked the seat sold.",font(43,True),880)
        for i,line in enumerate(lines): d.text((W//2,1360+i*58),line,font=font(43,True),fill=CREAM,anchor="mm")
    d.text((W//2,1740),"SOFTWARE IN DISGUISE",font=font(30,True),fill=(188,190,196),anchor="mm")
    d.text((W//2,1790),"EPISODE 01",font=font(25,True),fill=YELLOW,anchor="mm")
    return im

def intro_card(p):
    im=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(im)
    d.text((W//2,105),"SOFTWARE IN DISGUISE",font=font(56,True),fill=YELLOW,anchor="mm")
    d.rounded_rectangle((395,165,685,225),14,fill=CREAM)
    d.text((W//2,195),"EPISODE 01",font=font(28,True),fill=INK,anchor="mm")
    box=(100,285,880,880); d.rectangle((92,277,988,1173),fill=CREAM)
    art,pos=fit_panel(p,box); im.paste(art,pos)
    d.text((W//2,1310),"TWO TICKETS.",font=font(70,True),fill=CREAM,anchor="mm")
    d.text((W//2,1392),"ONE SEAT.",font=font(70,True),fill=YELLOW,anchor="mm")
    d.line((220,1500,860,1500),fill=CREAM,width=3)
    d.text((W//2,1570),"Everyday stories. Software revealed.",font=font(29),fill=(200,202,208),anchor="mm")
    return im

def make_sfx():
    sr=48000; t=np.arange(round(DURATION*sr))/sr
    rng=np.random.default_rng(12)
    s=np.zeros(len(t),dtype=np.float32)
    def tone(at,freq,dur=.14,amp=.11,decay=18):
        a=int(at*sr); n=min(int(dur*sr),len(s)-a); q=np.arange(n)/sr
        s[a:a+n]+=amp*np.sin(2*np.pi*freq*q)*np.exp(-decay*q)
    def pluck(at, freq, amp=.028, dur=.7):
        a=int(at*sr); n=min(int(dur*sr),len(s)-a); q=np.arange(n)/sr
        s[a:a+n]+=amp*(np.sin(2*np.pi*freq*q)+.35*np.sin(2*np.pi*freq*2*q))*np.exp(-5*q)
    for at,note in zip((1.4,2.15,3.05,3.78,4.72,5.35),(220,277,233,311,247,208)): pluck(at,note,.022,.65)
    for at,note in zip((6.9,7.35,7.8,8.25,8.8,9.25,9.7,10.15),(523,659,784,659,587,740,880,988)): pluck(at,note,.026,.45)
    tone(9.0,880,.18,.09,12); tone(10.25,1174,.18,.09,12)
    for at,note in ((12.2,196),(13.15,165),(14.0,220),(14.72,185)): pluck(at,note,.025,.85)
    tone(15.35,92,.42,.075,7); tone(18.25,155,.3,.06,10)
    for at,note in ((21.0,392),(21.42,494),(21.86,587),(22.3,784),(28.7,523),(29.08,659),(29.46,784)): pluck(at,note,.026,.65)
    for at in (0.0,6.85,10.95,20.95):
        a=int(at*sr); n=int(.25*sr); q=np.arange(n)/sr
        s[a:a+n]+=rng.normal(0,.035,n)*np.sin(np.pi*np.arange(n)/n)**2
    s[int(6.0*sr):int(6.9*sr)]=0
    sf.write(OUT/"sfx.wav",np.clip(s,-.8,.8),sr)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    FINAL.parent.mkdir(parents=True,exist_ok=True)
    p2=ROOT/"assets/page2.png"
    if not p2.exists(): raise SystemExit("assets/page2.png is required")
    p1=crop_panels(ROOT/"assets/page1.png","p1"); p2s=crop_panels(p2,"p2")
    cards=[
      (0,1.4,intro_card(p1[3])),
      (1.4,3.7,focus(p1[0],"Excuse me. That is my seat.",speaker="right")),
      (3.7,4.7,stacked(p1[0],p1[1],"A12.",bottom_text=True,speaker="right")),
      (4.7,6.0,stacked(p1[2],p1[3],"Mine too.",speaker="left")),
      (6.0,6.9,focus(p1[3])),
      (6.9,8.8,focus(p2s[0],"One ticket left!","FIVE MINUTES EARLIER",speaker="right")),
      (8.8,10.1,stacked(p2s[0],p2s[1],"Yes! Got it.",bottom_text=True,speaker="left")),
      (10.1,11.0,stacked(p2s[0],p2s[1],"Got it!",bottom_text=True,speaker="right")),
      (11.0,12.2,focus(p1[3],None,"BACK AT THE CONCERT")),
      (12.2,13.8,focus(p2s[2],"It is not under there.",speaker="right")),
      (13.8,15.3,focus(p2s[2],"Just checking.",speaker="left")),
      (15.3,18.2,focus(p2s[3],"We have arranged alternative seating.",speaker="center")),
      (18.2,21.0,focus(p2s[3],"Does it come with emotional support?",speaker="right")),
      (21.0,22.3,final_card(1)), (22.3,23.6,final_card(2)), (23.6,DURATION,final_card(3)),
    ]
    concat=[]
    for i,(start,end,im) in enumerate(cards):
        fn=OUT/f"card_{i:02d}.png"; im.save(fn,quality=95)
        concat.extend([f"file '{fn.as_posix()}'",f"duration {end-start:.3f}"])
    concat.append(f"file '{(OUT/f'card_{len(cards)-1:02d}.png').as_posix()}'")
    (OUT/"cards.ffconcat").write_text("ffconcat version 1.0\n"+"\n".join(concat)+"\n")
    make_sfx()
    voices=[("excuse",1.62),("ticket",3.82),("mine",4.82),("last",7.25),("yes",8.95),("also",10.22),("under",12.35),("check",13.95),("solution",15.5),("support",18.38),("reveal",23.8)]
    filters=["[1:a]volume=0.52[sfx]"]; ins=[]
    for i,(name,at) in enumerate(voices,2):
        filters.append(f"[{i}:a]atempo=1.08,adelay={round(at*1000)}|{round(at*1000)},volume=1.15[v{i}]"); ins.append(f"[v{i}]")
    filters.append("[sfx]"+"".join(ins)+f"amix=inputs={1+len(ins)}:duration=longest:normalize=0,alimiter=limit=0.92[a]")
    cmd=["ffmpeg","-y","-loglevel","warning","-f","concat","-safe","0","-i",str(OUT/"cards.ffconcat"),"-i",str(OUT/"sfx.wav")]
    for name,_ in voices: cmd += ["-i",str(ROOT/f"audio/{name}.wav")]
    cmd += ["-filter_complex",";".join(filters),"-map","0:v","-map","[a]","-r",str(FPS),"-t",str(DURATION),"-c:v","libx264","-preset","slow","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(FINAL)]
    run(cmd)
    print(FINAL)

if __name__ == "__main__": main()
