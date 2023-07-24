import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet'; 
import axios from 'axios';

function FileUploadComponent() {
  const [file, setFile] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);

  const submitFile = () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    // axios.post('http://localhost:4000/process/', formData, {
    const baseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
    // empty string as default
    axios.post(`${baseUrl}/process/`, formData, {
    // axios.post('http://neuralnavigate-prod-env.eba-jpr6yccf.us-west-1.elasticbeanstalk.com/process/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      setTopics(response.data.topics);
    })
    .finally(() => setLoading(false));
  };

  useEffect(() => {
    const handleResize = () => {
      const title = document.getElementById("upload-text");
      if (title) {
        const windowWidth = window.innerWidth;
        if (windowWidth < 700) {
          title.style.fontSize = "16px";
        } else if (windowWidth < 1000) {
          title.style.fontSize = "22px";
        } else {
          title.style.fontSize = "30px";
        }
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="container">
      <Helmet>
        <title>NeuralNavigate</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap" rel="stylesheet" />
      </Helmet>
      <h1 id="upload-text">Upload your Machine Learning & AI Research Paper</h1>
      <div className="upload-section">
        <input type="file" accept=".pdf" onChange={event => setFile(event.target.files[0])} />
        <button id="uploadButton" onClick={submitFile}>{loading ? "Loading..." : "Generate Graph"}</button>
      </div>
      <div id="topicsContainer">
        {topics.map((topic, i) => (
          <button key={i} onClick={() => {/* handle button click here */}}>
            {topic}
          </button>
        ))}
      </div>
    </div>
  );
}

export default FileUploadComponent;
