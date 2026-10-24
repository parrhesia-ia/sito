import numpy as np, subprocess, wave
SR=44100
def env(n,a,d):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def lpf(x,cut):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); m=f>cut; X[m]*=np.exp(-(f[m]-cut)/(cut*0.3)); return np.fft.irfft(X,len(x))
def reverb(x,decay=1.8,mix=0.35):
    n=int(decay*SR); ir=np.random.RandomState(1).randn(n)*np.exp(-np.arange(n)/SR*5/decay); ir=lpf(ir,4000)
    w=np.convolve(x,ir); w=w/(np.max(np.abs(w))+1e-9)*np.max(np.abs(x))
    out=np.zeros(len(w)); out[:len(x)]+=x*(1-mix); out+=w*mix; return out
def save(name,x):
    x=x/(np.max(np.abs(x))+1e-9)*0.89; d=(np.stack([x,x],1)*32767).astype(np.int16)
    with wave.open(name+".wav","wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",name+".wav","-b:a","192k",name+".mp3"],check=True)
def tone(f,dur,harm=(1,.5,.3,.2,.1),detune=0):
    t=np.arange(int(dur*SR))/SR; return sum(a*np.sin(2*np.pi*f*(k+1)*t*(1+detune*k)) for k,a in enumerate(harm))
def noise(dur,seed=0): return np.random.RandomState(seed).randn(int(dur*SR))
def place(buf,x,at):
    i=int(at*SR); m=min(len(x),len(buf)-i); buf[i:i+m]+=x[:m]

b=np.zeros(int(3.0*SR))
place(b,tone(55,3.0,(1,.6,.35,.25,.15,.1),0.0008)*env(int(3*SR),0.005,0.9),0)
place(b,lpf(noise(1.2,2),180)*env(int(1.2*SR),0.004,0.35)*6,0)
place(b,lpf(noise(0.25,3),900)*env(int(0.25*SR),0.001,0.03)*5+tone(90,0.25,(1,))*env(int(0.25*SR),0.001,0.05)*1.2,1.15)
save("firma_A_timbro",reverb(b,1.6,0.3)[:int(4.2*SR)])

b=np.zeros(int(3.4*SR))
for at in (0.0,0.42): place(b,tone(48,0.6,(1,.3))*env(int(0.6*SR),0.003,0.16)*1.4,at)
n=int(1.6*SR); place(b,lpf(noise(1.6,4),2500)*np.linspace(0,1,n)**2*0.5,1.0)
place(b,tone(2400,0.4,(1,0,.4,0,.2))*env(int(0.4*SR),0.001,0.06)*0.6,2.6)
save("firma_B_pulsazione",reverb(b,1.4,0.28)[:int(4.2*SR)])

b=np.zeros(int(4.2*SR))
def string(f,dur):
    t=np.arange(int(dur*SR))/SR; ph=np.cumsum(1+0.004*np.sin(2*np.pi*5.5*t))/SR
    x=sum((1/(k+1))*(np.sin(2*np.pi*f*(k+1)*ph)+np.sin(2*np.pi*f*1.003*(k+1)*ph)) for k in range(8))
    e=np.minimum(t/0.12,1)*np.clip((dur-t)/0.25,0,1); return lpf(x,1400)*e
for f,at,du in ((73.42,0,0.7),(87.31,0.7,0.7),(110.0,1.4,0.7),(73.42,2.1,2.0)):
    place(b,string(f,du),at); place(b,string(f*2,du)*0.4,at)
place(b,lpf(noise(1.0,5),200)*env(int(1*SR),0.003,0.3)*4,2.1)
save("firma_C_archi",reverb(b,2.0,0.35)[:int(5.0*SR)])

L=24; t=np.arange(int(L*SR))/SR
pad=sum(a*np.sin(2*np.pi*f*t+ph) for f,a,ph in ((36.71,1,0),(55.0,.7,1),(73.42,.5,2),(110.0,.25,.5),(146.8,.12,1.2)))
pad*=0.75+0.25*np.sin(2*np.pi*t/8)
bed=pad+lpf(noise(L,6),600)*0.15; fade=np.minimum(np.minimum(t/2,1),np.minimum((L-t)/2,1)); save("tappeto",bed*fade)
print("ok")
