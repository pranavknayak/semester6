import Header from '../../components/Header';
import { Box, useTheme } from '@mui/material';
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";

import { useContext } from 'react';
import { UserContext } from '../../App';
import { Navigate } from 'react-router-dom';

const FAQ = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const { user } = useContext(UserContext);

    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        <Box m="20px">
            <Header title="FAQ" subtitle="Here are some Frequently Asked Questions" />
            <br></br>
            <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography color={colors.greenAccent[500]} variant="h5">
                    Question1
                </Typography>
                </AccordionSummary>
                <AccordionDetails>
                <Typography>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
                    malesuada lacus ex, sit amet blandit leo lobortis eget.
                </Typography>
                </AccordionDetails>
            </Accordion>
            <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography color={colors.greenAccent[500]} variant="h5">
                    Question2
                </Typography>
                </AccordionSummary>
                <AccordionDetails>
                <Typography>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
                    malesuada lacus ex, sit amet blandit leo lobortis eget.
                </Typography>
                </AccordionDetails>
            </Accordion>
            <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography color={colors.greenAccent[500]} variant="h5">
                    Question3
                </Typography>
                </AccordionSummary>
                <AccordionDetails>
                <Typography>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
                    malesuada lacus ex, sit amet blandit leo lobortis eget.
                </Typography>
                </AccordionDetails>
            </Accordion>
        </Box>
        </>
    );
    
}

export default FAQ;