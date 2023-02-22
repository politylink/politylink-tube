import {Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar} from "@mui/material";
import * as React from 'react';
import Box from "@mui/material/Box";
import {Link} from "gatsby";
import HomeIcon from '@mui/icons-material/Home';
import ContentPasteSearchIcon from '@mui/icons-material/ContentPasteSearch';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';


const AppLeftNavigation = ({value}) => {
    const drawerWidth = 180;
    return (
        <Drawer variant="permanent" sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: {width: drawerWidth, boxSizing: 'border-box'}
        }}>
            <Toolbar/>
            <Box sx={{overflow: 'auto'}}>
                <List>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/" selected={value === 0}>
                            <ListItemIcon>
                                <HomeIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"ホーム"}/>
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/topic" selected={value === 1}>
                            <ListItemIcon>
                                <ContentPasteSearchIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"トピック"}/>
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/speaker" selected={value === 2}>
                            <ListItemIcon>
                                <AccountCircleIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"議員"}/>
                        </ListItemButton>
                    </ListItem>
                </List>
            </Box>
        </Drawer>
    );
};

export default AppLeftNavigation;