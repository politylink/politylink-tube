import * as React from "react"
import HomeLayout from "../layout/homeLayout";
import Container from "@mui/material/Container";
import {Alert} from "@mui/material";


const TopicPage = () => {
    return (
        <HomeLayout value={1}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Alert severity="info">このページにはトピックごとに分けられた短編動画が追加される予定です。</Alert>
            </Container>
        </HomeLayout>
    )
}

export default TopicPage;