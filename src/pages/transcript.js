import * as React from "react"
import {useEffect, useRef, useState} from "react"
import * as styles from './transcript.module.css';
import videojs from "video.js";
import Transcript from "../components/transcript";

const TranscriptPage = () => {
    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const transcriptRef = useRef(null);
    const activeWordPositionRef = useRef(null);

    const words = Array.from({length: 5000},
        (v, k) => {
            return {'startTime': k, 'text': `word${k}`}
        });

    useEffect(() => {
        if (!playerRef.current) {
            const options = {
                autoplay: false,
                controls: true,
                responsive: true,
                fluid: true,
                playbackRates: [0.5, 1, 1.5, 2],
                language: 'ja',
                liveui: true,
                sources: [{
                    src: 'https://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2022/2022-1222-0850-13/playlist.m3u8',
                    type: 'application/x-mpegURL'
                }]
            };
            const videoElement = document.createElement("video-js");
            videoElement.classList.add('vjs-big-play-centered');
            videoRef.current.appendChild(videoElement);
            playerRef.current = videojs(videoElement, options, onReady);
        }
    }, [videoRef]);

    const onReady = () => {
        console.log('onReady');
        console.log(playerRef.current);
        const onTimeUpdate = () => {
            const time = playerRef.current.currentTime();
            for (const [tid, transcript] of transcriptRef.current.childNodes.entries()) {
                // TODO: check if target word is in this block
                for (const [wid, word] of transcript.childNodes[1].childNodes.entries()) { // TODO: avoid hard-coding words index (=1)
                    if (word.getAttribute('data-start') >= time) {
                        word.classList.add(styles.activeWord);
                        if (activeWordPositionRef.current) {
                            const [_tid, _wid] = activeWordPositionRef.current;
                            if (_tid !== tid || _wid !== wid) {
                                const _word = transcriptRef.current.childNodes[_tid].childNodes[1].childNodes[_wid];
                                _word.classList.remove(styles.activeWord);
                            }
                        }
                        activeWordPositionRef.current = [tid, wid];
                        break;
                    }
                }
            }
        };
        playerRef.current.on("timeupdate", onTimeUpdate);
        return () => playerRef.current.off("timeupdate", onTimeUpdate);
    }

    const seekPlayer = (time) => {
        playerRef.current.currentTime(time);
    }

    return (
        <div>
            <p>Transcript</p>
            <div ref={videoRef}/>
            <div ref={transcriptRef}>
                <Transcript
                    words={words}
                    onWordClick={seekPlayer}
                />
                <Transcript
                    words={words}
                    onWordClick={seekPlayer}
                />
            </div>
        </div>
    )
}

export default TranscriptPage