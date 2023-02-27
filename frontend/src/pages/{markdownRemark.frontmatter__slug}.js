import React from "react"
import {graphql} from 'gatsby'
import SEO from "../components/seo";
import Container from "@mui/material/Container";
import AppTopBar from "../components/appTopBar";
import Box from "@mui/material/Box";
import {Toolbar} from "@mui/material";
import Link from "@mui/material/Link";

const MarkdownPage = ({data}) => {
    const {markdownRemark} = data
    const {html} = markdownRemark
    return (
        <Box sx={{backgroundColor: 'white', minHeight: '100vh'}}>
            <AppTopBar/>
            <Container>
                <Toolbar/>
                <Box dangerouslySetInnerHTML={{__html: html}}/>
                <Box sx={{paddingY: 10}}>
                    <Link href="https://www.buymeacoffee.com/mitsukiusui" target="_blank" rel="noopener" sx={{
                        display: 'flex',
                        justifyContent: 'center'
                    }}>
                        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee"
                             style={{
                                 height: '60px',
                                 width: '217px',
                             }}/>
                    </Link>
                </Box>
            </Container>
        </Box>
    )
}

export const query = graphql`
query ( $id: String!) {
    markdownRemark (id: {eq: $id}) {
        html
        frontmatter {
            slug
            title
        }
    }
}
`

export default MarkdownPage
export const Head = ({location, data}) => {
    const title = data.markdownRemark.frontmatter.title
    return (
        <SEO
            title={title}
            path={location.pathname}
        />
    )
}