import * as React from 'react'
import {useEffect, useRef, useState} from 'react'
import {graphql} from 'gatsby'
import Transcript from "../../components/transcript";
import * as styles from './clip.module.css';
import videojs from 'video.js';
import {editWordNodeClass, eqWordPosition, findActiveWordPosition, scrollToWord} from '../../utils/transcriptUtils';
import {getVideojsOptions} from '../../utils/videoUtils';
import ControlPanel from '../../components/controlPanel';

const ClipPage = ({data}) => {
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPaused, setIsPaused] = useState(true);
    const [isTranscript, setIsTranscript] = useState(false);
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

    const showMovie = () => {
        setIsTranscript(false);
    }

    const showTranscript = () => {
        setIsTranscript(true);
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

    let mainStyle = isTranscript ? {transform: `translateX(-50%)`} : {transform: `translateX(0)`}
    return (
        <div className={styles.panel}>
            <div className={styles.header}>
                <p>header</p>
            </div>
            <div className={styles.main} style={mainStyle}>
                <div className={styles.movie}>
                    <div ref={videoRef}/>
                </div>
                <div className={styles.transcript} ref={transcriptRef}>
                    <Transcript
                        utterances={data.clipJson.transcript.utterances}
                        updateTime={updateTime}
                        onScroll={disableAutoScroll}
                    />
                </div>
            </div>
            <div className={styles.footer}>
                <ControlPanel
                    duration={duration}
                    currentTime={currentTime}
                    isPaused={isPaused}
                    isTranscript={isTranscript}
                    updateTime={updateTime}
                    startPlayer={startPlayer}
                    stopPlayer={stopPlayer}
                    showMovie={showMovie}
                    showTranscript={showTranscript}
                />
            </div>
        </div>
    );
};

export default ClipPage;


export const query = graphql`
    query ($id: String) {
        clipJson (id: {eq:$id}) {
            clipId
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
