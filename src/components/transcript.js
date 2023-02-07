import React from 'react';
import * as styles from './transcript.module.css';

const Transcript = ({words, onWordClick}) => {
    return (
        <div data-start={0} data-end={100}>
            <p>time</p>
            <div className={styles.words}>
                {words.map(({startTime, text}, i) =>
                    <span key={i} className={'Word'} data-start={startTime} onClick={() => onWordClick(startTime)}>{text}</span>
                )}
            </div>
        </div>
    )
};

export default Transcript;
