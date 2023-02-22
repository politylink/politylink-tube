import * as React from "react"
import Container from "@mui/material/Container";
import HomeLayout from "../layout/homeLayout";
import {Alert} from "@mui/material";


const SpeakerPage = () => {
    return (
        <HomeLayout value={2}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Alert severity="info">このページには議員ごとに分割した短編動画が追加される予定です。</Alert>
            </Container>
        </HomeLayout>
    );
};

export default SpeakerPage;
