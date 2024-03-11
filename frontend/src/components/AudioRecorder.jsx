'use client'
import { useState, useRef } from "react";
import { Button, Typography, Stack, TextField, LinearProgress } from "@mui/material";
import { Box } from "@mui/system";
import { useSTT } from "../api/speech_trainer/useSTT";

const mimeType = "audio/wav";

const AudioRecorder = () => {
    const [permission, setPermission] = useState(false);

    const mediaRecorder = useRef(null);

    const [recordingStatus, setRecordingStatus] = useState("inactive");

    const [stream, setStream] = useState(null);

    const [audio, setAudio] = useState(null);

    const [audioChunks, setAudioChunks] = useState([]);

    const { mutate: createSTT, isLoading: isUpdateLoading } = useSTT();

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

            createSTT({ file: audioBlob, text: 'test' }, { onError: (error) => { console.error('error calling API'); } });
        };
    };

    return (
        <Stack
            className="audio-controls"
            direction={{ xs: 'column', sm: 'column' }}
            alignSelf="center"
            spacing={1}
            useFlexGap
            sx={{ pt: 2, width: { xs: '100%', sm: '50%' } }}>
            <Typography variant="h2" gutterBottom sx={{ display: 'none' }}>Audio Recorder</Typography>
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

            {recordingStatus === 'recording' && < LinearProgress sx={{ mt: 1 }} />}
            {audio && recordingStatus === 'inactive' ? (
                <Box sx={{ width: '100%' }} direction={{ xs: 'column', sm: 'column' }}>
                    <center><audio src={audio} controls></audio></center>
                    <Button variant="contained" color="primary" download href={audio} fullWidth>
                        Download Recording
                    </Button>
                    <TextField
                        id="generated-text"
                        label="Generated Text"
                        multiline
                        rows={4}
                        sx={{ m: 1 }}
                        placeholder="Generated Text will be shown here."
                        fullWidth
                        disabled
                    />
                </Box>
            ) : null
            }
        </Stack >
    );
};

export default AudioRecorder;