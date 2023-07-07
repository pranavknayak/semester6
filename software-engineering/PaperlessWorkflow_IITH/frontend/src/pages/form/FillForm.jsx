// Component that renders the form based on template - APPLICANT
import axios from 'axios';
import { useContext, useState } from 'react';
import { FormContext } from '../../App';
import { Box, Button } from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';
import Date from './fields/Date';
import File from './fields/File';
import Check from './fields/Check';
import Dropdown from './fields/Dropdown';
import Text from './fields/Text';
import { UserContext } from '../../App';
const baseURL = 'http://localhost:5000';

const FillForm = () => {

  const { formType, setFormType, fillFormInfo, setFillFormInfo } = useContext(FormContext);
  const { user, setUser } = useContext(UserContext);
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const req_fields = fillFormInfo['level_data'][0]['req_fields'];
  const [formData, setFormData] = useState({});

  // Logic to render fields specific to formtype
  const render_elements = () => {
    const elements = []
    for (let i = 0; i < req_fields.length; i++) {
      let display_name = req_fields[i][0]
      let field = req_fields[i][1];
      let item = <></>;
      if (field === 'textbox')
        item = <Text label={display_name} formData={formData} setFormData={setFormData} />
      else if (field === 'date')
        item = <Date label={display_name} formData={formData} setFormData={setFormData} />
      else if (field === 'dropdown') {
        let options = req_fields[i][2];
        item = <Dropdown label={display_name} options={options} formData={formData} setFormData={setFormData} name="dropdown" />
      }
      else if (field === 'file')
        item = <File label={display_name} formData={formData} setFormData={setFormData} name="file" />
      else if (field === 'checkbox')
        item = <Check label={display_name} formData={formData} setFormData={setFormData} name="checkbox" />

      elements.push(item);
    }
    return elements;
  }

  // Handles form submission
  const handleFormSubmit = (event) => {
    event.preventDefault();
    console.log("Submitted Form!");
    console.log(formData)

    // CHANGE formData state object to the backend instead
    let formdata = new FormData(event.target);
    formdata = Object.fromEntries(formdata.entries());
    // console.log(formdata);
    axios.post(`${baseURL}/demo/submit`, { 'data': formdata, 'user': user, 'form_type': 'leave' })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      })

    setFillFormInfo(null);
    setFormType(null);
    setFormData({});
  }

  return (
    <form onSubmit={handleFormSubmit}>
      <Box
        display="grid"
        gap="30px"
        gridTemplateColumns="repeat(4, minmax(0, 1fr))"
        sx={{
          "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
        }}
      >
        {render_elements()}
      </Box>
      <Box display="flex" justifyContent="end" mt="20px">
        <Button type="submit" color="secondary" variant="contained">
          Submit Form
        </Button>
      </Box>
    </form>

  )
}

export default FillForm;
