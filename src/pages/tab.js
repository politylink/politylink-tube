import * as React from 'react';
import {useState} from 'react';
import Box from "@mui/material/Box";
import {Toolbar, useMediaQuery, useTheme} from "@mui/material";
import AppBottomController from "../components/appBottomController";
import AppTopBar from "../components/appTopBar";


const TabPage = () => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const [isLeft, setIsLeft] = useState(true);

    return (
        <Box>
            <AppTopBar/>
            <Toolbar/>
            <Box sx={{
                width: isMobile ? '200%' : '100%',
                display: 'flex',
                transform: (isMobile && !isLeft) ? 'translateX(-50%)' : 'translateX(0)'
            }}>
                <Box sx={{width: "50%"}}>
                    <p>left</p>
                </Box>
                <Box sx={{width: "50%"}}>
                    <p>right</p>
                </Box>
            </Box>

            <AppBottomController
                isLeft={isLeft}
                switchLeft={() => setIsLeft(true)}
                switchRight={() => setIsLeft(false)}
                currentTime={0}
                duration={100}
                isPaused={true}
                updateTime={() => console.log('update')}
                startPlayer={() => console.log('start')}
                stopPlayer={() => console.log('stop')}
            />
        </Box>
    );
};

export default TabPage;