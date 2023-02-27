import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import {Chip} from "@mui/material";
import ShareIcon from "@mui/icons-material/Share";
import Link from "@mui/material/Link";


const VideoInfoPanel = ({title, date, duration, pageUrl, annotations, updateTime}) => {
    return (
        <Box sx={{
            padding: 1,
            maxWidth: '800px',
            margin: 'auto'
        }}>
            <Box sx={{display: 'flex', justifyContent: 'center'}}>
                <Box sx={{flexGrow: 1}}>
                    <Typography variant='h5'
                                sx={{letterSpacing: -0.05, fontWeight: 'bold', lineHeight: 1.15}}>
                        {title}
                    </Typography>
                    <Box sx={{
                        marginTop: 0.5,
                        display: "flex",
                        alignItems: "center",
                    }}>
                        <Typography variant="body1" color="text.secondary">
                            {date}
                        </Typography>
                        <Typography variant="body1" color="text.secondary" sx={{marginLeft: 2}}>
                            {duration}
                        </Typography>
                    </Box>
                </Box>
            </Box>
            <Box sx={{marginTop: 2}}>
                <Typography>
                    【公式サイト】
                </Typography>
                <Link href={pageUrl} target="_blank" rel="noopener">
                    {pageUrl}
                </Link>
            </Box>
            <Box sx={{marginTop: 2}}>
                <Typography>
                    【発言者】
                </Typography>
                {annotations.map(({start, time, text}, i) => (
                    <Box sx={{display: 'flex', marginY: 0, alignItems: 'start'}} key={i}>
                        <Link component="button" variant="body2" underline="hover" onClick={() => updateTime(start)}
                              color='primary'>
                            {time}
                        </Link>
                        <Typography sx={{marginLeft: 1}} variant='body2'>
                            {text}
                        </Typography>
                    </Box>
                ))}
            </Box>
        </Box>
    );
}

export default VideoInfoPanel;