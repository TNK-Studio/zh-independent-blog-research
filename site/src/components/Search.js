import React, { useContext, useState } from 'react';
import { fade, makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import Badge from '@material-ui/core/Badge';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import AccountCircle from '@material-ui/icons/AccountCircle';
import MailIcon from '@material-ui/icons/Mail';
import NotificationsIcon from '@material-ui/icons/Notifications';
import MoreIcon from '@material-ui/icons/MoreVert';

import { Divider } from '@material-ui/core';
import Select from '@material-ui/core/Select';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';

import { AppContext } from '../Context'

const useStyles = makeStyles(theme => ({
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
            width: 'auto',
        },
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: 200,
        },
    },
    sectionDesktop: {
        display: 'none',
        [theme.breakpoints.up('md')]: {
            display: 'flex',
        },
    },
    sectionMobile: {
        display: 'flex',
        [theme.breakpoints.up('md')]: {
            display: 'none',
        },
    },
}));

export default function PrimarySearchAppBar() {
    const classes = useStyles();
    const { state, dispatch } = useContext(AppContext)
    const [domain, setDomain] = useState(null)

    return (
        <div className={classes.grow}>
            <AppBar position="static" >
                <Toolbar>
                    {/* <IconButton
                        edge="start"
                        className={classes.menuButton}
                        color="inherit"
                        aria-label="open drawer"
                    >
                        <MenuIcon />
                    </IconButton> */}
                    <Typography className={classes.title} variant="h6" noWrap>
                        中文独立博客调研
                    </Typography>
                    <div className={classes.search}>
                        <div className={classes.searchIcon}>
                            <SearchIcon />
                        </div>
                        <InputBase
                            value={domain}
                            onChange={(e) => { setDomain(e.target.value) }}
                            placeholder="a.blog.domain"
                            classes={{
                                root: classes.inputRoot,
                                input: classes.inputInput,
                            }}
                            inputProps={{ 'aria-label': 'search' }}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    dispatch({
                                        type: 'setDomain',
                                        payload: {
                                            domain
                                        }
                                    })
                                }
                            }}
                        />
                    </div>
                    <div>
                        <FormControl >
                            <div style={{ display: 'flex' }}>
                                <div style={{ lineHeight: '2em' }}>关系网深度：</div> <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={state.depath}
                                    onChange={(e) => {
                                        dispatch({
                                            type: 'set',
                                            payload: {
                                                depath: parseInt(e.target.value)
                                            }
                                        })
                                    }}
                                >
                                    {
                                        [...Array(5).keys()].map(i => <MenuItem value={i + 1}>{i + 1}</MenuItem>)
                                    }
                                </Select>
                            </div>
                            {/* <FormHelperText>关系网深度</FormHelperText> */}
                        </FormControl>
                    </div>
                    <div className={classes.grow} />
                </Toolbar>
            </AppBar>
        </div>
    );
}
