import AppBar from "@mui/material/AppBar";
import * as React from "react";
import {Toolbar} from "@mui/material";
import Typography from "@mui/material/Typography";

const AppTopBar = () => {
    return (
        <AppBar position="fixed" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
            <Toolbar>
                <Typography varian={"h6"}>PolityLink</Typography>
            </Toolbar>
        </AppBar>
    );
}

export default AppTopBar;