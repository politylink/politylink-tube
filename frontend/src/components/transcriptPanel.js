import React, {PureComponent} from 'react';
import TranscriptUtterance from "./transcriptUtterance";
import Box from "@mui/material/Box";

class TranscriptPanel extends PureComponent {
    render() {
        return (
            <Box sx={{
                paddingX: {xs: 3, sm: 3, md: 5},
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
                {/* safeguard to avoid footer overlap. need to mimic TranscriptUtterance DOM structure (2 child nodes) for transcriptUtil.js */}
                <Box sx={{height: '100px'}}>
                    <div/>
                    <div/>
                </Box>
            </Box>
        );
    }
}

export default TranscriptPanel;
