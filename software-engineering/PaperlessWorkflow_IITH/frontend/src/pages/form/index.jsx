import Header from '../../components/Header';
import { Box, Button, TextField, useTheme} from '@mui/material';
import { tokens } from '../../theme';
import { Formik } from 'formik';
import * as yup from "yup";
import useMediaQuery from '@mui/material/useMediaQuery';
import { useContext, useState, useEffect, useRef } from 'react';
import { UserContext, FormContext } from '../../App';
import { Navigate } from 'react-router-dom';
import MenuItem from '@mui/material/MenuItem';
import Modal from './Modal';
import FillForm from './FillForm';
import Date from './fields/Date';

import axios from 'axios';
const baseURL = 'http://localhost:5000'

const initialValues = {
    firstName: "",
    lastName: "",
    email: "",
    date: "",
};

const formSchema = yup.object().shape({
    firstName: yup.string().required("required"),
    lastName: yup.string().required("required"),
    email: yup
            .string()
            // .matches(emailRegExp, "invalid email")
            .email("invalid email")
            .required("required"),
    date: yup.string().required()
});

const Form = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const isNonMobile = useMediaQuery("(min-width:600px)");
    const { user } = useContext(UserContext);
    const { openFormModal, setOpenFormModal, formType, setFormType, fillFormInfo, setFillFormInfo } = useContext(FormContext);
  
    const handleFormSubmit = (event) => {
    
      event.preventDefault();
      const data = new FormData(event.target);
      axios.post(`${baseURL}/form/submit`, { "formData": data, "user": user })
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error.code);
        })
        
        setFillFormInfo(null);
        setFormType(null);
        console.log("Submitted Form!");
        // event.preventDefault();
        // const values = new FormData(event.target);
        
        // console.log(values);
        

        // event.preventDefault();
        // const form = event.target;
        // const formData = new FormData(form);
        // const data = Object.fromEntries(formData.entries());
        // console.log(data);
    }

    
    return (
        <>
        {!user ? <Navigate to='/login'/> : <></>}
        { openFormModal ? 
        <Modal open={openFormModal} onClose={()=>setOpenFormModal(false)}/>
        : formType ?
        <Box m="20px">
            {/* <Box display="flex" justifyContent="space-between" alignItems="center"> */}
            <Header title={fillFormInfo['name'].toUpperCase()} subtitle="Enter the details and submit the form."/>
            <br></br>
            <Formik>
                <FillForm/>
            </Formik>
        </Box> 
        :
        <Navigate to='/'/>
        }
        </>
    );
}

export default Form;
