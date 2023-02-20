import * as React from "react"
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import VideoCard from "../components/VideoCard";
import HomeLayout from "../layout/homeLayout";


const HomePage = () => {
    return (
        <HomeLayout value={0}>
            <Container maxWidth="sm" sx={{flexGrow: 1}}>
                <Grid container spacing={2}>
                    <VideoCard/>
                </Grid>
            </Container>
        </HomeLayout>
    );
}

export default HomePage
