num=[3,16,41,28];
den=[1,14,110,528,1494,2177,112];
subplot(211);
nyquist(num,den);
subplot(212);
pzmap(num,den)
