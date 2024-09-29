
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Input from "@/components/ui/input";
import { SendIcon, Inbox, InboxIcon,UserIcon,LogOut} from "lucide-react";
import { DropEvent } from 'react-dropzone';

const sidenav = () => {
  return (
    <div className="flex min-h-screen bg-gray-100">
        {/* Sidebar for looks*/}
      <aside className="w-16 bg-white border-r hidden md:flex flex-col items-center py-4 space-y-4">
        <Button variant="ghost" size="icon" className="rounded-full">
            <a href='/'>
                <SendIcon className="h-6 w-6" />
            </a>
        </Button>
        <Button variant="ghost" size="icon" className="rounded-full">
            <a href='/receive'><InboxIcon className="h-6 w-6" /></a>
        </Button>
        <Button variant="ghost" size="icon" className="rounded-full">
            <a href="/log-in"><UserIcon className="h-6 w-6" /></a>
        </Button>

        <div className="flex-grow"></div>
        
        <Button variant="ghost" size="icon" className="rounded-full">
            <LogOut className="h-6 w-6" />
        </Button>
    </aside>

    </div>
  )
}

export default sidenav