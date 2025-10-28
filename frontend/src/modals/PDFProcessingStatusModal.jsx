import LOGOSvg from "../assets/logo.svg";
import CROSSSvg from '../assets/cross.svg';
import { useState, useEffect } from 'react';

const PDFProcessingStatusModal = ({ onCancel, fileName }) => {
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
        if (timeElapsed < 5) {
            return "Uploading PDF file...";
        } else if (timeElapsed < 15) {
            return "Extracting text from PDF...";
        } else if (timeElapsed < 45) {
            return "Processing content with AI...";
        } else if (timeElapsed < 90) {
            return "Generating summary...";
        } else {
            return "Finalizing processing...";
        }
    };

    const getProgressPercentage = () => {
        if (timeElapsed < 5) return 10;
        if (timeElapsed < 15) return 25;
        if (timeElapsed < 45) return 60;
        if (timeElapsed < 90) return 85;
        return 95;
    };

    return (
        <div className="modal-container" style={{ minWidth: '400px' }}>
            <div className="title">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <img src={LOGOSvg} alt="logo" style={{ width: '24px', height: '24px' }} />
                    <p>Processing PDF</p>
                </div>
                {onCancel && (
                    <img
                        src={CROSSSvg}
                        alt="Cancel"
                        onClick={onCancel}
                        style={{ cursor: 'pointer' }}
                    />
                )}
            </div>
            
            <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '1.5rem',
                padding: '1rem 0'
            }}>
                {/* File info */}
                <div style={{ 
                    fontSize: '1rem', 
                    color: 'var(--font-color)',
                    opacity: '0.8'
                }}>
                    File: {fileName || 'Unknown'}
                </div>

                {/* Progress bar */}
                <div style={{ width: '100%' }}>
                    <div style={{ 
                        width: '100%', 
                        height: '8px', 
                        backgroundColor: 'var(--input-bar-color)', 
                        borderRadius: '4px',
                        overflow: 'hidden'
                    }}>
                        <div style={{ 
                            width: `${getProgressPercentage()}%`, 
                            height: '100%', 
                            backgroundColor: '#eece47',
                            transition: 'width 0.5s ease'
                        }} />
                    </div>
                    <div style={{ 
                        fontSize: '0.8rem', 
                        color: 'var(--font-color)',
                        opacity: '0.6',
                        marginTop: '0.5rem'
                    }}>
                        {getProgressPercentage()}% complete
                    </div>
                </div>

                {/* Status message */}
                <div style={{ 
                    fontSize: '1.1rem', 
                    fontWeight: '500',
                    color: 'var(--font-color)',
                    textAlign: 'center'
                }}>
                    {getStatusMessage()}{dots}
                </div>

                {/* Time elapsed */}
                <div style={{ 
                    fontSize: '0.9rem', 
                    color: 'var(--font-color)',
                    opacity: '0.6',
                    textAlign: 'center'
                }}>
                    Time elapsed: {formatTime(timeElapsed)}
                </div>

                {/* Warning for long processing */}
                {timeElapsed > 60 && (
                    <div style={{ 
                        fontSize: '0.8rem', 
                        color: 'var(--font-color)',
                        opacity: '0.5',
                        textAlign: 'center',
                        padding: '1rem',
                        backgroundColor: 'var(--input-bar-color)',
                        borderRadius: '0.5rem',
                        marginTop: '1rem'
                    }}>
                        <strong>Large or complex PDFs may take several minutes to process.</strong>
                        <br />
                        Please be patient while we extract and analyze the content.
                        <br />
                        You can cancel this operation if needed.
                    </div>
                )}

                {/* Cancel button */}
                {onCancel && timeElapsed > 30 && (
                    <div style={{ textAlign: 'center', marginTop: '1rem' }}>
                        <button
                            id="cancel"
                            onClick={onCancel}
                            style={{ 
                                padding: '0.5rem 1.5rem',
                                fontSize: '0.9rem'
                            }}
                        >
                            Cancel Processing
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PDFProcessingStatusModal;