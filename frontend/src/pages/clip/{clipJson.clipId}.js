import * as React from 'react'
import {useEffect, useRef, useState} from 'react'
import {graphql} from 'gatsby'
import * as wordStyles from '../../components/transcriptWord.module.css';
import videojs from 'video.js';
import {editWordNodeClass, eqWordPosition, findActiveWordPosition, scrollToWord} from '../../utils/transcriptUtils';
import {getVideojsOptions} from '../../utils/videoUtils';
import AppBottomController from "../../components/appBottomController";
import AppTopBar from "../../components/appTopBar";
import {Toolbar, useMediaQuery, useTheme} from "@mui/material";
import Box from "@mui/material/Box";
import SEO from "../../components/seo";
import {buildClipPageDescription, buildClipPageTitle} from "../../utils/seoUtils";
import TranscriptPanel from "../../components/transcriptPanel";
import VideoInfoPanel from "../../components/videoInfoPanel";
import {buildClipImageUrl} from "../../utils/urlUtils";


const ClipPage = ({data}) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPaused, setIsPaused] = useState(true);
    const [isLeft, setIsLeft] = useState(true);

    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const transcriptRef = useRef(null);
    const activeWordPositionRef = useRef(null);
    const isAutoScrollRef = useRef(true);

    useEffect(() => {
        if (!playerRef.current) {
            const videoElement = document.createElement('video-js');
            videoElement.classList.add('vjs-big-play-centered');
            videoRef.current.appendChild(videoElement);
            playerRef.current = videojs(videoElement, getVideojsOptions(data.clipJson.video.url), onReady);
            videoRef.current.childNodes[0].childNodes[0].setAttribute('playsinline', '');
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
            highlightTranscript(currentTime);
        };
        playerRef.current.on('timeupdate', onTimeUpdate);
        return () => playerRef.current.off('timeupdate', onTimeUpdate);
    }

    const highlightTranscript = (currentTime) => {
        let activeWordPosition = findActiveWordPosition(transcriptRef.current, currentTime);
        if (!eqWordPosition(activeWordPosition, activeWordPositionRef.current)) {
            editWordNodeClass(transcriptRef.current, activeWordPosition, wordStyles.active);
            editWordNodeClass(transcriptRef.current, activeWordPositionRef.current, wordStyles.active, false);
            activeWordPositionRef.current = activeWordPosition;
            if (isAutoScrollRef.current) {
                scrollToWord(transcriptRef.current, activeWordPositionRef.current);
            }
        }
    }

    const updateTime = (time) => {
        setCurrentTime(time);
        highlightTranscript(time);
        playerRef.current.currentTime(time);

    }

    const updateTimeWithScroll = (time) => {
        isAutoScrollRef.current = true;
        updateTime(time);
    }

    const updateTimeWithoutScroll = (time) => {
        isAutoScrollRef.current = false;
        updateTime(time);
    }

    const startPlayer = () => {
        setIsPaused(false);
        isAutoScrollRef.current = true; // TODO: trigger immediate scroll?
        highlightTranscript(currentTime);
        playerRef.current.play();
    }

    const stopPlayer = () => {
        setIsPaused(true);
        playerRef.current.pause();
    }

    return (
        <Box sx={{height: '100vh', overflowX: 'hidden'}}>
            <AppTopBar/>
            <Toolbar variant='dense'/>
            <Box sx={{
                width: isMobile ? '200%' : '100%',
                display: 'flex',
                transform: (isMobile && !isLeft) ? 'translateX(-50%)' : 'translateX(0)',
                height: isMobile ? 'calc(100vh - 250px)' : 'calc(100vh - 200px)', // TODO: fix hardcoded AppBar + BottomController height
                transitionDuration: '0.1s',
            }}>
                <Box sx={{
                    width: '50%',
                    marginX: 'auto',
                    overflowX: 'scroll',
                    height: '100%',
                    paddingBottom: 6,
                }}>
                    <Box ref={videoRef} sx={{
                        maxWidth: '800px',
                        margin: 'auto'
                    }}></Box>
                    <VideoInfoPanel
                        title={data.clipJson.title}
                        date={data.clipJson.video.date}
                        duration={data.clipJson.video.duration}
                        pageUrl={data.clipJson.video.page}
                        annotations={data.clipJson.annotations}
                        updateTime={updateTimeWithScroll}
                    />
                </Box>
                <Box sx={{
                    width: '50%',
                    backgroundColor: 'white',
                    overflowX: 'scroll',
                    paddingY: 3,
                    height: '100%',
                }}
                     onScroll={() => {
                         isAutoScrollRef.current = false;
                     }}
                     ref={transcriptRef}>
                    <TranscriptPanel
                        utterances={data.clipJson.transcript.utterances}
                        updateTime={updateTimeWithoutScroll}
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
                updateTime={updateTimeWithScroll}
                startPlayer={startPlayer}
                stopPlayer={stopPlayer}
            />
        </Box>
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
                page
                date
                duration
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
            annotations {
                start
                time
                text
            }
        }   
    }
`

export const Head = ({location, data}) => {
    const clip = data.clipJson
    return (
        <SEO
            path={location.pathname}
            title={buildClipPageTitle(clip.title)}
            description={buildClipPageDescription(clip.title, clip.video.date)}
            imageUrl={buildClipImageUrl(clip.clipId, 'l')}
            twitterCard={'summary_large_image'}
        />
    )
}

