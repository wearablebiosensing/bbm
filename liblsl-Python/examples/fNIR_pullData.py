from pylsl import StreamInlet, resolve_stream

print('Looking for (fNIR) stream...')

fNIR_streams = resolve_stream('type', 'NIRS')

stream_inlet = StreamInlet(fNIR_streams[0])

while True:
    sample, timestamp = stream_inlet.pull_sample()
    print((timestamp, sample)+"\n")

print("...Fin.")
