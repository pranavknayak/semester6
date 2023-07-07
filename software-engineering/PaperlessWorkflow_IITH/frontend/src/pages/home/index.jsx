import Header from '../../components/Header';
import { Box } from '@mui/material';
import { useContext } from 'react';
import { UserContext, SidebarContext } from '../../App';
import { Navigate } from 'react-router-dom';

const Home = () => {

    const { user } = useContext(UserContext);
    const { setSelected } = useContext(SidebarContext);

    setSelected("Home");
    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header
                    title="HOME"
                    subtitle="Welcome to your homescreen"
                />
            </Box>
        </Box>
        </>
    );
    
}

export default Home;