import React, { useContext, useState } from 'react';
import { fade, makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import MenuItem from '@material-ui/core/MenuItem';
import SearchIcon from '@material-ui/icons/Search';
import { Link } from 'react-router-dom';

import Select from '@material-ui/core/Select';
import FormControl from '@material-ui/core/FormControl';

import { AppContext } from '../Context'

const useStyles = makeStyles(theme => ({
    grow: {
        flexGrow: 1,
        position: "fixed",
        top: 0,
        width: '100%',
        zIndex: 10
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
    console.log(state)

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
                        <Link to="/" style={{
                            textDecoration: 'none',
                            color: '#fff'
                        }}>中文独立博客调研</Link>
                    </Typography>
                    <div className={classes.search}>
                        <div className={classes.searchIcon}>
                            <SearchIcon />
                        </div>
                        <InputBase
                            value={domain}
                            onChange={(e) => { setDomain(e.target.value) }}
                            placeholder="搜索"
                            classes={{
                                root: classes.inputRoot,
                                input: classes.inputInput,
                            }}
                            inputProps={{ 'aria-label': 'search' }}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    dispatch({
                                        type: 'setQ',
                                        payload: {
                                            q: domain
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
                    <Link to='report' component={Button} style={{
                        textDecoration: 'none',
                        color: '#fff'
                    }}>
                        报告
                    </Link>
                    <Link to='about' component={Button} style={{
                        textDecoration: 'none',
                        color: '#fff'
                    }}>
                        关于
                    </Link>

                    <div className={classes.grow} />
                </Toolbar>
            </AppBar>
        </div>
    );
}
