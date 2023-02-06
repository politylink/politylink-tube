import * as React from "react"
import {useEffect, useRef, useState} from "react"
import 'react-tabs/style/react-tabs.css';
import * as styles from './tab.module.css';
import Transcript from "../components/transcript";
import videojs from "video.js";
import {editWordNodeClass, eqWordPosition, findActiveWordPosition, genTestWords} from "../utils/transcriptUtils";
import {videoJsOptions} from "../utils/videoUtils";

const TabPage = () => {
    const [isLeft, setIsLeft] = useState(true);
    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const transcriptRef = useRef(null);
    const activeWordPositionRef = useRef(null);
    const words = genTestWords(300);

    const toggleIsLeft = () => {
        setIsLeft((x) => !x);
    }

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
            const time = playerRef.current.currentTime();
            let activeWordPosition = findActiveWordPosition(transcriptRef.current, time);
            if (!eqWordPosition(activeWordPosition, activeWordPositionRef.current)) {
                editWordNodeClass(transcriptRef.current, activeWordPosition, styles.activeWord);
                editWordNodeClass(transcriptRef.current, activeWordPositionRef.current, styles.activeWord, false);
                activeWordPositionRef.current = activeWordPosition;
            }
        };
        playerRef.current.on('timeupdate', onTimeUpdate);
        return () => playerRef.current.off('timeupdate', onTimeUpdate);
    }

    const seekPlayer = (time) => {
        playerRef.current.currentTime(time);
    }

    let mainStyle = isLeft ? {transform: `translateX(0)`} : {transform: `translateX(-50%)`}
    return (
        <div className={styles.panel}>
            <div className={styles.header}>
                <p>header</p>
            </div>
            <div className={styles.main} style={mainStyle}>
                <div className={styles.left}>
                    <p>panel1</p>
                    <div ref={videoRef}/>
                </div>
                <div className={styles.right}>
                    <p>panel2</p>
                    <div className={styles.transcripts} ref={transcriptRef}>
                        <Transcript
                            words={words.slice(0, 100)}
                            onWordClick={seekPlayer}
                        />
                        <Transcript
                            words={words.slice(100, 200)}
                            onWordClick={seekPlayer}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.footer}>
                <button type="button" onClick={toggleIsLeft}>toggle</button>
            </div>
        </div>
    );
};

export default TabPage;