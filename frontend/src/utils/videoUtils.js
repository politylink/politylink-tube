export const getVideojsOptions = (videoUrl) => {
    return {
        autoplay: false,
        controls: true,
        responsive: true,
        fluid: true,
        playbackRates: [0.5, 1, 1.5, 2],
        language: 'ja',
        sources: [{
            src: videoUrl,
            type: 'application/x-mpegURL'
        }],
        html5: {
            vhs: {
                overrideNative: true
            },
            nativeAudioTracks: false,
            nativeVideoTracks: false
        }
    };
}

export const videojsOptions = getVideojsOptions(
    'https://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2022/2022-1222-0850-13/playlist.m3u8'
)