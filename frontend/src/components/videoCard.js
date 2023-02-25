import * as React from "react"
import Grid from "@mui/material/Grid";
import {Card, CardActionArea} from "@mui/material";
import Typography from "@mui/material/Typography";
import {Link as GatsbyLink} from "gatsby";
import PersonIcon from '@mui/icons-material/Person';
import PlaceIcon from '@mui/icons-material/Place';
import Box from "@mui/material/Box";


const VideoCard = ({clipUrl, imageUrl, title, date, duration, speaker, place}) => {
    return (
        <Grid item xs={12} sm={6} md={3}>
            <CardActionArea component={GatsbyLink} to={clipUrl}>
                <Card square elevation={0}>
                    <img
                        loading='lazy' height='200' width='100%' style={{objectFit: 'cover'}}
                        src={imageUrl} alt="thumbnail"
                    />
                    <Box sx={{paddingX: 1, paddingTop: 1, paddingBottom: 2}}>
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{letterSpacing: -0.05, fontWeight: 'bold', lineHeight: 1.15}}
                        >
                            {title}
                        </Typography>
                        <Box sx={{
                            marginTop: 0.5,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                        }}>
                            <Typography variant="body2" color="text.secondary" sx={{marginLeft: 0.5}}>
                                {date}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{marginLeft: 0.5}}>
                                {duration}
                            </Typography>
                        </Box>

                        {(speaker || place) &&
                            <Box sx={{paddingX: 1, marginTop: 1}}>
                                {place &&
                                    <Box sx={{display: "flex", alignItems: "center"}}>
                                        <PlaceIcon/>
                                        <Typography variant="body2" color="text.secondary" sx={{marginLeft: 0.5}}>
                                            {place}
                                        </Typography>
                                    </Box>
                                }
                                {speaker &&
                                    <Box sx={{display: "flex", alignItems: "center"}}>
                                        <PersonIcon/>
                                        <Typography variant="body2" color="text.secondary" sx={{marginLeft: 0.5}}>
                                            {speaker}
                                        </Typography>
                                    </Box>
                                }
                            </Box>
                        }
                    </Box>
                </Card>
            </CardActionArea>
        </Grid>
    );
}

export default VideoCard;