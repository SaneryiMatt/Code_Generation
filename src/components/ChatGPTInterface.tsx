"use client";

import React, { useState, useRef, ChangeEvent, ReactNode } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PlusCircle, Send, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import '../app/globals.css'; // 导入全局样式

const ChatGPTInterface = () => {
  const [formData, setFormData] = useState({
    system_name: '',
    save_path: '',
    code_language: '',
    description: '',
  });
  const [features, setFeatures] = useState([{ name: '', description: '' }]);
  const [receivedMessages, setReceivedMessages] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target as HTMLInputElement;
    const files = (e.target as HTMLInputElement).files;

    if (name === 'save_path' && files && files.length > 0) {
      setFormData(prev => ({ ...prev, [name]: files[0].name }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSelectChange = (value: string) => {
    setFormData(prev => ({ ...prev, code_language: value }));
  };

  const handleFeatureChange = (index: number, field: 'name' | 'description', value: string) => {
    const newFeatures = [...features];
    newFeatures[index][field] = value;
    setFeatures(newFeatures);
  };

  const addFeature = () => {
    setFeatures(prev => [...prev, { name: '', description: '' }]);
  };

  const deleteFeature = (index: number) => {
    setFeatures(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    const payload = {
      system_name: formData.system_name,
      save_path: formData.save_path,
      code_language: formData.code_language,
      description: formData.description,
      features: features.map((feature) => ({
        feature_name: feature.name,
        feature_description: feature.description
      }))
    };

    fetch('http://localhost:5000/api/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.status === "success") {
          setReceivedMessages(prev => [
            ...prev, 
            "### Received Data:\n" + JSON.stringify(data.data_received, null, 2),
            "### Markdown Examples:\n" + data.markdown_examples
          ]);
        } else {
          alert("Error in submission! Check your data.");
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert("Network error! Please try again later.");
      });
  };

  return (
    <div className="flex h-screen">
      {/* 左侧 - ChatGPT 聊天窗口 */}
      <div className="flex flex-col w-1/2 p-4 border-r border-gray-200">
        <div className="h-full bg-gray-100 rounded-lg p-4 overflow-y-auto flex-grow message-container">
          {receivedMessages.map((msg, index) => (
            <div key={index} className="mb-4 p-2 bg-white rounded-lg border border-gray-300 shadow-sm">
              <div className="markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({ node, inline, className, children, ...props }: { node: any, inline?: boolean, className?: string, children: ReactNode }) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <SyntaxHighlighter
                          style={oneDark}
                          language={match[1]}
                          PreTag="div"
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {msg}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 右侧 - 表单 */}
      <div className="flex flex-col w-1/2 p-4 bg-white border-l border-gray-200 form-container">
        <h2 className="text-2xl font-bold mb-4">Configuration</h2>
        <div className="space-y-4 flex-grow">
          <div>
            <Label htmlFor="system_name">System Name</Label>
            <Input
              id="system_name"
              name="system_name"
              value={formData.system_name}
              onChange={handleInputChange}
              className="border p-2 mb-4"
            />
          </div>
          <div>
            <Label htmlFor="save_path">Save Path</Label>
            <div className="flex">
              <Input
                id="save_path"
                name="save_path"
                value={formData.save_path}
                onChange={handleInputChange}
                readOnly
                className="border p-2"
              />
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleInputChange}
                //webkitdirectory="true"
                multiple
              />
              <Button onClick={() => fileInputRef.current?.click()} className="ml-2 bg-blue-500 text-white">
                Choose
              </Button>
            </div>
          </div>
          <div>
            <Label htmlFor="code_language">Code Language</Label>
            <Select onValueChange={handleSelectChange}>
              <SelectTrigger>
                <SelectValue placeholder="Select a language" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="python">Python</SelectItem>
                <SelectItem value="java">Java</SelectItem>
                <SelectItem value="cpp">C++</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              className="border p-2"
            />
          </div>
          <div>
            <Label htmlFor="features">Features</Label>
            {features.map((feature, index) => (
              <div key={index} className="mt-2 space-y-2">
                <div className="flex items-center space-x-2">
                  <Input
                    placeholder={`Feature ${index + 1} Name`}
                    value={feature.name}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => handleFeatureChange(index, 'name', e.target.value)}
                    className="flex-grow border p-2"
                  />
                  <Button variant="destructive" size="icon" onClick={() => deleteFeature(index)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
                <Textarea
                  placeholder={`Feature ${index + 1} Description`}
                  value={feature.description}
                  onChange={(e: ChangeEvent<HTMLTextAreaElement>) => handleFeatureChange(index, 'description', e.target.value)}
                  className="border p-2"
                />
              </div>
            ))}
            <Button onClick={addFeature} className="mt-2 bg-green-500 text-white">
              <PlusCircle className="mr-2 h-4 w-4" /> Add Feature
            </Button>
          </div>
          <Button onClick={handleSubmit} className="w-full bg-blue-500 text-white">
            <Send className="mr-2 h-4 w-4" /> Send
          </Button>
        </div>
      </div>
    </div>
  );
}

export default ChatGPTInterface;
