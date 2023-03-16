export const buildClipUrl = (clipId) => {
  return `/clip/${clipId}`;
};

export const buildImageUrl = (path) => {
  return `https://image.politylink.jp/player${path}`;
};

export const buildClipImageUrl = (clipId, size = "m") => {
  return buildImageUrl(`/clip/${size}/${clipId}.jpg`);
};

export const buildAbsoluteUrl = (path) => {
  return `https://politylink.jp${path}`;
};
