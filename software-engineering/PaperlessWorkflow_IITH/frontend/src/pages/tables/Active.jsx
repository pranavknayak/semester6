import Header from '../../components/Header';
import { Box, Typography, useTheme } from '@mui/material';
import { tokens } from '../../theme';
import { DataGrid } from '@mui/x-data-grid';
import { mockData } from '../../data/mockData';
import PersonIcon from '@mui/icons-material/Person';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import { useContext } from 'react';
import { UserContext } from '../../App';
import { Navigate } from 'react-router-dom';

const Active = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const { user } = useContext(UserContext);

    const columns = [
        {field: "id", headerName: "ID"},
        {field: "type", headerName: "Form Type", flex: 1    , cellClassName: "form-column--cell"},
        {
            field: "role", 
            headerName: "Role",
            headerAlign: "center", 
            flex: 1,
            renderCell: ({row: {role}}) => {
                return (
                    <Box
                        width="40%"
                        m="0 auto"
                        p="5px"
                        display="flex"
                        justifyContent="center"
                        backgroundColor={
                            role==='applicant'
                            ? colors.greenAccent[600]
                            : colors.greenAccent[700]
                        }
                        borderRadius="4px"
                    >
                        {role==='applicant'? <PersonIcon/> : <VerifiedUserIcon/>}
                        <Typography
                            color={colors.grey[100]}
                            sx={{ ml: "5px"}}
                        >{role}</Typography>
                    </Box>
                )
            }
        }
    ]
    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        <Box m="20px">
            {/* <Box display="flex" justifyContent="space-between" alignItems="center"> */}
            <Header title="ACTIVE FORMS" subtitle="List of active forms."/>
            <Box
                m="40px 0 0 0"
                height="75vh"   
                sx ={{
                    "& .MuiDataGrid-root": {
                        border: "none",
                      },
                      "& .MuiDataGrid-cell": {
                        borderBottom: "none",
                      },
                      "& .form-column--cell": {
                        color: colors.greenAccent[300],
                      },
                      "& .MuiDataGrid-columnHeaders": {
                        backgroundColor: colors.blueAccent[700],
                        borderBottom: "none",
                      },
                      "& .MuiDataGrid-virtualScroller": {
                        backgroundColor: colors.primary[400],
                      },
                      "& .MuiDataGrid-footerContainer": {
                        borderTop: "none",
                        backgroundColor: colors.blueAccent[700],
                      },
                      "& .MuiCheckbox-root": {
                        color: `${colors.greenAccent[200]} !important`,
                      },  
                }} 
            >
                <DataGrid rows={mockData} columns={columns}/>
            </Box>
        </Box>
        </>
    );
    
}

export default Active;