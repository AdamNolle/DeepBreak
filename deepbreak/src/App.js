import './App.css';
import { UploadButton } from "@bytescale/upload-widget-react";

const options = {
  apiKey: "public_12a1yuP2GtyBHjybdh9CyYkHFP6k", // This is your API key.
  maxFileCount: 1
};

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          DEEPBREAK
        </p>
      </header>
      <div className='App-body'>
        <UploadButton options={options}
                      onComplete={files => alert(files.map(x => x.fileUrl).join("\n"))}>
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
