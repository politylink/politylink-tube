import * as React from "react"
import Container from "@mui/material/Container";
import HomeLayout from "../layout/homeLayout";


const HomePage = () => {
    return (
        <HomeLayout value={2}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <p>WIP</p>
            </Container>
        </HomeLayout>
    );
}

export default HomePage
