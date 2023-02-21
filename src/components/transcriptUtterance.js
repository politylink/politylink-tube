import React, {PureComponent} from 'react';
import {formatTime} from "../utils/timeUtils";
import TranscriptWord from "./transcriptWord";
import Box from "@mui/material/Box";
import TinyText from "./tinyText";

class TranscriptUtterance extends PureComponent {
    render() {
        return (
            <Box data-start={this.props.start} data-end={this.props.end} sx={{margin: 1}}>
                <TinyText>
                    {formatTime(this.props.start)}
                </TinyText>
                <Box>
                    {this.props.words.map(({start, end, text}, i) => (
                        <TranscriptWord
                            key={i}
                            start={start}
                            end={end}
                            text={text}
                            updateTime={this.props.updateTime}
                        />
                    ))}
                </Box>
            </Box>
        );
    }
}

export default TranscriptUtterance;
