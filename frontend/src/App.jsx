import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";


function App() {

  const handleAutoFocus = async () => {
    const url = `${API_BASE_URL}/autofocus/`;
    const response = await axios.post(url);
    console.log(response);


  };
  return <>
    <button onClick={handleAutoFocus}>Auto Focus</button>
  </>
}

export default App
