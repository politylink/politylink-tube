import * as React from "react"
import {useState} from "react"
import VideoJS from "../components/VideoJS";

const IndexPage = () => {
    const playerRef = React.useRef(null);
    const [url, setUrl] = useState('http://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2023/2023-0201-0900-01/playlist.m3u8')

    const handleUrlChange = (event) => {
        const value = event.target.value;
        console.log(value);
        setUrl(value);
    }

    const videoJsOptions = {
        autoplay: false,
        controls: true,
        responsive: true,
        fluid: true,
        playbackRates: [0.5, 1, 1.5, 2],
        language: 'ja',
        liveui: true,
        sources: [{
            src: url,
            type: 'application/x-mpegURL'
        }]
    }

    const handlePlayerReady = (player) => {
        playerRef.current = player;

        player.on('waiting', () => {
            console.log('player is waiting');
        });

        player.on('dispose', () => {
            console.log('player will dispose');
        })
    }

    return (
        <div>
            <p>Hello World!</p>
            <input
                type="text"
                placeholder={"URLを入力"}
                onChange={handleUrlChange}
                style={{width: '100%'}}
            />
            <VideoJS options={videoJsOptions} onReady={handlePlayerReady}/>
        </div>
    );
}

export default IndexPage

export const Head = () => (
    <>
        <title>Home Page</title>
        <link href="//vjs.zencdn.net/7.21.2/video-js.min.css" rel="stylesheet"/>
        <script src="//vjs.zencdn.net/7.21.2/video.min.js"></script>
    </>
)
