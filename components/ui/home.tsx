"use client";
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Input from "@/components/ui/input";
import { SendIcon, Inbox, InboxIcon,UserIcon,LogOut} from "lucide-react";
import Sidenav from './sidenav';



export default function Home() {
  interface FileProps {
    path?: string;
    lastModified: number;
    lastModifiedDate?: Date;
    name: string;
    size: number;
    type: string;
    webkitRelativePath: string;
  }

  const onDrop = useCallback((acceptedFiles: FileProps[]) => {
    // Handle file upload here and display the files
    console.log(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidenav />

      {/* Main Content */}
      <main className="flex-1 p-6">
        <header className="mb-8">
          <h1 className="text-3xl font-bold">Hello there! 👋</h1>
          <p className="text-gray-600">Looking to share files? We can help you with that, please select your file below!</p>
        </header>

        <section className="mb-12">
          <h2 className="text-xl font-semibold mb-4">Choose a starting point you like</h2>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-6 rounded-lg cursor-pointer ${
              isDragActive ? 'border-blue-500' : 'border-gray-300'
            }`}
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <p>Drop the files here ...</p>
            ) : (
              <p>Drag 'n' drop some files here, or click to select files</p>
            )}
          </div>
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-4">Current ID:</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Output files will be displayed here */}
          </div>
        </section>
      </main>
    </div>
  );
}