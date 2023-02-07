import * as React from 'react';
import {useEffect, useRef, useState} from 'react';
import 'react-tabs/style/react-tabs.css';
import * as styles from './tab.module.css';
import Transcript from '../components/transcript';
import videojs from 'video.js';
import {editWordNodeClass, eqWordPosition, findActiveWordPosition, genTestWords} from '../utils/transcriptUtils';
import {videoJsOptions} from '../utils/videoUtils';
import ControlPanel from '../components/controlPanel';

const TabPage = () => {
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPaused, setIsPaused] = useState(true);
    const [isTranscript, setIsTranscript] = useState(false);

    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const transcriptRef = useRef(null);
    const activeWordPositionRef = useRef(null);
    const words = genTestWords(3000); // TODO: change to structured

    useEffect(() => {
        if (!playerRef.current) {
            const videoElement = document.createElement('video-js');
            videoElement.classList.add('vjs-big-play-centered');
            videoRef.current.appendChild(videoElement);
            playerRef.current = videojs(videoElement, videoJsOptions, onReady);
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
            }
        };
        playerRef.current.on('timeupdate', onTimeUpdate);
        return () => playerRef.current.off('timeupdate', onTimeUpdate);
    }

    const updateTime = (time) => {
        setCurrentTime(time);
        playerRef.current.currentTime(time);
    }

    const startPlayer = () => {
        setIsPaused(false);
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
                <div className={styles.transcript}>
                    <div className={styles.transcripts} ref={transcriptRef}>
                        <Transcript
                            words={words.slice(0, 100)}
                            onWordClick={updateTime}
                        />
                        <Transcript
                            words={words.slice(100)}
                            onWordClick={updateTime}
                        />
                    </div>
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

export default TabPage;