"use client"; // This directive indicates client-side interactivity in App Router

import { useState, FormEvent } from 'react';

export default function Home() {

  const [message, setMessage] = useState('');

  interface WeatherResponse {
    temp_f: string;
    condition: string;
    err: string;
  }

  const handleSubmit = async (formData: any) => {

    const zipCode = formData.get('zipCode');

    if(!zipCode) {
      setMessage('Please enter a zip code.')
      return;
    }

    setMessage('Loading weather for ' + zipCode + '...');

    const weatherResponse = await getWeather(zipCode);

    if (weatherResponse.err) {
      setMessage(weatherResponse.err);
    } else {
      const weatherString = "The temperature is " + weatherResponse.temp_f + " and " + weatherResponse.condition;
      setMessage(weatherString);
    }
  };

  async function getWeather(zipCode: string): Promise<WeatherResponse> {

    try {
      const response = await fetch('http://localhost:8000/api/weather/?zip_code='+zipCode, {
        method: 'GET',
        headers: {
          "access-control-allow-origin": "http://localhost:3000",
          "access-control-allow-methods": "*",
          "access-control-allow-headers": "*",
        },
      });

      return await response.json() as WeatherResponse;
    } catch (error) {
      return {
        temp_f: '',
        condition: '',
        err: String(error),
      };
    }
  }

  return (
    <div>
    <h1>Weather App</h1>
    <form action={handleSubmit}>
      <label>Zip Code:</label>
      <input name="zipCode" maxLength={5}/>
      <br/>
      <button type="submit">Get Weather</button>
    </form>
    {message && <p className="message">{message}</p>}
    </div>
  );
}
