import Header from '../../components/Header';
import { Box } from '@mui/material';
import { useContext } from 'react';
import { UserContext } from '../../App';
import { Navigate } from 'react-router-dom';

const Admin = () => {
    const { user } = useContext(UserContext);

    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header
                    title="ADMIN"
                    subtitle="This is the Admin Panel"
                />
            </Box>
        </Box>
        </>
    );
    
}

export default Admin;