import React, { PureComponent } from "react";
import TranscriptUtterance from "./transcriptUtterance";
import Box from "@mui/material/Box";

class TranscriptPanel extends PureComponent {
  render() {
    return (
      <Box
        sx={{
          paddingX: { xs: 3, sm: 3, md: 5 },
          paddingBottom: 12, // safeguard to avoid footer overlap
        }}
      >
        {this.props.utterances.map(({ start, end, words }, i) => (
          <TranscriptUtterance
            key={i}
            start={start}
            end={end}
            words={words}
            updateTime={this.props.updateTime}
          />
        ))}
      </Box>
    );
  }
}

export default TranscriptPanel;
