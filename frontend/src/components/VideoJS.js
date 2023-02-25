import React from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';


export const VideoJS = (props) => {
    const videoRef = React.useRef(null);
    const playerRef = React.useRef(null);
    const {options, onReady} = props;

    React.useEffect(() => {

        // Make sure Video.js player is only initialized once
        if (!playerRef.current) {
            // The Video.js player needs to be _inside_ the component el for React 18 Strict Mode.
            const videoElement = document.createElement("video-js");

            videoElement.classList.add('vjs-big-play-centered');
            videoRef.current.appendChild(videoElement);

            const player = playerRef.current = videojs(videoElement, options, () => {
                videojs.log('player is ready');
                onReady && onReady(player);
            });
            var Button  = videojs.getComponent('Button');
            var button = new Button(player, {
                clickHandler: function(event) {
                    videojs.log('clicked');
                }
            });
            button.controlText('MyButton');
            button.addClass('vjs-visible-text');
            player.getChild('ControlBar').addChild(button);

            // You could update an existing player in the `else` block here
            // on prop change, for example:
        } else {
            const player = playerRef.current;

            player.autoplay(options.autoplay);
            player.src(options.sources);
        }
    }, [options, videoRef]);

    // Dispose the Video.js player when the functional component unmounts
    React.useEffect(() => {
        const player = playerRef.current;

        return () => {
            if (player && !player.isDisposed()) {
                player.dispose();
                playerRef.current = null;
            }
        };
    }, [playerRef]);

    const handleClickSkip = () => {
        console.log(playerRef.current.currentTime());
        playerRef.current.currentTime(playerRef.current.currentTime() + 30);
    }

    const handleSkipInput = (event) => {
        playerRef.current.currentTime(event.target.value);
    }

    return (
        <div data-vjs-player>
            <div ref={videoRef}/>
            <button onClick={handleClickSkip}>Skip</button>
            <input
                type="text"
                placeholder={"再生時間を入力"}
                onChange={handleSkipInput}
                style={{width: '50px'}}
            />
        </div>
    );
};

export default VideoJS;