import * as React from "react";
import {Button, createTheme, ThemeProvider} from "@mui/material";
import Box from "@mui/material/Box";
import TvIcon from "@mui/icons-material/Tv";
import NotesIcon from "@mui/icons-material/Notes";
import Slider from "@mui/material/Slider";
import {formatTime} from "../utils/timeUtils";
import IconButton from "@mui/material/IconButton";
import {Forward30, Replay30} from "@mui/icons-material";
import PlayArrowRounded from "@mui/icons-material/PlayArrowRounded";
import PauseRounded from "@mui/icons-material/PauseRounded";
import {styled} from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import {BottomPaper} from "../layout/bottomPaper";


const TinyText = styled(Typography)({
    fontSize: '0.75rem',
    opacity: 0.38,
    fontWeight: 500,
    letterSpacing: 0.2,
});

const theme = createTheme({
    palette: {
        basic: {
            main: 'rgba(0,0,0,0.87)'
        }
    }
});


const AppBottomController = (
    {
        isLeft, switchLeft, switchRight,
        currentTime, duration, isPaused, updateTime, startPlayer, stopPlayer
    }
) => {
    return (
        <ThemeProvider theme={theme}>
            <BottomPaper sx={{padding: {xs: 1, sm: 1, md: 2}, backgroundColor: '#f3f2ef'}} elevation={3}>
                <Box sx={{
                    display: {xs: 'flex', sm: 'flex', md: 'none'},
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <Button variant={isLeft ? 'outlined' : 'text'} startIcon={<TvIcon/>}
                            color='basic' sx={{margin: '5px', borderRadius: '10px'}}
                            onClick={switchLeft}>動画</Button>
                    <Button variant={isLeft ? 'text' : 'outlined'} startIcon={<NotesIcon/>}
                            color='basic' sx={{margin: '5px', borderRadius: '10px'}}
                            onClick={switchRight}>文字起こし</Button>
                </Box>
                <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexDirection: 'column',
                    width: '90%',
                    maxWidth: '800px',
                    margin: 'auto'
                }}>
                    <Slider
                        aria-label='time-indicator'
                        value={currentTime}
                        min={0}
                        step={1}
                        max={duration}
                        onChange={(_, value) => updateTime(value)}
                        color='primary'
                        sx={{
                            color: 'rgba(0,0,0,0.87)',
                            margin: 'auto',
                            width: '95%'
                        }}
                    />
                    <Box sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        margin: '-2px 0 0 0',
                        width: '100%'
                    }}>
                        <TinyText>{formatTime(currentTime)}</TinyText>
                        <TinyText>-{formatTime(duration - currentTime)}</TinyText>
                    </Box>
                </Box>
                <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '-30px 0 0 0'
                }}>
                    <IconButton aria-label='replay 30s' onClick={() => updateTime(currentTime - 30)}>
                        <Replay30 color='basic' fontSize='large'/>
                    </IconButton>
                    {isPaused ?
                        <IconButton aria-label='play' onClick={startPlayer}>
                            <PlayArrowRounded color='basic' sx={{fontSize: '3rem'}}/>
                        </IconButton> :
                        <IconButton aria-label='pause' onClick={stopPlayer}>
                            <PauseRounded color='basic' sx={{fontSize: '3rem'}}/>
                        </IconButton>
                    }
                    <IconButton aria-label='skip 30s' onClick={() => updateTime(currentTime + 30)}>
                        <Forward30 color='basic' fontSize='large'/>
                    </IconButton>
                </Box>
            </BottomPaper>
        </ThemeProvider>
    );
};

export default AppBottomController;