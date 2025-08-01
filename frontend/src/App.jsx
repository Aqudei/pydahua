import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";


function App() {
  const [data, setData] = useState({});
  const [result, setResult] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;

    setData(d => ({
      ...d,
      [name]: value
    }));
  };
  const handleSend = async () => {
    const url = `${API_BASE_URL}/command/`;
    const response = await axios.post(url, {
      cgi: data.cgi,
      params: data.params
    });

    setResult(response.data);
    console.log(response);

  };

  const handleAutoFocus = async () => {
    const url = `${API_BASE_URL}/autofocus/`;
    const response = await axios.post(url);
    console.log(response);


  };
  return (
    <div className="p-4 space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">CGI</label>
        <input
          type="text"
          name='cgi'
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Params</label>
        <textarea
          name='params'
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          rows="4"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Result</label>
        <textarea
          disabled
          value={result}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          rows="4"
        />
      </div>

      <div className='space-x-1'>
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Send
        </button>

        <button
          onClick={handleAutoFocus}
          className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Auto Focus
        </button>
      </div>
    </div>
  );
}

export default App
