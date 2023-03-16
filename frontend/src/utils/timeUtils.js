export const formatTime = (value) => {
  let second = parseInt(value);
  const hour = Math.floor(second / 3600);
  second -= hour * 3600;
  const minute = Math.floor(second / 60);
  second -= minute * 60;

  if (hour > 0) {
    return `${hour}:${zeroPad2(minute)}:${zeroPad2(second)}`;
  } else {
    return `${minute}:${zeroPad2(second)}`;
  }
};

export const zeroPad2 = (value) => {
  return value.toString().padStart(2, "0");
};
