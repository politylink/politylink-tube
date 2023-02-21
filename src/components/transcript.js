import React, {PureComponent} from 'react';
import TranscriptUtterance from "./transcriptUtterance";
import Box from "@mui/material/Box";

class Transcript extends PureComponent {
    render() {
        return (
            <Box sx={{
                backgroundColor: 'white',
                overflow: 'scroll',
                paddingX: 3,
                maxHeight: '100%',
            }} onScroll={this.props.onScroll}>
                {this.props.utterances.map(({start, end, words}, i) => (
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

export default Transcript;
