'use client'
import { useState, useRef } from "react";
import { Button, Typography, Stack } from "@mui/material";

const mimeType = "audio/wav";

const AudioRecorder = () => {
    const [permission, setPermission] = useState(false);

    const mediaRecorder = useRef(null);

    const [recordingStatus, setRecordingStatus] = useState("inactive");

    const [stream, setStream] = useState(null);

    const [audio, setAudio] = useState(null);

    const [audioChunks, setAudioChunks] = useState([]);

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const mediaStream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false,
                });
                setPermission(true);
                setStream(mediaStream);
            } catch (err) {
                alert(err.message);
            }
        } else {
            alert("The MediaRecorder API is not supported in your browser.");
        }
    };

    const startRecording = async () => {
        setRecordingStatus("recording");
        const media = new MediaRecorder(stream, { type: mimeType });

        mediaRecorder.current = media;

        mediaRecorder.current.start();

        let localAudioChunks = [];

        mediaRecorder.current.ondataavailable = (event) => {
            if (typeof event.data === "undefined") return;
            if (event.data.size === 0) return;
            localAudioChunks.push(event.data);
        };

        setAudioChunks(localAudioChunks);
    };

    const stopRecording = () => {
        setRecordingStatus("inactive");
        mediaRecorder.current.stop();

        mediaRecorder.current.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: mimeType });
            const audioUrl = URL.createObjectURL(audioBlob);

            setAudio(audioUrl);

            setAudioChunks([]);
        };
    };

    return (
        <div>
            <Typography variant="h2" gutterBottom sx={{ display: 'none' }}>Audio Recorder</Typography>
            <Stack
                className="audio-controls"
                direction={{ xs: 'column', sm: 'column' }}
                alignSelf="center"
                spacing={1}
                useFlexGap
                sx={{ pt: 2, width: { xs: '100%', sm: 'auto' } }}>
                {!permission ? (
                    <Button variant="contained" color="primary" onClick={getMicrophonePermission} type="button">
                        Click to Turn On Microphone
                    </Button>
                ) : null}
                {permission && recordingStatus === "inactive" ? (
                    <Button variant="contained" color="primary" onClick={startRecording} type="button">
                        Start Recording
                    </Button>
                ) : null}
                {recordingStatus === "recording" ? (
                    <Button variant="contained" color="primary" onClick={stopRecording} type="button">
                        Stop Recording
                    </Button>
                ) : null}
            </Stack>
            <Stack
                className="audio-player"
                direction={{ xs: 'column', sm: 'column' }}
                alignSelf="center"
                spacing={1}
                useFlexGap
                sx={{ pt: 2, width: { xs: '100%', sm: 'auto' } }}>
                {audio ? (
                    <>
                        <audio src={audio} controls></audio>
                        <Button variant="contained" color="primary" download href={audio}>
                            Download Recording
                        </Button>
                    </>
                ) : <>
                    <audio src={null} controls></audio>
                </>}
            </Stack>
        </div>
    );
};

export default AudioRecorder;