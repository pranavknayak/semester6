import { useState, useContext, useEffect } from 'react';
import { ProSidebar, Menu, MenuItem } from 'react-pro-sidebar';
// import '../../../node_modules/react-pro-sidebar/dist/styles';
import 'react-pro-sidebar/dist/css/styles.css'
import { Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import { tokens } from '../../theme';
import { UserContext, FormContext, SidebarContext } from '../../App';
import { Navigate } from 'react-router-dom';

import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import QuizIcon from '@mui/icons-material/Quiz';
import AddIcon from '@mui/icons-material/Add';
import HomeIcon from '@mui/icons-material/Home';
import ViewListIcon from '@mui/icons-material/ViewList';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";

const Item = ( {title, to, icon, selected, setSelected, altClickFunc}) => {
    const theme = useTheme()
    const colors = tokens(theme.palette.mode);
    return(
        <MenuItem 
            active={selected === title} 
            style = {{ color: colors.grey[100]}} 
            onClick={!altClickFunc ? () => setSelected(title): altClickFunc}
            icon = {icon}>
            <Typography>{title}</Typography>
            <Link to={to}/>
        </MenuItem>
    )
}


const Sidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isCollapsed, setIsCollapsed] = useState(false);
    const { user } = useContext(UserContext);
    const { setOpenFormModal } = useContext(FormContext);
    const { selected, setSelected } = useContext(SidebarContext);

    const altClickFunc = () => {
        setSelected("Submit Form");
        setOpenFormModal(true);
    };

    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        <Box
            sx ={{
                "& .pro-sidebar-inner": {
                    background: `${colors.primary[400]} !important`,
                },
                "& .pro-icon-wrapper": {
                    backgroundColor: "transparent !important",
                },
                "& .pro-inner-item": {
                    padding: "5px 35px 5px 20px !important",
                },
                "& .pro-inner-item:hover": {
                    color: "#868dfb !important",
                },
                "& .pro-menu-item.active": {
                    color: "#6870fa !important",
                }
            }}
        >
        <ProSidebar collapsed={isCollapsed} style={{ height:"100vh" }}>
        <Menu iconShape="square">
          {/* LOGO AND MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            style={{
              margin: "10px 0 20px 0",
              color: colors.grey[100],
            }}
          >
            {!isCollapsed && (
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                ml="15px"
              >
                <Typography variant="h3" color={colors.grey[100]}>
                  {/* PAPERLESS <br></br> WORKFLOW */}
                  DASHBOARD
                </Typography>
                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                  <MenuOutlinedIcon />
                </IconButton>
              </Box>
            )}
          </MenuItem>

        {/* USER */}
        {!isCollapsed && (
            <Box mb="25px">
                <Box display="flex" justifyContent="center" alignItems="center">
                    <img
                        alt="profile-user"
                        width="100px"
                        height="100px"
                        // src={"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}
                        src={user.picture}
                        style={{ cursor: "pointer", borderRadius: "50%"}}
                    />
                </Box>
                <Box textAlign="center">
                    <Typography 
                        variant="h2" 
                        colors={colors.grey[100]} 
                        frontWeight="bold" 
                        sx={{ m: "10px 0 0 0"}}
                    > {user.name} </Typography>
                    <Typography
                        variant="h5"
                        color={colors.greenAccent[500]}
                    > {user.email} </Typography>
                </Box>
            </Box>
        )}

        {/* Navigate to diff pages */}
        <Box paddingLeft={isCollapsed ? undefined : "10%"}>
            <Item
                title="Home"
                to="/home"
                icon={<HomeIcon/>}
                selected={selected}
                setSelected={setSelected} 
            />
            {/* <Item
                title="Admin"
                to="/admin"
                icon={<AdminPanelSettingsIcon/>}
                selected={selected}
                setSelected={setSelected} 
            /> */}
            <Item
                title="Submit Form"
                to="/form"
                icon={<AddIcon/>}
                selected={selected}
                setSelected={setSelected} 
                altClickFunc={altClickFunc}
            />
            <Item
                title="FAQ"
                to="/FAQ"
                icon={<QuizIcon/>}
                selected={selected}
                setSelected={setSelected} 
            />
            <Typography
              variant="h6"
              color={colors.grey[300]}
              sx={{ m: "15px 0 5px 20px" }}
            >
              View Forms
            </Typography>
            <Item
                title="Active Forms"
                to="/active"
                icon={<ViewListIcon/>}
                selected={selected}
                setSelected={setSelected} 
            />
            <Item
                title="Past Forms"
                to="/past"
                icon={<ViewListIcon/>}
                selected={selected}
                setSelected={setSelected} 
            />
        </Box>
        </Menu>
        </ProSidebar>
        </Box>
        </>
    );
}

export default Sidebar;