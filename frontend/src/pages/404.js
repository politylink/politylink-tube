import * as React from "react"
import HomeLayout from "../layout/homeLayout";
import Container from "@mui/material/Container";
import {Alert} from "@mui/material";


const NotFoundPage = () => {
    return (
        <HomeLayout value={3}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Alert severity="error">ページが見つかりませんでした。</Alert>
            </Container>
        </HomeLayout>

    )
}

export default NotFoundPage

export const Head = () => <title>Not found</title>