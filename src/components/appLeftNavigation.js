import {Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar} from "@mui/material";
import * as React from 'react';
import Box from "@mui/material/Box";
import RestoreIcon from "@mui/icons-material/Restore";
import FavoriteIcon from "@mui/icons-material/Favorite";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import {Link} from "gatsby";

const AppLeftNavigation = ({value}) => {
    const drawerWidth = 180;
    return (
        <Drawer variant="permanent" sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' }
        }}>
            <Toolbar/>
            <Box sx={{overflow: 'auto'}}>
                <List>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/home" selected={value === 0}>
                            <ListItemIcon>
                                <RestoreIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"Home1"}/>
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/home2" selected={value === 1}>
                            <ListItemIcon>
                                <FavoriteIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"Home2"}/>
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={Link} to="/home3" selected={value === 2}>
                            <ListItemIcon>
                                <LocationOnIcon/>
                            </ListItemIcon>
                            <ListItemText primary={"Home3"}/>
                        </ListItemButton>
                    </ListItem>
                </List>
            </Box>
        </Drawer>
    );
};

export default AppLeftNavigation;