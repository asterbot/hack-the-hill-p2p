"use client";
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Input from "@/components/ui/input";
import { SendIcon, Inbox, InboxIcon,UserIcon,LogOut} from "lucide-react";
import { DropEvent } from 'react-dropzone';
import Sidenav from '@/components/ui/sidenav';



export default function page() {


  interface AcceptedFile {
    path?: string;
    lastModified: number;
    lastModifiedDate?: Date;
    name: string;
    size: number;
    type: string;
    webkitRelativePath: string;
  }

  const onDrop = useCallback((acceptedFiles: AcceptedFile[], fileRejections: any[], event: DropEvent) => {
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

        <section className="">
          <h2 className="text-xl font-semibold mb-4 ">ID Selection:</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Output files will be displayed here */}
            </div>
            <div className="mt-4">
              <input
                type="text"
                placeholder="Please Enter the ID ..."
                className="border border-gray-300 rounded p-2 mr-2"
              />
              <button className="bg-blue-500 text-white rounded p-2">
                Submit
              </button>
            </div>
        </section>  

        {/* Received files */}
        <section className="">
          <h2 className="text-xl font-semibold mb-4 mt-60">Received: </h2>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-6 rounded-lg cursor-pointer flex items-center justify-center h-96 ${
              isDragActive ? 'border-blue-500' : 'border-gray-300'
            }`}
          >
              {/* Modification*/}
              <h1 className="text-5xl"> <b>File...</b></h1>
          </div>
        </section>

      </main>
    </div>
  );
}