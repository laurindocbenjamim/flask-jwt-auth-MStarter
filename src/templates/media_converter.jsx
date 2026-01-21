import React, { useState } from 'react';
import { Upload, Music, ArrowRight, Download, XCircle, CheckCircle, Loader2 } from 'lucide-react'; // Using lucide-react for icons

// Main App component
const App = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [targetFormat, setTargetFormat] = useState('mp3'); // Default target format
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    // Define allowed output formats for the dropdown
    const allowedOutputFormats = [
        { value: 'mp3', label: 'MP3' },
        { value: 'wav', label: 'WAV' },
        { value: 'flac', label: 'FLAC' },
        { value: 'ogg', label: 'OGG' },
        { value: 'm4a', label: 'M4A (Audio)' }
    ];

    // Handle file input change
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setMessage(''); // Clear any previous messages
        setMessageType('');
    };

    // Handle target format selection change
    const handleFormatChange = (event) => {
        setTargetFormat(event.target.value);
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent default form submission

        if (!selectedFile) {
            setMessage('Please select a file to convert.');
            setMessageType('error');
            return;
        }

        setLoading(true);
        setMessage('');
        setMessageType('');

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('target_format', targetFormat);

        try {
            const response = await fetch('http://127.0.0.1:5000/convert', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                // If conversion is successful, trigger file download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = selectedFile.name.split('.').slice(0, -1).join('.') + '.' + targetFormat;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);

                setMessage('File converted and downloaded successfully!');
                setMessageType('success');
            } else {
                // If there's an error, parse the JSON response
                const errorData = await response.json();
                setMessage(errorData.message || 'An unknown error occurred during conversion.');
                setMessageType('error');
            }
        } catch (error) {
            setMessage(`Network error: ${error.message}. Please check if the backend server is running.`);
            setMessageType('error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-700 to-blue-600 font-inter">
            <div className="bg-white bg-opacity-15 backdrop-blur-lg rounded-2xl shadow-xl p-8 w-full max-w-md text-center text-white border border-white border-opacity-30">
                <h1 className="text-4xl font-bold mb-4 flex items-center justify-center">
                    <Music className="mr-3 h-10 w-10" /> Media Converter
                </h1>
                <p className="mb-6 text-lg opacity-80">Convert your audio and video files to various audio formats.</p>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* File Upload */}
                    <div className="relative border-2 border-dashed border-white border-opacity-50 rounded-xl p-6 cursor-pointer hover:border-opacity-80 transition-all duration-300">
                        <input
                            type="file"
                            onChange={handleFileChange}
                            className="absolute inset-0 opacity-0 cursor-pointer"
                            accept=".m4a,.mp4,.wav,.mp3,.flac,.ogg,.avi,.mov" // Accept common audio/video formats
                        />
                        <div className="flex flex-col items-center justify-center">
                            <Upload className="h-12 w-12 text-white opacity-70 mb-3" />
                            <p className="text-lg font-semibold">
                                {selectedFile ? selectedFile.name : 'Drag & Drop or Click to Upload File'}
                            </p>
                            <p className="text-sm opacity-70 mt-1">
                                (M4A, MP4, WAV, MP3, FLAC, OGG, AVI, MOV)
                            </p>
                        </div>
                    </div>

                    {/* Target Format Selection */}
                    <div className="flex items-center justify-center space-x-4">
                        <span className="text-lg font-semibold">Convert to:</span>
                        <select
                            value={targetFormat}
                            onChange={handleFormatChange}
                            className="p-3 rounded-lg bg-white bg-opacity-20 border border-white border-opacity-30 text-white focus:outline-none focus:ring-2 focus:ring-blue-400 appearance-none pr-8"
                            style={{backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E")`, backgroundRepeat: 'no-repeat', backgroundPosition: 'right 0.75rem center', backgroundSize: '16px 12px'}}
                        >
                            {allowedOutputFormats.map((format) => (
                                <option key={format.value} value={format.value} className="bg-gray-800 text-white">
                                    {format.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-300 flex items-center justify-center"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <Loader2 className="animate-spin mr-3 h-5 w-5" />
                                Converting...
                            </>
                        ) : (
                            <>
                                <ArrowRight className="mr-3 h-5 w-5" />
                                Start Conversion
                            </>
                        )}
                    </button>
                </form>

                {/* Message Display */}
                {message && (
                    <div className={`mt-6 p-4 rounded-xl flex items-center justify-center text-left ${messageType === 'success' ? 'bg-green-500 bg-opacity-80' : 'bg-red-500 bg-opacity-80'}`}>
                        {messageType === 'success' ? <CheckCircle className="mr-3 h-6 w-6" /> : <XCircle className="mr-3 h-6 w-6" />}
                        <p>{message}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;
