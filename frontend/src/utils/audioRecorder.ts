declare global {
  interface Window {
    webkitAudioContext?: any,
    stream?: any
  }
}

interface AudioRecorderState {
  color: string
}

interface AudioData {
  blob: Blob
  url: string
  type: string
}

interface AudioRecorderProps {
  args: Map<string, any>
  width: number
  disabled: boolean
}

class Recorder {
  public constructor(sample_rate = null, pause_threshold = null, start_threshold = null, end_threshold = null) {
    this.sample_rate = sample_rate;
    this.pause_threshold = pause_threshold;
    this.start_threshold = start_threshold;
    this.end_threshold = end_threshold;
    if (typeof window !== 'undefined') {
      this.AudioContext = window.AudioContext || window.webkitAudioContext;
    }
    //super(props)
    //this.state = { color: this.props.args["neutral_color"] }
  }

  stream: MediaStream | null = null;
  context: any;
  AudioContext = null;
  type: string = "audio/wav";
  sampleRate: number | null = null;
  phrase_buffer_count: number | null = null;
  pause_buffer_count: number | null = null;
  pause_count: number = 0;
  stage: string | null = null;
  volume: any = null;
  audioInput: any = null;
  analyser: any = null;
  recorder: any = null;
  recording: boolean = false;
  leftchannel: Float32Array[] = [];
  rightchannel: Float32Array[] = [];
  leftBuffer: Float32Array | null = null;
  rightBuffer: Float32Array | null = null;
  recordingLength: number = 0;
  tested: boolean = false;
  sample_rate: any;
  pause_threshold: any;
  start_threshold: any;
  end_threshold: any;
  audioUrl: string = null;
  audioBlob: Blob = null;

  //get mic stream
  getStream = (): Promise<MediaStream> => {
    return navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  };

  setupMic = async () => {
    try {
      window.stream = this.stream = await this.getStream();
      if (this.stream) {

      } else { console.error('stream passing failed') }
    } catch (err) {
      console.log("Error: Issue getting mic", err);
    }

    this.startRecording();
  };

  closeMic = () => {
    this.stream!.getAudioTracks().forEach((track) => {
      track.stop();
    });
    this.audioInput.disconnect(0);
    this.analyser.disconnect(0);
    this.recorder.disconnect(0);
  };

