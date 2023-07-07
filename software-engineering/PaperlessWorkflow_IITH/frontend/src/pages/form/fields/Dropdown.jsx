import { useState, useEffect } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const Dropdown = ( { label, options, formData, setFormData }) => {

    const [value, setValue] = useState("");

    useEffect(() => {
        setFormData({...formData, [label]: value});
    }, [value]);

    const handleChange = (e) => {
        setValue(e.target.value.toString());
    }

    const renderMenuItems = () => {
        const items = []
        for(let i = 0; i < options.length; i++)
            items.push(<MenuItem value={options[i]}>{options[i]}</MenuItem>)
        return items;
    }

    return(
        <FormControl sx={{gridColumn: "span 2"}}>
            <InputLabel id="demo-multiple-name-label" color='secondary'>{label}</InputLabel>
            <Select
                value={value}
                label={label}
                onChange={handleChange}
                color='secondary'
            >
                {renderMenuItems()}
            </Select>
        </FormControl>
    );
}

export default Dropdown;