'use client'
import { useState, useRef } from "react";
import { Button, Typography, Stack, TextField, LinearProgress, CircularProgress } from "@mui/material";
import { Box } from "@mui/system";
import { useSTT } from "../api/speech_trainer/useSTT";
import Recorder from "../utils/audioRecorder";
import LanguageSelector from "./LanguageSelector";
import { LANG } from "../constant";

const AudioRecorder = () => {

    const [recordingStatus, setRecordingStatus] = useState("inactive");

    const [audio, setAudio] = useState(null);

    const { mutate: createSTT, isLoading: isSTTLoading } = useSTT();

    const [recorder, setRecorder] = useState(null);

    const [generatedTextInput, setGeneratedTextInput] = useState('');

    const [isGenerateText, setIsGenerateText] = useState(false);

    const [lang, setLang] = useState(LANG.ENGLISH.value);

    const handleLanguageChange = (event) => {
        setLang(event.target.value);
    };

    const startRecording = async () => {
        setRecordingStatus("recording");
        const recorderStream = new Recorder();

        await recorderStream.start();
        setRecorder(recorderStream);
        setIsGenerateText(false);
    };

    const stopRecording = async () => {
        setRecordingStatus("inactive");
        await recorder.stop();
        setAudio(recorder.audioUrl);
        // console.log(recorder.audioUrl);
        // console.log(recorder.audioBlob);
        createSTT({
            data: { file: recorder.audioBlob }, lang: lang
        }, {
            onSuccess: (response) => {
                setGeneratedTextInput(response.text);
            }
        });
        setIsGenerateText(true);
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
            {recordingStatus === "inactive" ? (
                <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }} flexDirection={{ xs: 'column', sm: 'row' }} >
                    <LanguageSelector onChange={handleLanguageChange} value={lang} />
                    <Button variant="contained" color="primary" onClick={startRecording} type="button">
                        Start Recording
                    </Button>
                </Box>
            ) : null}
            {recordingStatus === "recording" ? (
                <Button variant="contained" color="primary" onClick={stopRecording} type="button">
                    Stop Recording
                </Button>
            ) : null}

            {recordingStatus === 'recording' && < LinearProgress sx={{ mt: 1 }} />}
            {isGenerateText ? isSTTLoading ? (<center><CircularProgress /></center>) : (
                <Box sx={{ width: '100%' }} direction={{ xs: 'column', sm: 'column' }}>
                    <center><audio src={audio} controls></audio></center>
                    Result
                    <TextField
                        id="generated-text"
                        multiline
                        rows={4}
                        sx={{ m: 1 }}
                        placeholder="Generated Text will be shown here."
                        fullWidth
                        disabled
                        value={generatedTextInput}
                    />
                </Box>
            ) : null
            }
        </Stack >
    );
};

export default AudioRecorder;