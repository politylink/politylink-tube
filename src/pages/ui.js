import * as React from 'react';
import {styled} from '@mui/material/styles';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Slider from '@mui/material/Slider';
import IconButton from '@mui/material/IconButton';
import PauseRounded from '@mui/icons-material/PauseRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import {Forward30, Replay30} from "@mui/icons-material";
import {formatTime} from "../utils/timeUtils";
import ControlPanel from "../components/controlPanel";


const TinyText = styled(Typography)({
    fontSize: '0.75rem',
    opacity: 0.38,
    fontWeight: 500,
    letterSpacing: 0.2,
});

export default function MusicPlayerSlider() {
    const duration = 4000; // seconds
    const [position, setPosition] = React.useState(32);
    const [paused, setPaused] = React.useState(false);

    const updateTime = (time) => {
        setPosition(Math.min(Math.max(0, time), duration));
    }

    const startPlayer = () => {
        setPaused(false);
    }

    const stopPlayer = () => {
        setPaused(true);
    }

    const mainIconColor = '#000';
    return (
        <Box sx={{width: '80%', overflow: 'hidden', margin: 'auto'}}>
            <Slider
                aria-label="time-indicator"
                value={position}
                min={0}
                step={1}
                max={duration}
                onChange={(_, value) => setPosition(value)}
                sx={{
                    margin: '10px',
                    color: 'rgba(0,0,0,0.87)',
                }}
            />
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mt: -2,
                }}
            >
                <TinyText>{formatTime(position)}</TinyText>
                <TinyText>-{formatTime(duration - position)}</TinyText>
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mt: -1,
                }}
            >
                <IconButton aria-label="replay 30s">
                    <Replay30 fontSize="large" htmlColor={mainIconColor}/>
                </IconButton>
                <IconButton
                    aria-label={paused ? 'play' : 'pause'}
                    onClick={() => setPaused(!paused)}
                >
                    {paused ? (
                        <PlayArrowRounded
                            sx={{fontSize: '3rem'}}
                            htmlColor={mainIconColor}
                        />
                    ) : (
                        <PauseRounded sx={{fontSize: '3rem'}} htmlColor={mainIconColor}/>
                    )}
                </IconButton>
                <IconButton aria-label="skip 30s">
                    <Forward30 fontSize="large" htmlColor={mainIconColor}/>
                </IconButton>
            </Box>
            <ControlPanel
                duration={duration}
                currentTime={position}
                isPaused={paused}
                updateTime={updateTime}
                startPlayer={startPlayer}
                stopPlayer={stopPlayer}
            />
        </Box>
    );
}