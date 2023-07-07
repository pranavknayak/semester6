import { useState, useEffect } from 'react';
import { Checkbox, FormControlLabel } from '@mui/material';

const Check = ({ label, formData, setFormData }) => {

    const [value, setValue] = useState(false);

    useEffect(() => {
        setFormData({...formData, [label]: value});
        // console.log(value);
    }, [value]);

    const handleChange = (e) => {
        setValue(e.target.checked);
    }

    return(
        <FormControlLabel 
            control={<Checkbox defaultChecked={false} color='secondary'/>} 
            label={label}
            value={value}
            onChange={handleChange} 
            sx ={{ gridColumn: "span 4" }}
        />
    );
}

export default Check;