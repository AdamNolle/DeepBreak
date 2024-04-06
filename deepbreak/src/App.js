import './App.css';
import { UploadButton } from "@bytescale/upload-widget-react";
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Buffer } from 'buffer';

const options = {
  apiKey: "public_12a1yuP2GtyBHjybdh9CyYkHFP6k", // This is your API key.
  maxFileCount: 1
};

function App() {
  const [img, setImg] = useState("");

  const handleFileUpload = async (event) => {
    const imageURL = event[0].fileUrl;
    if( !imageURL ) {return;}

    console.log(imageURL);
    convertImageToBase64(imageURL)
    .then(base64String => console.log(base64String))
    .then(base64String => sendImageToBackend(base64String))

  }

  async function convertImageToBase64(url) {
    try {
      const response = await fetch(url);
      const arrayBuffer = await response.arrayBuffer();
      const base64 = Buffer.from(arrayBuffer).toString('base64');
      return `data:${response.headers['content-type']};base64,${base64}`;
    } catch (error) {
      console.error('Error converting image to Base64:', error);
      return null;
    }
  }

  const sendImageToBackend = async (base64Image) => {
    console.log('sendImageToBackend call');
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: base64Image }),
      });

      if (response.ok) {
        const data = await response.json();
        setImg(data.img); 
      } else {
        console.error('Backend processing failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>
          DEEPBREAK
        </p>
      </header>
      <div className='App-body'>
        <UploadButton options={options}
                      onComplete={e => {
                        console.log(e);
                        handleFileUpload(e);
                      }}>
          {({onClick}) =>
            <button onClick={onClick}>
              Upload a file...
            </button>
          }
        </UploadButton>
        <img src="https://i.pinimg.com/originals/e0/50/29/e05029add9bfd9db2db88264b375257a.jpg"/>
      </div>
    </div>
  );
}

export default App;
