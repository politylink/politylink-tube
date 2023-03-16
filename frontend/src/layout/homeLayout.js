import React from "react";
import AppTopBar from "../components/appTopBar";
import AppLeftNavigation from "../components/appLeftNavigation";
import Box from "@mui/material/Box";
import AppBottomNavigation from "../components/appBottomNavigation";
import { Toolbar, useMediaQuery, useTheme } from "@mui/material";

const HomeLayout = ({ children, value }) => {
  const theme = useTheme();
  const isLarge = useMediaQuery(theme.breakpoints.up("md"));

  return (
    <Box sx={{ display: "flex" }}>
      <AppTopBar />
      {isLarge && <AppLeftNavigation value={value} />}
      <Box sx={{ flexGrow: 1, margin: 0 }}>
        <Toolbar variant="dense" />
        {children}
        <Toolbar />
      </Box>
      {!isLarge && <AppBottomNavigation value={value} />}
    </Box>
  );
};

export default HomeLayout;
