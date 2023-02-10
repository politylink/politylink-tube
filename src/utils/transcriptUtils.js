/***
 WARNING: these methods are heavily dependent on the DOM structure produced by the transcript components.
 I'm not sure if this is the best approach.
 ***/


export const findActiveWordPosition = (transcriptRoot, time) => {
    const utteranceNodes = transcriptRoot.childNodes[0].childNodes;
    for (const [uid, utterance] of utteranceNodes.entries()) {
        const wordNodes = utterance.childNodes[1].childNodes;
        for (const [wid, word] of wordNodes.entries()) {
            if (word.getAttribute('data-start') >= time) {
                return [uid, wid];
            }
        }
    }
    return null;
}

export const eqWordPosition = (p1, p2) => {
    if (p1 === null || p2 === null) {
        return false;
    }
    return p1[0] === p2[0] && p1[1] === p2[1];
}

export const getWordNode = (transcriptRoot, wordPosition) => {
    const utteranceNodes = transcriptRoot.childNodes[0].childNodes;
    const [uid, wid] = wordPosition;
    return utteranceNodes[uid].childNodes[1].childNodes[wid];
}

export const editWordNodeClass = (transcriptRoot, wordPosition, className, add = true) => {
    if (wordPosition === null) {
        return;
    }
    const node = getWordNode(transcriptRoot, wordPosition);
    if (add) {
        node.classList.add(className);
    } else {
        node.classList.remove(className);
    }
}

export const genTestWords = (length) => {
    return Array.from({length: length},
        (v, k) => {
            return {'startTime': k, 'text': `word${k}`}
        });
}

export const genTestTranscript = () => {
    return {
        'utterances': [
            {
                "start": 0,
                "end": 5,
                "words": [
                    {"start": 0, "end": 1, "text": "word1"},
                    {"start": 1, "end": 2, "text": "word2"},
                    {"start": 2, "end": 3, "text": "word3"},
                    {"start": 3, "end": 4, "text": "word4"},
                    {"start": 4, "end": 5, "text": "word5"}
                ]
            },
            {
                "start": 5,
                "end": 10,
                "words": [
                    {"start": 5, "end": 6, "text": "word6"},
                    {"start": 6, "end": 7, "text": "word7"},
                    {"start": 7, "end": 8, "text": "word8"},
                    {"start": 8, "end": 9, "text": "word9"},
                    {"start": 9, "end": 10, "text": "word10"}
                ]
            }
        ]
    }
}