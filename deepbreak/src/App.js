import './App.css';
import { UploadButton } from "@bytescale/upload-widget-react";
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Buffer } from 'buffer';
import BlobImageComponent from './NewImageBlob';

const options = {
  apiKey: "public_12a1yuP2GtyBHjybdh9CyYkHFP6k", // This is your API key.
  maxFileCount: 1
};

function App() {
  const [img, setImg] = useState("");
  const [base64img, setBase64Img] = useState("");
  const [imageSrc, setImageSrc] = useState(null);
  const [imgDownload, setImgDownload] = useState(null);
  const [isLoading, setIsLoading] = useState(null);

  const handleFileUpload = async (event) => {
    //ERROR CHECK
    if( event.length === 0 ) {return;}

    const imageURL = event[0].fileUrl;

    const file_ext_array = imageURL.split('.');
    const file_ext = file_ext_array[file_ext_array.length - 1];
    if (file_ext !== "jpg" && file_ext !== "jfif" && file_ext !== "png" && file_ext !== "webp" ) {
      alert(file_ext + " is currently not supported!");
      return;
    }
    
    console.log(imageURL);
    convertImageToBase64(imageURL)
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
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "image": base64Image }),
      });

      if (response.ok) {
        console.log("RETURNED")
        setIsLoading(false);
        const data = await response.json();
        console.log(data);
        // setImg(data.data[0].image); 
        const base64image = data.data[0].image;
        // console.log(data.data[0].image );
        // const imageBlob = base64ToBlob(data.data[0].image);
        const imageBlob = base64ToBlob(base64image);

        setImgDownload(imageBlob);
        // downloadBlob(imageBlob);
        
      } else {
        console.error('Backend processing failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  function base64ToBlob(base64, mimeType = 'image/jpeg') {
    const byteCharacters = atob(base64);
    const byteArrays = [];
  
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512);
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    const blob = new Blob(byteArrays, { type: mimeType })
    setImageSrc(URL.createObjectURL(blob));
    console.log(blob);
    // return new Blob(byteArrays, { type: mimeType });
    return blob;
  }

  function downloadBlob(blob, filename = 'download.jpg') {
    console.log(blob)
    if( !blob ){
      return;
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a); // Append anchor to body.
    a.click();
    document.body.removeChild(a); // Remove anchor from body
    URL.revokeObjectURL(url); // Clean up URL object
  }

  return (
    <div className="App">
      <header className="App-header">
        <h>
          DEEPBREAK
        </h>
      </header>
      <div className='App-body'>
        <p>
          Make sure that the image is not too low of a resolution!
        </p>
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
      </div>
      <div className='App-image'>

        {imageSrc && isLoading ? (<div className='spinner'></div>)
        :
        (imageSrc ? <img src={imageSrc} alt="TEST" onClick={() => downloadBlob(imgDownload)}/> : <div></div>)}
      </div>
      
    </div>
  );
}

export default App;
