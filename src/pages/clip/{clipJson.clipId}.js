import * as React from 'react'
import {useEffect, useRef, useState} from 'react'
import {graphql} from 'gatsby'
import Transcript from "../../components/transcript";
import * as styles from './clip.module.css';
import videojs from 'video.js';
import {editWordNodeClass, eqWordPosition, findActiveWordPosition, scrollToWord} from '../../utils/transcriptUtils';
import {getVideojsOptions} from '../../utils/videoUtils';
import AppBottomController from "../../components/appBottomController";
import AppTopBar from "../../components/appTopBar";
import {Toolbar, useMediaQuery, useTheme} from "@mui/material";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

const ClipPage = ({data}) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPaused, setIsPaused] = useState(true);
    const [isLeft, setIsLeft] = useState(true);
    const [isAutoScroll, setIsAutoScroll] = useState(true);

    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const transcriptRef = useRef(null);
    const activeWordPositionRef = useRef(null);

    useEffect(() => {
        if (!playerRef.current) {
            const videoElement = document.createElement('video-js');
            videoElement.classList.add('vjs-big-play-centered');
            videoRef.current.appendChild(videoElement);
            playerRef.current = videojs(videoElement, getVideojsOptions(data.clipJson.video.url), onReady);
        }
    }, [videoRef]);

    const onReady = () => {
        const onTimeUpdate = () => {
            const currentTime = playerRef.current.currentTime();
            const duration = playerRef.current.duration();
            const isPaused = playerRef.current.paused();
            setCurrentTime(currentTime);
            setDuration(duration);
            setIsPaused(isPaused);
            let activeWordPosition = findActiveWordPosition(transcriptRef.current, currentTime);
            if (!eqWordPosition(activeWordPosition, activeWordPositionRef.current)) {
                editWordNodeClass(transcriptRef.current, activeWordPosition, styles.activeWord);
                editWordNodeClass(transcriptRef.current, activeWordPositionRef.current, styles.activeWord, false);
                activeWordPositionRef.current = activeWordPosition;
                if (isAutoScroll) {
                    scrollToWord(transcriptRef.current, activeWordPositionRef.current);
                }
            }
        };
        playerRef.current.on('timeupdate', onTimeUpdate);
        return () => playerRef.current.off('timeupdate', onTimeUpdate);
    }

    const updateTime = (time) => {
        setCurrentTime(time);
        enableAutoScroll();
        playerRef.current.currentTime(time);
    }

    const startPlayer = () => {
        setIsPaused(false);
        enableAutoScroll();
        playerRef.current.play();
    }

    const stopPlayer = () => {
        setIsPaused(true);
        playerRef.current.pause();
    }

    const enableAutoScroll = () => {
        if (!isAutoScroll) {
            setIsAutoScroll(true);
            console.log('enabled auto scroll');
        }
    }

    const disableAutoScroll = () => {
        if (isAutoScroll) {
            setIsAutoScroll(false);
            console.log('disabled auto scroll');
        }
    }

    return (
        <div className={styles.panel}>
            <AppTopBar/>
            <Toolbar/>
            <Box sx={{
                width: isMobile ? '200%' : '100%',
                display: 'flex',
                transform: (isMobile && !isLeft) ? 'translateX(-50%)' : 'translateX(0)'
            }}>
                <Box sx={{width: "50%", padding: 2}}>
                    <Box ref={videoRef}></Box>
                    <Typography variant={'h5'} sx={{backgroundColor: 'white', marginTop: 2}}>
                        {data.clipJson.title}
                    </Typography>
                </Box>
                <Box sx={{width: "50%", padding: 2}} ref={transcriptRef}>
                    <Transcript
                        utterances={data.clipJson.transcript.utterances}
                        updateTime={updateTime}
                        onScroll={disableAutoScroll}
                    />
                </Box>
            </Box>
            <AppBottomController
                isLeft={isLeft}
                switchLeft={() => setIsLeft(true)}
                switchRight={() => setIsLeft(false)}
                currentTime={currentTime}
                duration={duration}
                isPaused={isPaused}
                updateTime={updateTime}
                startPlayer={startPlayer}
                stopPlayer={stopPlayer}
            />
        </div>
    );
};

export default ClipPage;


export const query = graphql`
    query ($id: String) {
        clipJson (id: {eq:$id}) {
            clipId
            title
            video {
                url
            }
            transcript {
                utterances {
                    start
                    end
                    words {
                        start
                        end
                        text
                    }
                }
            }
        }   
    }
`
