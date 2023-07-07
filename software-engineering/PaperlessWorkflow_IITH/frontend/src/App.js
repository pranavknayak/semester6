import React, { useState, createContext } from 'react'
import { Routes, Route, useLocation, Navigate } from 'react-router-dom'
import Topbar from './pages/global/Topbar';
import LoginTopbar from './pages/login/LoginTopbar'
import Sidebar from './pages/global/Sidebar';
import Login from './pages/login';
import Home from './pages/home'
import Admin from './pages/admin';
import FAQ from './pages/FAQ';
import Form from './pages/form';
import Active from './pages/tables/Active';
import Past from './pages/tables/Past';

import { ColorModeContext, useMode } from './theme'
import { CssBaseline, ThemeProvider } from '@mui/material'
import { googleLogout } from '@react-oauth/google';
import { create } from '@mui/material/styles/createTransitions';

// const baseURL = 'http://localhost:5000';
export const UserContext = createContext();
export const FormContext = createContext();
export const SidebarContext = createContext();

function App() {

  const [theme, colorMode] = useMode()
  const location = useLocation();
  const isLogin = location.pathname.startsWith('/login');
  const isFormPage = location.pathname.startsWith('/form');
  const [user, setUser] = useState(null);

  const logoutUser = () => {
        googleLogout();
        setUser(null);
  }

  const [openFormModal, setOpenFormModal] = useState(false);
  const [formType, setFormType] = useState(null);
  const [fillFormInfo, setFillFormInfo] = useState(null);
  const [selected, setSelected] = useState("Dashboard");
  const [pendingForms, setPendingForms] = useState(null);
  
  return(
    <>
    <SidebarContext.Provider value={{selected, setSelected}}>
    <FormContext.Provider value={{formType, setFormType, openFormModal, setOpenFormModal, fillFormInfo, setFillFormInfo}}>
    <UserContext.Provider value={{user, setUser, logoutUser, pendingForms, setPendingForms}}>
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
          <div className='app'>
            {!isLogin && user? <Sidebar/> : <></>} 
            <main className='content'>
              {!isLogin && user? <Topbar/> : <LoginTopbar/>}
                <Routes>
                  <Route path="/*" element={<Navigate to="/" />} />
                  <Route path="/" element={<Home />} />
                  <Route path="/admin" element={<Admin />} />
                  <Route path="/FAQ" element={<FAQ />} />
                  <Route path="/form" element={<Form />} />
                  <Route path="/active" element={<Active />} />
                  <Route path="/past" element={<Past />} />
                  
                  <Route path="/login" element={<Login />} />
                </Routes>
            </main>
          </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
    </UserContext.Provider>
    </FormContext.Provider>
    </SidebarContext.Provider>
    </>
  );

}

export default App;

