export const buildClipUrl = (clipId) => {
    return `/clip/${clipId}`
}

export const buildClipImageUrl = (clipId) => {
    return `https://image.politylink.jp/player/clip/m/${clipId}.jpg`
}

export const buildAbsoluteUrl = (path) => {
    return `https://politylink.jp${path}`
}
