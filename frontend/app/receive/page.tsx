"use client";
import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Input from "@/components/ui/input";
import { SendIcon, Inbox, InboxIcon, UserIcon, LogOut } from "lucide-react";
import { DropEvent } from "react-dropzone";
import Sidenav from "@/components/ui/sidenav";

interface AcceptedFile {
  path?: string;
  lastModified: number;
  lastModifiedDate?: Date;
  name: string;
  size: number;
  type: string;
  webkitRelativePath: string;
}

export default function Page() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageId, setImageId] = useState<string>("");
  
  // Function to upload files to the API
  const uploadID = async () => {    
    try {
      const response = await fetch("http://127.0.0.1:5000/receive-token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ final_id: imageId }), // Send the image ID in the body
      });


      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.download_name;  // Name of the downloaded file
        document.body.appendChild(a);
        a.click();
        a.remove();

        
      } else {
        console.error("Failed to upload ID");
      }
    } catch (error) {
      console.error("Error uploading ID:", error);
    }
    };
  

  // Function to handle fetching the image by ID
  const handleFetchImage = async () => {
    if (!imageId) return;
    console.log("Image ID:", imageId);
    uploadID();
  };

  // Handle downloading the image
  const handleDownload = () => {
    if (!imageUrl) return;
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = `image-${imageId}.jpg`; // Default filename for download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const onDrop = useCallback(
    (acceptedFiles: AcceptedFile[], fileRejections: any[], event: DropEvent) => {
      // Handle file upload here and display the files
      console.log(acceptedFiles);
    },
    []
  );


  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidenav />

      {/* Main Content */}
      <main className="flex-1 p-6">
        <header className="mb-8">
          <h1 className="text-3xl font-bold">Hello there! 👋</h1>
          <p className="text-gray-600">
            Looking to share files? We can help you with that, please select your file below!
          </p>
        </header>

        {/* ID Input Section */}
        <section className="">
          <h2 className="text-xl font-semibold mb-4">ID Selection:</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
          <div className="mt-4">
            <input
              type="text"
              value={imageId}
              onChange={(e) => setImageId(e.target.value)}
              placeholder="Please Enter the ID ..."
              className="border border-gray-300 rounded p-2 mr-2"
            />
            <button onClick={handleFetchImage} className="bg-blue-500 text-white rounded p-2">
              Submit
            </button>
          </div>
        </section>

        {/* Display and Download Section */}
        <section className="">
          <h2 className="text-xl font-semibold mb-4 mt-60">Received Image: </h2>
          {imageUrl ? (
            <div className="flex flex-col items-center">
              {/* Displaying the image */}
              <img
                src={imageUrl}
                alt="Fetched by ID"
                className="max-w-full h-auto rounded-lg shadow-md mb-4"
              />
              
              {/* Download button */}
              <button
                onClick={handleDownload}
                className="bg-green-500 text-white rounded p-2"
              >
                Download Image
              </button>
            </div>
          ) : (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed p-6 rounded-lg flex items-center justify-center h-96 ${
                isDragActive ? "border-blue-500" : "border-gray-300"
              }`}
            >
              <h1 className="text-5xl">
                <b>No Image Available...</b>
              </h1>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
