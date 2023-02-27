import * as React from "react"
import Container from "@mui/material/Container";
import HomeLayout from "../layout/homeLayout";
import {Alert} from "@mui/material";
import SEO from "../components/seo";


const SpeakerPage = () => {
    return (
        <HomeLayout value={2}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Alert severity="info">このページには議員ごとに分けられた短編動画が追加される予定です。</Alert>
            </Container>
        </HomeLayout>
    );
};

export default SpeakerPage;

export const Head = ({location}) => {
    return (
        <SEO
            path={location.pathname}
        />
    )
}
