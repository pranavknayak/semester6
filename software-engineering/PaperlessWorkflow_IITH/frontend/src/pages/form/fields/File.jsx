import { Input, InputAdornment, IconButton } from '@mui/material';
import AttachmentIcon from '@mui/icons-material/Attachment';
import { useState, useEffect } from 'react';

const File = ({ label, formData, setFormData }) => {

    const [value, setValue] = useState({});

    useEffect(() => {
        console.log(value);
        setFormData({...formData, [label]: value});
    }, [value]);

    const handleChange = (e) => {
        setValue(e.target.files);
    }
    
    return(
        <Input
            required
            type="file"
            name="file"
            color='secondary'
            onChange={handleChange}
            inputProps={{ multiple: true, title: "Upload a file" }}
            endAdornment={
                <InputAdornment position="end" >
                    {label}
                  <IconButton disableFocusRipple disableRipple style={{cursor: 'auto'}}>
                    <AttachmentIcon/>
                  </IconButton>
                </InputAdornment>
            }
            sx={{
                gridColumn: "span 2",
                padding: "10px",
                borderRadius: "5px",
            }}  
        />
    );
}

export default File;