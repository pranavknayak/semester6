// TODO: need to check if backend error occurred after every server response
// TODO: add documentation to specify the structure of data returned by each function
// TODO: fine tune functionality to respond to different server responses
import axios from 'axios'
const baseURL = 'http://localhost:5000'

//  assumes that user context is available in the component 
handleFormSubmit = (event) => {
  const formdata = new FormData(event.target);
  axios.post(`${baseURL}/form/submit`, { "formData": formdata, "user": user })
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.log(error.code);
    });
}

handleFormApprove = (event) => {
  const formdata = new FormData(event.target);
  axios.post(`${baseURL}/form/approve`, { 'formData': formdata, 'user': user })
    .then(response => {
      console.log(response);
    })
    .catch(error => console.log(error.code))
}

handleFormReject = (event) => {
  const formdata = new FormData(event.target);
  axios.post(`${baseURL}/form/reject`, { 'formData': formdata, 'user': user })
    .then(response => {
      console.log(response);
    })
    .catch(error => console.log(error.code))
}

handleFormReview = (event) => {
  const formdata = new FormData(event.target);
  axios.post(`${baseURL}/form/review`, { 'formData': formdata, 'user': user })
    .then(response => {
      console.log(response);
    })
    .catch(error => console.log(error.code))
}

handleFormRender = (event) => {
  const formID = '';
  axios.get(`${baseURL}/demo/render`, {
    params: {
      'formID': formID
    }
  })
    .then(response => {
      const form_data = response.data;
      console.log(form_data);
    })
    .catch(error => console.log(error.code));
}


