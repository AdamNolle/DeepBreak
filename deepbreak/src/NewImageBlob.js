import React, { useState, useEffect } from 'react';

function BlobImageComponent({ imageBlob }) {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    // Create a URL for the blob
    const newImageUrl = URL.createObjectURL(imageBlob);

    // Update state
    setImageUrl(newImageUrl);

    // Clean up by revoking the blob URL to avoid memory leaks
    return () => {
      URL.revokeObjectURL(newImageUrl);
    };
  }, [imageBlob]); // Recreate the URL if the blob changes

  return <img src={imageUrl} alt="Blob Image" />;
}

export default BlobImageComponent;
