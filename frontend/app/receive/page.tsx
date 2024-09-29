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
  const [verificationStatus, setVerificationStatus] = useState(''); // Verification status of the ID
  
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
    setVerificationStatus('File received!'); // Set status to file received
    setTimeout(() => setVerificationStatus(''), 3000); // Clear status after 3 seconds
  };

  {/* const handleDownload = () => {
    if (!imageUrl) return;
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = `image-${imageId}.jpg`; // Default filename for download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  */}

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

        <div className="w-full max-w-md mb-8">
              <hr className="bg-blue-500 border-0 h-1"></hr>
            </div>

        <div className=" pb-5">
          <p className="flex items-center justify-center text-xs text-gray-500 border border-blue-500 border-dashed text-center h-10 rounded-xl mb-16">
            To receive a file please enter the generated ID selection key.
          </p>
        </div>
        

        {/* ID Input Section */}
        <section className="h-40 w-auto flex">
          <div>
          
            <h2 className="text-xl font-semibold">ID Selection:</h2>
          
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"> 
              <div className="">
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
            </div>
          </div>
          
        </section>

        {/* Display Download Section */}
        <section className="relative h-80 rounded-xl overflow-hidden">
          <div className="absolute inset-0 blur-[4px]">
            <div className="h-full w-full ring ring-gray-200 ring-offset-2 ring-offset-slate-900 dark:ring-offset-slate-900 rounded-xl"></div>
          </div>
          <div className="relative h-full w-full p-4 z-10 flex items-center justify-center">
            {verificationStatus ? (
              <div className="p-2 bg-green-100 text-green-700 rounded-md">
                {verificationStatus}
              </div>
            ) : (
              <p className="text-gray-500 flex items-center">
                Waiting for verification status
                <span className="dot-1">.</span>
                <span className="dot-2">.</span>
                <span className="dot-3">.</span>
              </p>
            )}
          </div>
        </section>
      </main>
      <style jsx>{`
        @keyframes blink {
          0% {
            opacity: 0;
          }
          50% {
            opacity: 1;
          }
          100% {
            opacity: 0;
          }
        }

        .dot-1 {
          animation: blink 1.4s infinite both;
          animation-delay: 0.2s;
        }

        .dot-2 {
          animation: blink 1.4s infinite both;
          animation-delay: 0.4s;
        }

        .dot-3 {
          animation: blink 1.4s infinite both;
          animation-delay: 0.6s;
        }
      `}</style>
    </div>
  );
}

