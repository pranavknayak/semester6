import { TextField, FormControl } from '@mui/material';
import { useState } from 'react';

const Text = ({label, formData, setFormData}) => {

    const [value, setValue] = useState("");
    const handleChange = (e) => {
        setValue(e.target.value);
        setFormData({...formData, [label]: value});
    }

    return(
        <FormControl sx={{gridColumn: "span 4"}}>
        <TextField
            fullWidth
            required
            variant="filled"
            type="text"
            label={label}
            autoComplete='off'
            onChange={handleChange}
            value={value}
            name={label}
            color='secondary'
        />
        </FormControl>
    );
}

export default Text;