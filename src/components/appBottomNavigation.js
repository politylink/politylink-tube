import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import {Link} from "gatsby";
import * as React from "react";
import {BottomPaper} from "../layout/bottomPaper";
import HomeIcon from '@mui/icons-material/Home';
import ContentPasteSearchIcon from '@mui/icons-material/ContentPasteSearch';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const AppBottomNavigation = ({value}) => {
    return (
        <BottomPaper elevation={3}>
            <BottomNavigation showLabels value={value}>
                <BottomNavigationAction
                    label="ホーム"
                    icon={<HomeIcon/>}
                    component={Link}
                    to="/"
                />
                <BottomNavigationAction
                    label="トピック"
                    icon={<ContentPasteSearchIcon/>}
                    component={Link}
                    to="/topic"
                />
                <BottomNavigationAction
                    label="議員"
                    icon={<AccountCircleIcon/>}
                    component={Link}
                    to={"/speaker"}
                />
            </BottomNavigation>
        </BottomPaper>
    );
};

export default AppBottomNavigation;