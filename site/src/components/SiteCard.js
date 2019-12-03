import React, { useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import { AppContext } from '../Context'


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
    const { selectedSite } = state
    return (
        <>
            {selectedSite && <Card className={classes.card}>
                <CardActionArea>
                    <CardMedia
                        className={classes.media}
                        image="/static/images/cards/contemplative-reptile.jpg"
                        title="Contemplative Reptile"
                    />
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {selectedSite.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" component="p">
                            {selectedSite.url}
                        </Typography>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary" onClick={() => window.open(selectedSite.url)}>
                        查看站点
                    </Button>
                    <Button size="small" color="primary" onClick={() => dispatch({ type: 'computeGraph' })}>
                        查看好友关系
                    </Button>
                    <Button size="small" color="primary" onClick={() => dispatch({ type: 'clearCard' })}>
                        关闭卡片
                    </Button>
                </CardActions>
            </Card>
            }
        </>
    );
}
