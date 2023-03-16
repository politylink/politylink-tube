import AppBar from "@mui/material/AppBar";
import * as React from "react";
import { Toolbar } from "@mui/material";
import Typography from "@mui/material/Typography";
import { Link as GatsbyLink } from "gatsby";
import Link from "@mui/material/Link";

const AppTopBar = () => {
  return (
    <AppBar
      position="fixed"
      sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
    >
      <Toolbar
        variant="dense"
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Link component={GatsbyLink} to="/" sx={{ textDecoration: "none" }}>
          <Typography variant={"h6"} color="white">
            PolityLink
          </Typography>
        </Link>
        <Link
          component={GatsbyLink}
          to="/about"
          sx={{ textDecoration: "none" }}
        >
          <Typography
            color="white"
            sx={{
              fontSize: "0.75rem",
              fontWeight: 500,
              letterSpacing: 0.2,
            }}
          >
            このサイトについて
          </Typography>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default AppTopBar;
