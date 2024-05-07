import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { useState, useRef } from "react";
import { useTTS } from "../api/speech_trainer/useTTS";
import { CircularProgress } from '@mui/material';
import LanguageSelector from '../components/LanguageSelector';
import { LANG } from '../constant';

export default function TextToSpeech() {

    const [audio, setAudio] = useState(null);

    const [isGenerating, setIsGenerating] = useState(false);

    const inputTextField = useRef(null);

    const { mutate: createTTS, isLoading: isTTSLoading } = useTTS();

    const [lang, setLang] = useState(LANG.ENGLISH.value);

    const handleLanguageSelector = (event) => {
        setLang(event.target.value);
    }

    const handleGenerateSpeech = () => {
        setIsGenerating(true);
        const text = inputTextField.current.value;

        //Set audio if audio generated successfully from backend
        createTTS({ data: { text: text }, lang: lang }, {
            onSuccess: (response) => {
                const audioBlob = new Blob([response.data], { type: 'audio/wav' })
                const audioUrl = URL.createObjectURL(audioBlob);
                setAudio(audioUrl);
            }
        });
    }

    return (
        <Box
            id="TextToSpeech"
            sx={{
                width: '100%',
            }}
        >
            <Container
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    pt: { xs: 14, sm: 20 },
                    pb: { xs: 8, sm: 12 },
                }}
            >
                <Stack spacing={2} useFlexGap sx={{ width: { xs: '100%', sm: '70%' } }}>
                    <Typography
                        component="h1"
                        variant="h1"
                        sx={{
                            display: 'flex',
                            flexDirection: { xs: 'column', md: 'row' },
                            alignSelf: 'center',
                            textAlign: 'center',
                        }}
                    >
                        Text&nbsp;
                        <Typography
                            component="span"
                            variant="h1"
                            sx={{
                                color: (theme) =>
                                    theme.palette.mode === 'light' ? 'primary.main' : 'primary.light',
                            }}
                        >
                            to&nbsp;speech
                        </Typography>
                    </Typography>
                    <Typography sx={{ display: 'none' }} variant="body1" textAlign="center" color="text.secondary">
                        Unleashing the Potential of Speech with Our Web-Based Speech Trainer. <br />
                        Transforming Text into Eloquence and Back, Explore the Power of Speech Training with Our Innovative Web Platform.
                    </Typography>
                    <TextField
                        id="input-text"
                        label="Text"
                        multiline
                        rows={4}
                        sx={{ m: 1 }}
                        placeholder="Input your text here."
                        inputRef={inputTextField}
                        fullWidth
                    />
                    <Stack
                        direction={{ xs: 'column', sm: 'column' }}
                        alignSelf="center"
                        spacing={1}
                        useFlexGap
                        sx={{ pt: 2, width: { xs: '100%', sm: '50%' } }}
                    >
                        <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }} flexDirection={{ xs: 'column', sm: 'row' }} >
                            <LanguageSelector onChange={handleLanguageSelector} value={lang} />
                            <Button variant="contained" color="primary" onClick={handleGenerateSpeech} type="button" sx={{ mb: 1 }} >
                                Generate Speech
                            </Button>
                        </Box>
                        {isGenerating ? !isTTSLoading ? (<center><audio src={audio} controls></audio></center>) : (<center><CircularProgress /></center>) : null}
                    </Stack>
                    <Typography variant="caption" textAlign="center" sx={{ opacity: 0.8 }}>
                        By clicking &quot;Generate Speech&quot; you agree to our&nbsp;
                        <Link href="#" color="primary">
                            Terms & Conditions
                        </Link>
                        .
                    </Typography>
                </Stack>
                {/*
        <Box
          id="image"
          sx={(theme) => ({
            mt: { xs: 8, sm: 10 },
            alignSelf: 'center',
            height: { xs: 200, sm: 700 },
            width: '100%',
            backgroundImage:
              theme.palette.mode === 'light'
                ? 'url("/static/images/templates/templates-images/hero-light.png")'
                : 'url("/static/images/templates/templates-images/hero-dark.png")',
            backgroundSize: 'cover',
            borderRadius: '10px',
            outline: '1px solid',
            outlineColor:
              theme.palette.mode === 'light'
                ? alpha('#BFCCD9', 0.5)
                : alpha('#9CCCFC', 0.1),
            boxShadow:
              theme.palette.mode === 'light'
                ? `0 0 12px 8px ${alpha('#9CCCFC', 0.2)}`
                : `0 0 24px 12px ${alpha('#033363', 0.2)}`,
          })}
        />*/}
            </Container>
        </Box>
    );
}
