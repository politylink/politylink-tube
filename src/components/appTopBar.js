import AppBar from "@mui/material/AppBar";
import * as React from "react";
import {Toolbar} from "@mui/material";
import Typography from "@mui/material/Typography";
import {Link as GatsbyLink} from "gatsby";
import Link from "@mui/material/Link"

const AppTopBar = () => {
    return (
        <AppBar position="fixed" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
            <Toolbar variant="dense">
                <Link component={GatsbyLink} to="/home" sx={{textDecoration: 'none'}}>
                    <Typography variant={"h6"} color="white">PolityLink</Typography>
                </Link>
            </Toolbar>
        </AppBar>
    );
}

export default AppTopBar;