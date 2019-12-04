import React, { useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import RSSIcon from '@material-ui/icons/RssFeed'
import Typography from '@material-ui/core/Typography';
import { AppContext } from '../Context'
import Avatar from '@material-ui/core/Avatar';
import CardHeader from '@material-ui/core/CardHeader';
import IconButton from '@material-ui/core/IconButton';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import FriendsIcon from '@material-ui/icons/People';
import CloseIcon from '@material-ui/icons/Close';
import OpenInNewIcon from '@material-ui/icons/OpenInNew';
import HttpsIcon from '@material-ui/icons/Https';
import { Divider } from '@material-ui/core';


const useStyles = makeStyles({
    card: {
        width: 345,
        // height: 270
    },
    hideCard: {
        right: -345
    },
    media: {
        height: 140,
    },
});

export default function MediaCard() {
    const classes = useStyles();
    const { state, dispatch } = useContext(AppContext)
    const { selectedSite, q } = state
    return (
        <>
            {selectedSite && !q && <Card className={classes.card}>
                <CardHeader
                    avatar={
                        <Avatar aria-label="recipe" className={classes.avatar} src={selectedSite.icon} />
                    }
                    action={
                        <div>
                            <HttpsIcon style={{ color: selectedSite.url.startsWith("https") ? 'green' : 'gray', padding: 5 }} />
                            <RSSIcon style={{ color: selectedSite.rss ? 'green' : 'gray', padding: 5 }} />
                        </div>
                    }
                    title={selectedSite.name}
                    subheader={selectedSite.url}
                />
                <CardContent>
                    <Typography variant="body1" color="textSecondary" component="p">
                        {selectedSite.description}
                    </Typography>
                    <br />
                    <Typography variant="body2" color="textSecondary" component="p">
                        生成器: {selectedSite.generator}
                    </Typography>
                </CardContent>
                <CardActions>
                    <IconButton aria-label="查看" onClick={() => window.open(selectedSite.url)}>
                        <OpenInNewIcon />
                    </IconButton>
                    <IconButton aria-label="好友" onClick={() => dispatch({ type: 'computeGraph' })}>
                        <FriendsIcon />
                    </IconButton>
                    <IconButton aria-label="关闭" onClick={() => dispatch({ type: 'clearCard' })}>
                        <CloseIcon />
                    </IconButton>
                </CardActions>
            </Card>
            }
        </>
    );
}
