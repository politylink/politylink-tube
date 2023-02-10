import * as React from 'react'
import {graphql} from 'gatsby'
import Transcript from "../../components/transcript";

const ClipPage = ({data}) => {
    return (
        <div>
            <p>{data.clipJson.video.url}</p>
            <Transcript
                utterances={data.clipJson.transcript.utterances}
                updateTime={console.log}
            />
        </div>
    )
}

export const query = graphql`
    query ($id: String) {
        clipJson (id: {eq:$id}) {
            clipId
            video {
                url
            }
            transcript {
                utterances {
                    start
                    end
                    words {
                        start
                        end
                        text
                    }
                }
            }
        }   
    }
`

export default ClipPage