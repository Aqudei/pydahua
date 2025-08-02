import { useState } from 'react';
import './App.css';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

function App() {
  const [data, setData] = useState({});
  const [result, setResult] = useState('');
  const [colorMode, setColorMode] = useState(1);


  const handleSetColorMode = async () => {
    try {
      const url = `${API_BASE_URL}/set-color-mode/`;
      const response = await axios.post(url, {
        color_mode: colorMode
      });

      setResult(JSON.stringify(response.data, null, 2));
      console.log(response);
    } catch (err) {
      setResult('Error: ' + err.message);
      console.error(err);
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSend = async () => {
    try {
      const url = `${API_BASE_URL}/command/`;
      const response = await axios.post(url, {
        cgi: data.cgi,
        params: data.params,
      });
      setResult(JSON.stringify(response.data, null, 2));
      console.log(response);
    } catch (err) {
      setResult('Error: ' + err.message);
      console.error(err);
    }
  };

  const handleAutoFocus = async () => {
    try {
      const url = `${API_BASE_URL}/autofocus/`;
      const response = await axios.post(url);
      console.log(response);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-2xl mx-auto">
      {/* Color Mode Section */}
      <div className="space-y-2">
        <label htmlFor="colorMode" className="block text-sm font-medium text-gray-700">
          Color Mode
        </label>
        <select
          name="colorMode"
          id="colorMode"
          onChange={(e) => setColorMode(parseInt(e.target.value))}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          <option value="">--Select Color Mode--</option>
          <option value="0">Always MultiColor</option>
          <option value="1">Auto-switch with Brightness</option>
          <option value="2">Always Monochrome</option>
        </select>
        <button
          type="button"
          onClick={handleSetColorMode}
          className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Set Color Mode
        </button>
      </div>

      {/* CGI Input */}
      <div>
        <label htmlFor="cgi" className="block text-sm font-medium text-gray-700">
          CGI
        </label>
        <input
          type="text"
          name="cgi"
          id="cgi"
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
      </div>

      {/* Params Input */}
      <div>
        <label htmlFor="params" className="block text-sm font-medium text-gray-700">
          Params
        </label>
        <textarea
          name="params"
          id="params"
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          rows="4"
        />
      </div>

      {/* Result Display */}
      <div>
        <label htmlFor="result" className="block text-sm font-medium text-gray-700">
          Result
        </label>
        <textarea
          id="result"
          disabled
          value={result}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm bg-gray-100 focus:border-indigo-500 focus:ring-indigo-500"
          rows="4"
        />
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-2">
        <button
          type="button"
          onClick={handleSend}
          className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Send
        </button>
        <button
          type="button"
          onClick={handleAutoFocus}
          className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Auto Focus
        </button>
      </div>
    </div>
  );
}

export default App;
