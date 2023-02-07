/***
 WARNING: these methods are heavily dependent on the DOM structure produced by the transcript components.
 I'm not sure if this is the best approach.
 ***/


export const findActiveWordPosition = (transcriptRoot, time) => {
    const transcriptNodes = transcriptRoot.childNodes;
    for (const [tid, transcript] of transcriptNodes.entries()) {
        const wordNodes = transcript.childNodes[1].childNodes;
        for (const [wid, word] of wordNodes.entries()) {
            if (word.getAttribute('data-start') >= time) {
                return [tid, wid];
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
    const transcriptNodes = transcriptRoot.childNodes;
    const [tid, wid] = wordPosition;
    return transcriptNodes[tid].childNodes[1].childNodes[wid];
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