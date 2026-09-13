from pathlib import Path
from kokoro_onnx import Kokoro
import soundfile as sf
import json
import os
R=Path(__file__).resolve().parent
MODEL_DIR=Path(os.environ.get('KOKORO_MODEL_DIR',R.parents[1]/'models'))
k=Kokoro(str(MODEL_DIR/'kokoro.onnx'),str(MODEL_DIR/'voices.bin'))
lines=[
 ('excuse','af_bella','Excuse me. That is my seat.',1.0),
 ('ticket','af_bella','A twelve.',.95),
 ('mine','am_michael','Mine too.',.93),
 ('last','af_bella','One ticket left!',1.04),
 ('yes','am_michael','Yes! Got it.',1.07),
 ('also','af_bella','Got it!',1.08),
 ('under','af_bella','It is not under there.',1.0),
 ('check','am_michael','Just checking.',.94),
 ('solution','bf_emma','We have arranged alternative seating.',1.0),
 ('support','af_bella','Does it come with emotional support?',1.03),
 ('reveal','am_michael','In software, this is a race condition. Both checked the seat before either booking marked it sold.',1.12),
]
meta={}
for name,voice,text,speed in lines:
 a,sr=k.create(text,voice=voice,speed=speed,lang='en-gb' if voice.startswith('b') else 'en-us')
 sf.write(R/'audio'/f'{name}.wav',a,sr)
 meta[name]={'voice':voice,'text':text,'duration':len(a)/sr}
 print(name,round(len(a)/sr,2),flush=True)
(R/'audio/dialogue.json').write_text(json.dumps(meta,indent=2))
