import { FormControl, InputLabel } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useState, useEffect } from 'react';

const Date = ({ label, formData, setFormData }) => {

  const [value, setValue] = useState("");

  useEffect(() => {
    setFormData({...formData, [label]: value});
  }, [value]);

  const handleChange = (newVal) => {
    setValue(newVal.toISOString());
    // setFormData({...formData, [label]: value});
  }

  return (
    <FormControl label="hello" sx={{ gridColumn: "span 1" }}>
      <DatePicker
        // name='DOB'
        label={label}
        onChange={handleChange}
        color='secondary'
      />

    </FormControl>

  );
}

export default Date;
