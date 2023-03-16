import * as React from "react";
import { Button, createTheme, ThemeProvider } from "@mui/material";
import Box from "@mui/material/Box";
import TvIcon from "@mui/icons-material/Tv";
import NotesIcon from "@mui/icons-material/Notes";
import Slider from "@mui/material/Slider";
import { formatTime } from "../utils/timeUtils";
import IconButton from "@mui/material/IconButton";
import { Forward30, Replay30 } from "@mui/icons-material";
import { BottomPaper } from "../layout/bottomPaper";
import TinyText from "../layout/tinyText";
import PlayCircleIcon from "@mui/icons-material/PlayCircle";
import PauseCircleIcon from "@mui/icons-material/PauseCircle";

const theme = createTheme({
  palette: {
    basic: {
      main: "rgba(0,0,0,0.87)",
    },
  },
});

const AppBottomController = ({
  isLeft,
  switchLeft,
  switchRight,
  currentTime,
  duration,
  isPaused,
  updateTime,
  startPlayer,
  stopPlayer,
}) => {
  return (
    <ThemeProvider theme={theme}>
      <BottomPaper
        sx={{ padding: { xs: 1, sm: 1, md: 2 }, backgroundColor: "white" }}
        elevation={3}
      >
        <Box
          sx={{
            display: { xs: "flex", sm: "flex", md: "none" },
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Button
            variant={isLeft ? "outlined" : "text"}
            startIcon={<TvIcon />}
            color="basic"
            sx={{ margin: "5px", borderRadius: "10px" }}
            onClick={switchLeft}
          >
            動画
          </Button>
          <Button
            variant={isLeft ? "text" : "outlined"}
            startIcon={<NotesIcon />}
            color="basic"
            sx={{ margin: "5px", borderRadius: "10px" }}
            onClick={switchRight}
          >
            文字起こし
          </Button>
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            width: "90%",
            maxWidth: "800px",
            margin: "auto",
          }}
        >
          <Slider
            aria-label="time-indicator"
            value={currentTime}
            min={0}
            step={1}
            max={duration}
            onChange={(_, value) => updateTime(value)}
            color="primary"
            sx={{
              margin: "auto",
              width: "95%",
            }}
          />
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              margin: "-2px 0 0 0",
              width: "100%",
            }}
          >
            <TinyText>{formatTime(currentTime)}</TinyText>
            <TinyText>-{formatTime(duration - currentTime)}</TinyText>
          </Box>
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            margin: "-30px 0 -10px 0",
          }}
        >
          <IconButton
            aria-label="replay 30s"
            onClick={() => updateTime(currentTime - 30)}
          >
            <Replay30 color="basic" fontSize="large" />
          </IconButton>
          {isPaused ? (
            <IconButton aria-label="play" onClick={startPlayer}>
              <PlayCircleIcon color="primary" sx={{ fontSize: "4rem" }} />
            </IconButton>
          ) : (
            <IconButton aria-label="pause" onClick={stopPlayer}>
              <PauseCircleIcon color="primary" sx={{ fontSize: "4rem" }} />
            </IconButton>
          )}
          <IconButton
            aria-label="skip 30s"
            onClick={() => updateTime(currentTime + 30)}
          >
            <Forward30 color="basic" fontSize="large" />
          </IconButton>
        </Box>
      </BottomPaper>
    </ThemeProvider>
  );
};

export default AppBottomController;
