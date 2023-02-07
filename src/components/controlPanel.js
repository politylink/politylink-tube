import * as React from 'react';
import {styled} from '@mui/material/styles';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Slider from '@mui/material/Slider';
import IconButton from '@mui/material/IconButton';
import PauseRounded from '@mui/icons-material/PauseRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import {Forward30, Replay30} from '@mui/icons-material';
import {formatTime} from '../utils/timeUtils';
import {Button} from "@mui/material";
import TvIcon from '@mui/icons-material/Tv';
import NotesIcon from '@mui/icons-material/Notes';
import * as styles from './controlPanel.module.css';


const TinyText = styled(Typography)({
    fontSize: '0.75rem',
    opacity: 0.38,
    fontWeight: 500,
    letterSpacing: 0.2,
});
const mainIconColor = '#000';

const ControlPanel = ({
                          currentTime, duration, isPaused, isTranscript, updateTime, startPlayer, stopPlayer, showMovie,
                          showTranscript
                      }) => {
    return (
        <Box className={styles.panel}>
            <Box className={styles.tabBox}>
                <Button variant={isTranscript ? 'text' : 'outlined'} startIcon={<TvIcon/>}
                        sx={{margin: '5px', borderRadius: '10px'}} onClick={showMovie}>動画</Button>
                <Button variant={isTranscript ? 'outlined' : 'text'} startIcon={<NotesIcon/>}
                        sx={{margin: '5px', borderRadius: '10px'}} onClick={showTranscript}>文字起こし</Button>
            </Box>
            <Box className={styles.sliderBox}>
                <Slider
                    aria-label='time-indicator'
                    value={currentTime}
                    min={0}
                    step={1}
                    max={duration}
                    onChange={(_, value) => updateTime(value)}
                    sx={{color: 'rgba(0,0,0,0.87)'}}
                    className={styles.slider}
                />
            </Box>
            <Box className={styles.timeBox}>
                <TinyText>{formatTime(currentTime)}</TinyText>
                <TinyText>-{formatTime(duration - currentTime)}</TinyText>
            </Box>
            <Box className={styles.playerBox}>
                <IconButton aria-label='replay 30s' onClick={() => updateTime(currentTime - 30)}>
                    <Replay30 fontSize='large' htmlColor={mainIconColor}/>
                </IconButton>
                <IconButton
                    aria-label={isPaused ? 'play' : 'pause'}
                    onClick={() => isPaused ? startPlayer() : stopPlayer()}
                >
                    {isPaused ? (
                        <PlayArrowRounded
                            sx={{fontSize: '3rem'}}
                            htmlColor={mainIconColor}
                        />
                    ) : (
                        <PauseRounded sx={{fontSize: '3rem'}} htmlColor={mainIconColor}/>
                    )}
                </IconButton>
                <IconButton aria-label='skip 30s' onClick={() => updateTime(currentTime + 30)}>
                    <Forward30 fontSize='large' htmlColor={mainIconColor}/>
                </IconButton>
            </Box>
        </Box>
    );
}

export default ControlPanel;
