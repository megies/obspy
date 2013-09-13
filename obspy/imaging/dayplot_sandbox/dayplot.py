from obspy import readEvents, read
cat = readEvents("2010-05-27.xml")
st = read("uh1.mseed")
st.plot(type="dayplot", events=cat)
