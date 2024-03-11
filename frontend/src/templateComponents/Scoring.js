import * as React from 'react';
import { useState, useRef } from "react";
import { Container, Grid, Typography, TextField, Button, Stack, Link } from '@mui/material';

const Scoring = () => {
    const groundTruthText = useRef(null);
    const answerText = useRef(null);

    const [score, setScore] = useState(null);

    const handleGetScore = () => {

    }

    return (
        <Container id="Scoring" sx={{ py: { xs: 8, sm: 16 }, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
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
                    Scoring&nbsp;
                    <Typography
                        component="span"
                        variant="h1"
                        sx={{
                            color: (theme) =>
                                theme.palette.mode === 'light' ? 'primary.main' : 'primary.light',
                        }}
                    >
                        comparison
                    </Typography>
                </Typography>
            </Stack>
            <Grid container spacing={6} sx={{ mt: 1, mb: 1 }}>
                <Grid item xs={12} md={6}>
                    Ground Truth
                    <TextField
                        id="ground-truth-text-input"
                        label="Ground Truth"
                        multiline
                        rows={4}
                        sx={{ m: 1 }}
                        placeholder="Input your ground truth here."
                        inputRef={groundTruthText}
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12} md={6}>
                    Answer
                    <TextField
                        id="answer-text-input"
                        label="Answer"
                        multiline
                        rows={4}
                        sx={{ m: 1 }}
                        placeholder="Input your answer here."
                        inputRef={answerText}
                        fullWidth
                    />
                </Grid>
            </Grid>
            <Button variant="contained" color="primary" onClick={handleGetScore} type="button" sx={{ m: 1, width: { xs: '100%', sm: '50%' } }} >
                Get Score
            </Button>
            <Typography variant="caption" textAlign="center" sx={{ opacity: 0.8 }}>
                By clicking &quot;Get Score&quot; you agree to our&nbsp;
                <Link href="#" color="primary">
                    Terms & Conditions
                </Link>
                .
            </Typography>
        </Container>
    )
}

export default Scoring;