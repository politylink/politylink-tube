import * as React from "react"
import HomeLayout from "../layout/homeLayout";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import VideoCard from "../components/videoCard";
import {graphql} from 'gatsby'
import {buildClipImageUrl, buildClipUrl} from "../utils/urlUtils";


const IndexPage = ({data}) => {
    const clips = data.allClipJson.nodes;
    return (
        <HomeLayout value={0}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Grid container spacing={1}>
                    {
                        clips.map(clip => (
                            <VideoCard
                                key={clip.clipId}
                                clipUrl={buildClipUrl(clip.clipId)}
                                imageUrl={buildClipImageUrl(clip.clipId)}
                                title={clip.title}
                                date={clip.video.date}
                                duration={clip.video.duration}
                            />
                        ))
                    }
                </Grid>
            </Container>
        </HomeLayout>
    )
}


export const query = graphql`
  query {
    allClipJson (sort: {video: {date: DESC}}) {
      nodes {
        clipId
        title
        video {
          url
          date
          duration
        }
      }
    }
  }
`


export default IndexPage;