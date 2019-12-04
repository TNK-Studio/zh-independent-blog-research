import React, { useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import { AppContext } from '../Context'


const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
        height: 'calc(100% - 64px)',
        position: 'fixed',
        overflowY: 'scroll'
    },
    inline: {
        display: 'inline',
    },
}));

export default function AlignItemsList() {
    const classes = useStyles();
    const { state, dispatch } = useContext(AppContext)
    const { q, blogList, selectedSite } = state
    return (<>
        {
            q && <List className={classes.root}>
                {
                    blogList.length === 0 ? <span>啥也没有</span> : blogList.map(site => <ListItem
                        alignItems="flex-start"
                        button
                        onClick={() => {
                            dispatch({
                                type: 'setSelectedSite',
                                payload: {
                                    selectedSite: site
                                }
                            })
                        }}
                    >
                        <ListItemAvatar>
                            <Avatar alt={site.name} src={site.icon} />
                        </ListItemAvatar>
                        <ListItemText
                            primary={site.name}
                            secondary={
                                <React.Fragment>
                                    <Typography
                                        component="span"
                                        variant="body2"
                                        className={classes.inline}
                                        color="textPrimary"
                                    >
                                        {site.description}
                                    </Typography>
                                </React.Fragment>
                            }
                        />
                    </ListItem>)
                }

            </List>
        }
    </>)
}
