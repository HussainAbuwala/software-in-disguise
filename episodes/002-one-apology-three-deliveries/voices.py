from pathlib import Path
import os, json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT=Path(__file__).resolve().parent
MODEL=Path(os.environ.get('KOKORO_MODEL_DIR',ROOT.parents[1]/'models'))
k=Kokoro(str(MODEL/'kokoro.onnx'),str(MODEL/'voices.bin'))
lines=[
 ('grand','af_bella',"You don't have to make everything a grand gesture.",1.04),
 ('okay','am_michael','Okay. One little bouquet.',.98),
 ('note','am_michael',"I'm learning not to overdo it.",1.02),
 ('through','am_michael','Did it go through?',.98),
 ('sweet','af_bella',"That's actually sweet.",.94),
 ('two','am_adam','And these two.',.94),
 ('payoff','af_bella','Not to overdo it.',.90),
 ('reveal','bf_emma',"The missing safeguard? Idempotency. Retrying the same order shouldn't create another bouquet.",1.05),
]
out=ROOT/'audio'; out.mkdir(exist_ok=True)
meta={}
for name,voice,text,speed in lines:
 a,sr=k.create(text,voice=voice,speed=speed,lang='en-gb' if voice.startswith('b') else 'en-us')
 # Keep consonant onsets and natural tails, remove excessive model padding.
 inds=np.flatnonzero(np.abs(a)>.007)
 if len(inds): a=a[max(0,inds[0]-int(.06*sr)):min(len(a),inds[-1]+int(.13*sr))]
 a=a*min(1.0,.82/max(float(np.max(np.abs(a))),1e-8))
 sf.write(out/f'{name}.wav',a,sr)
 rms=[float(np.sqrt(np.mean(a[i:i+int(sr/30)]**2))) for i in range(0,len(a),int(sr/30))]
 meta[name]={'voice':voice,'text':text,'speed':speed,'duration':len(a)/sr,'sample_rate':sr,'rms_30fps':rms}
 print(name,round(len(a)/sr,3),flush=True)
(out/'dialogue.json').write_text(json.dumps(meta,indent=2)+'\n')
