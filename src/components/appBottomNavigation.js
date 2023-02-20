import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import RestoreIcon from "@mui/icons-material/Restore";
import {Link} from "gatsby";
import FavoriteIcon from "@mui/icons-material/Favorite";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import * as React from "react";
import {Paper} from "@mui/material";
import {BottomPaper} from "../layout/bottomPaper";

const AppBottomNavigation = ({value}) => {
    return (
        <BottomPaper elevation={3}>
            <BottomNavigation showLabels value={value}>
                <BottomNavigationAction
                    label="Recent"
                    icon={<RestoreIcon/>}
                    component={Link}
                    to="/home"
                />
                <BottomNavigationAction
                    label="Favorites"
                    icon={<FavoriteIcon/>}
                    component={Link}
                    to="/home2"
                />
                <BottomNavigationAction
                    label="Nearby"
                    icon={<LocationOnIcon/>}
                    component={Link}
                    to={"/home3"}
                />
            </BottomNavigation>
        </BottomPaper>
    );
};

export default AppBottomNavigation;