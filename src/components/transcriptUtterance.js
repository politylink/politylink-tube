import React, {PureComponent} from 'react';
import {formatTime} from "../utils/timeUtils";
import TranscriptWord from "./transcriptWord";
import * as styles from './transcriptUtterance.module.css';

class TranscriptUtterance extends PureComponent {
    render() {
        return (
            <div data-start={this.props.start} data-end={this.props.end} className={styles.container}>
                <p className={styles.time}>
                    {formatTime(this.props.start)}
                </p>
                <div className={styles.words}>
                    {this.props.words.map(({start, end, text}, i) => (
                        <TranscriptWord
                            key={i}
                            start={start}
                            end={end}
                            text={text}
                            updateTime={this.props.updateTime}
                        />
                    ))}
                </div>
            </div>
        );
    }
}

export default TranscriptUtterance;
