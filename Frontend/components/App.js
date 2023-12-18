// App.js
import React, { useState } from 'react';
import { TextField, Button, Box, Dropdown } from '@material-ui/core';
import ArchitecturePreview from './ArchitecturePreview';

function App() {
  const [prompt, setPrompt] = useState('');
  const [region, setRegion] = useState('us-east-1'); // Default region
  const [diagram, setDiagram] = useState(null);
  const regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']; // Example list

  const onInputChange = (event) => setPrompt(event.target.value);
  const onRegionChange = (event) => setRegion(event.target.value);
  const onSubmit = async () => {
    const generatedDiagram = await fetch('/api/generate-diagram', {
      method: 'POST',
      body: JSON.stringify({ prompt, region }),
    }).then((response) => response.json());
    setDiagram(generatedDiagram);
  };

  return (
    <Box>
      <h2>Cloud Architecture Generator</h2>
      <TextField
        label="Describe your desired application"
        variant="outlined"
        fullWidth
        multiline
        rows={4}
        value={prompt}
        onChange={onInputChange}
      />
      <Dropdown
        select
        label="Region"
        value={region}
        onChange={onRegionChange}
      >
        {regions.map((region) => (
          <MenuItem key={region} value={region}>
            {region}
          </MenuItem>
        ))}
      </Dropdown>
      <Button variant="contained" color="primary" onClick={onSubmit}>
        Generate Diagram
      </Button>
      {diagram && <ArchitecturePreview diagram={diagram} />}
    </Box>
  );
}

export default App;

// ... ArchitecturePreview.js implementation (similar to previous example)