  writeUTFBytes = (view: DataView, offset: number, string: string) => {
    let lng = string.length;
    for (let i = 0; i < lng; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  mergeBuffers = (channelBuffer: Float32Array[], recordingLength: number) => {
    let result = new Float32Array(recordingLength);
    let offset = 0;
    let lng = channelBuffer.length;
    for (let i = 0; i < lng; i++) {
      let buffer = channelBuffer[i];
      result.set(buffer, offset);
      offset += buffer.length;
    }
    return result;
  };

  interleave = (leftChannel: Float32Array, rightChannel: Float32Array) => {
    let length = leftChannel.length + rightChannel.length;
    let result = new Float32Array(length);

    let inputIndex = 0;

    for (let index = 0; index < length;) {
      result[index++] = leftChannel[inputIndex];
      result[index++] = rightChannel[inputIndex];
      inputIndex++;
    }
    return result;
  };

  startRecording = () => {
    let input_sample_rate = this.sample_rate;
    if (input_sample_rate === null) {
      this.context = new this.AudioContext();
      this.sampleRate = this.context.sampleRate;
    } else {
      this.context = new this.AudioContext(
        { "sampleRate": input_sample_rate }
      );
      this.sampleRate = input_sample_rate;
    }
    console.log(`Sample rate ${this.sampleRate}Hz`);

    // create buffer states counts
    let bufferSize = 2048;
    let seconds_per_buffer = bufferSize / this.sampleRate!;
    this.pause_buffer_count = Math.ceil(
      this.pause_threshold / seconds_per_buffer
    );
    this.pause_count = 0;
    this.stage = "start";

    // creates a gain node
    this.volume = this.context.createGain();

    // creates an audio node from teh microphone incoming stream
    this.audioInput = this.context.createMediaStreamSource(this.stream);

    // Create analyser
    this.analyser = this.context.createAnalyser();

    // connect audio input to the analyser
    this.audioInput.connect(this.analyser);

    // connect analyser to the volume control
    // analyser.connect(volume);

    this.recorder = this.context.createScriptProcessor(bufferSize, 2, 2);

    // we connect the volume control to the processor
    // volume.connect(recorder);

    this.analyser.connect(this.recorder);

    // finally connect the processor to the output
    this.recorder.connect(this.context.destination);
    const self = this;  // to reference component from inside the function
    this.recorder.onaudioprocess = function (e: any) {
      // console.log(self.recording);
      // Check
      if (!self.recording) return;
      // Do something with the data, i.e Convert this to WAV
      let left = e.inputBuffer.getChannelData(0);
      let right = e.inputBuffer.getChannelData(1);
      if (!self.tested) {
        self.tested = true;
        // if this reduces to 0 we are not getting any sound
        if (!left.reduce((a: number, b: number) => a + b)) {
          console.log("Error: There seems to be an issue with your Mic");
          // clean up;
          self.stop();
          self.stream!.getTracks().forEach(function (track: any) {
            track.stop();
          });
          self.context.close();
        }
      }
      // Check energy level
      let energy = Math.sqrt(
        left.map((x: number) => x * x).reduce((a: number, b: number) => a + b) / left.length
      );
      if (self.stage === "start" && energy > self.start_threshold) {
        self.stage = "speaking";
      } else if (self.stage === "speaking") {
        if (energy > self.end_threshold) {
          self.pause_count = 0;
        } else {
          self.pause_count += 1;
          if (self.pause_count > self.pause_buffer_count!) {
            self.stop();
          }
        }
      }
      // let radius = 33.0 + Math.sqrt(1000.0 * energy);
      // this.props.setRadius(radius.toString());

      // we clone the samples
      self.leftchannel.push(new Float32Array(left));
      self.rightchannel.push(new Float32Array(right));
      self.recordingLength += bufferSize;
    };
    // this.visualize();
  };

  start = async () => {
    this.recording = true;
    /*this.setState({
      color: this.props.args["recording_color"]
    })*/
    await this.setupMic();
    console.log('Mic Permission granted');
    // reset the buffers for the new recording
    this.leftchannel.length = this.rightchannel.length = 0;
    this.recordingLength = 0;
  };
  check = () => {
    return window.stream;
  }
  stop = async () => {
    this.recording = false;
    /*this.setState({
      color: this.props.args["neutral_color"]
    })*/
    this.closeMic();
    console.log(this.recordingLength);

    // we flat the left and right channels down
    this.leftBuffer = this.mergeBuffers(this.leftchannel, this.recordingLength);
    this.rightBuffer = this.mergeBuffers(
      this.rightchannel,
      this.recordingLength
    );
    // we interleave both channels together
    let interleaved = this.interleave(this.leftBuffer, this.rightBuffer);

    ///////////// WAV Encode /////////////////
    // from http://typedarray.org/from-microphone-to-wav-with-getusermedia-and-web-audio/
    //

    // we create our wav file
    let buffer = new ArrayBuffer(44 + interleaved.length * 2);
    let view = new DataView(buffer);

    // RIFF chunk descriptor
    this.writeUTFBytes(view, 0, "RIFF");
    view.setUint32(4, 44 + interleaved.length * 2, true);
    this.writeUTFBytes(view, 8, "WAVE");
    // FMT sub-chunk
    this.writeUTFBytes(view, 12, "fmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    // stereo (2 channels)
    view.setUint16(22, 2, true);
    view.setUint32(24, this.sampleRate!, true);
    view.setUint32(28, this.sampleRate! * 4, true);
    view.setUint16(32, 4, true);
    view.setUint16(34, 16, true);
    // data sub-chunk
    this.writeUTFBytes(view, 36, "data");
    view.setUint32(40, interleaved.length * 2, true);

    // write the PCM samples
    let lng = interleaved.length;
    let index = 44;
    let volume = 1;
    for (let i = 0; i < lng; i++) {
      view.setInt16(index, interleaved[i] * (0x7fff * volume), true);
      index += 2;
    }

    // our final binary blob
    console.log(view);
    const blob = new Blob([view], { type: this.type });
    const audioUrl = URL.createObjectURL(blob);


    await this.onStop({
      blob: blob,
      url: audioUrl,
      type: this.type,
    });
    this.audioUrl = audioUrl;
    this.audioBlob = blob;
  };

  private onClicked = async () => {
    if (!this.recording) {
      await this.start()
    } else {
      await this.stop()
    }
  }

  private onStop = async (data: AudioData) => {
    var buffer = await data.blob.arrayBuffer();
    var json_string = JSON.stringify(Array.from(new Uint8Array(buffer)));
  }

}

export default Recorder;