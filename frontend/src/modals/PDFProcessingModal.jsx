import LOGOSvg from "../assets/logo.svg";
import { useState, useEffect } from 'react';

const PDFProcessingModal = () => {
    const [dots, setDots] = useState('');
    const [timeElapsed, setTimeElapsed] = useState(0);

    useEffect(() => {
        // Animate dots
        const dotsInterval = setInterval(() => {
            setDots(prev => {
                if (prev === '...') return '';
                return prev + '.';
            });
        }, 500);

        // Track time elapsed
        const timeInterval = setInterval(() => {
            setTimeElapsed(prev => prev + 1);
        }, 1000);

        return () => {
            clearInterval(dotsInterval);
            clearInterval(timeInterval);
        };
    }, []);

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const getStatusMessage = () => {
        if (timeElapsed < 10) {
            return "Uploading PDF file...";
        } else if (timeElapsed < 30) {
            return "Extracting text from PDF...";
        } else if (timeElapsed < 60) {
            return "Processing content with AI...";
        } else if (timeElapsed < 120) {
            return "Generating summary...";
        } else {
            return "Almost done, please wait...";
        }
    };

    return (
        <div style={{ 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            gap: '1rem',
            padding: '2rem',
            textAlign: 'center'
        }}>
            <img src={LOGOSvg} alt="logo" id="logo" />
            <div style={{ 
                fontSize: '1.2rem', 
                fontWeight: '600',
                color: 'var(--font-color)'
            }}>
                Processing PDF{dots}
            </div>
            <div style={{ 
                fontSize: '1rem', 
                color: 'var(--font-color)',
                opacity: '0.8'
            }}>
                {getStatusMessage()}
            </div>
            <div style={{ 
                fontSize: '0.9rem', 
                color: 'var(--font-color)',
                opacity: '0.6'
            }}>
                Time elapsed: {formatTime(timeElapsed)}
            </div>
            {timeElapsed > 60 && (
                <div style={{ 
                    fontSize: '0.8rem', 
                    color: 'var(--font-color)',
                    opacity: '0.5',
                    maxWidth: '300px',
                    marginTop: '1rem'
                }}>
                    Large or complex PDFs may take several minutes to process. 
                    Please be patient while we extract and analyze the content.
                </div>
            )}
        </div>
    );
};

export default PDFProcessingModal;