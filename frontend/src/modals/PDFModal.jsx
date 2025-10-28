import PDFSvg from '../assets/pdf.svg';
import CROSSSvg from '../assets/cross.svg';
import RIGHTArrow from '../assets/right.svg';
import { useState } from 'react';
import InputBar from '../helpful-components/InputBar';
import { nanoid } from 'nanoid';
import useStore from '../stores/store';
import { useShallow } from 'zustand/shallow';
import modalStore from '../stores/modalStore';
import axios from 'axios';
import { createApiUrl } from '../config/api.js';
import LoadingModal from './LoadingModal';
import PDFProcessingModal from './PDFProcessingModal';
import setRequestData from '../config/setRequestData';
import flowStore from '../stores/flowStore';
import DataSourceSet from '../nodes/DataSourceSet';
import DataSourceSelect from '../global-components/DataSourceSelect';
import ErrorModal from './ErrorModal';
import errorStore from '../stores/errorStore';
import DELETESvg from '../assets/delete.svg';
import { useReactFlow } from '@xyflow/react';

const PDFModal = () => {
    const flowId = flowStore((s) => s.flow_id);
    const [file, setFile] = useState();
    const [isProcessing, setIsProcessing] = useState(false);
    const [processingStatus, setProcessingStatus] = useState('');
    const pushNode = modalStore((s) => s.pushNode);
    const popNode = modalStore((s) => s.popNode);
    // const csvAccept = ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
    const markdownAccept = 'text/markdown';
    const setFlowId = flowStore((s) => s.setFlow);
    const flow_id = flowStore((s) => s.flow_id);
    const setFlowName = flowStore((s) => s.setFlowName);
    const { fitView } = useReactFlow();
    const selector = (state) => ({
        trigger: state.trigger,
        setTrigger: state.setTrigger,
        nodes: state.nodes,
        edges: state.edges,
        setNodes: state.setNodes,
        setEdges: state.setEdges,
        setViewPort: state.setViewPort
    });

    const {
        trigger,
        setTrigger,
        nodes,
        edges,
        setNodes,
        setEdges,
        setViewPort
    } = useStore(useShallow(selector));
    const pdfAccept = 'application/pdf';
    const [processingType, setProcessingType] = useState('gpt');
    const addDataSource = (e) => {
        console.log('🚀 PDF Upload Started');
        console.log('   File:', file);
        console.log('   Processing Type:', processingType);
        console.log('   Flow ID:', flowId);
        
        const data = {
            file: file,
            processing_type: processingType
        };
        
        pushNode(PDFProcessingModal);
        const [url, body, headerConfig] = setRequestData('pdf', flowId, data);
        
        console.log('📡 Making API Request');
        console.log('   URL:', createApiUrl(url));
        console.log('   Body:', body);
        console.log('   Headers:', headerConfig);
        
        // Show processing message
        console.log('⏳ Processing PDF... This may take 1-3 minutes depending on file size and complexity.');
        
        const startTime = Date.now();
        
        axios
            .post(createApiUrl(url), body, {
                headers: {
                    'Content-Type': headerConfig
                },
                timeout: 300000, // 5 minutes timeout
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    console.log(`📤 Upload progress: ${percentCompleted}%`);
                }
            })
            .then((res) => {
                const processingTime = ((Date.now() - startTime) / 1000).toFixed(2);
                console.log('✅ PDF Upload Success:', res.data);
                console.log(`⏱️ Total processing time: ${processingTime} seconds`);
                setupNodes(res.data);
            })
            .catch((err) => {
                const processingTime = ((Date.now() - startTime) / 1000).toFixed(2);
                console.error('❌ PDF Upload Error:', err);
                console.error(`⏱️ Failed after: ${processingTime} seconds`);
                console.error('   Status:', err.response?.status);
                console.error('   Data:', err.response?.data);
                
                // Provide more specific error messages
                if (err.code === 'ECONNABORTED') {
                    console.error('⏰ Request timed out - PDF processing took too long');
                    setStatus(408);
                    setMsg('PDF processing timed out. Please try with a smaller file or different processing type.');
                } else if (err.response?.status === 500) {
                    console.error('🔧 Server error during PDF processing');
                    setStatus(500);
                    setMsg('Server error during PDF processing. Please try again or contact support.');
                } else if (err.response?.status === 400) {
                    console.error('📄 Invalid PDF file or processing parameters');
                    setStatus(400);
                    setMsg('Invalid PDF file or processing parameters. Please check your file and try again.');
                } else {
                    manageErrors(err);
                }
                
                popNode();
                pushNode(ErrorModal);
            });
    };
    
    const setupNodes = (data) => {
        if (data.flow_type === 'automatic') {
            manageAutomaticNode(data)
        } else {
            manageNodes(data)
        }
    }

    const manageAutomaticNode = (data) => {
        setupFlow(data)
    }
    const setupFlow = (data) => {
        console.log("SETUUUUUUUUUUUUUUUUUUP new flow")
        pushNode(LoadingModal);
        setFlowId(data.flow_id);
        console.log('DEDEDE', data);
        setFlowName(data.flow_name);
        const jsonString = JSON.stringify(data.mindmap_json)
        console.log(jsonString, "JSON STRINGGGGGGGGGGGGGG")
        if (jsonString.length > 0) {
            const flow = JSON.parse(jsonString);
            console.log('NODEEEEEEEEEE', flow.nodes);
            if (flow.nodes.length === 0 && flow.edges.length === 0) {
                console.log('not clled');
                setTrigger(!trigger);
                setViewPort(0, 0, 1);
                popNode();
            }
            if (flow) {
                const { x = 0, y = 0, zoom = 1.25 } = flow.viewport;
                setNodes(flow.nodes || []);
                setEdges(flow.edges || []);
                setViewPort(x, y, zoom);
                // fitView();
                console.log(
                    'FLow selecteed sadassssssssssssssssssssss',
                    flow_id,
                    data.flow_id,
                    nodes
                );
            } else {
                console.log('Flow error');
            }
        } else {
            setNodes([]);
            setEdges([]);
            // setViewPort({});
            fitView();
            popNode();
        }
        // setTrigger(!trigger);
    };

    const selector2 = (state) => ({
        status: state.status,
        message: state.message,
        setStatus: state.setStatus,
        setMsg: state.setMsg
    });
    const { status, message, setStatus, setMsg } = errorStore(
        useShallow(selector2)
    );

    const manageErrors = (err) => {
        console.log(err);
        console.log('Errroro', err.status);
        console.log('Errroross', err.response.statusText);
        setStatus(err.status);
        setMsg(err.response.statusText);
        popNode();
        pushNode(ErrorModal);
    };

    const manageNodes = (data) => {
        const node = {
            id: data.component_id,
            position: { x: 0, y: 0 },
            type: 'dataSource',
            data: {
                name: data.type,
                content: file.name,
                flow_id: flowId,
                prompt: 'Research Assistant',
                file: file,
                processing_type: processingType
            }
        };
        if (nodes.length === 0) {
            setNodes([node]);
        } else {
            const newArr = [...nodes, node];
            setNodes(newArr);
        }

        setTrigger(!trigger);
    };

    const handleFileUpload = (e) => {
        setFile(e.target.files[0]);
    };

    const handleChange = (e) => {
        setProcessingType(e.target.value);
    };

    return (
        <div className="modal-container">
            <div className="title">
                <div>
                    <img
                        src={PDFSvg}
                        alt="SQL SVG"
                    />
                    <p>Load A Pdf</p>
                </div>
                <img
                    src={CROSSSvg}
                    alt="Cross Svg"
                    onClick={(e) => popNode()}
                />
            </div>
            <div className="data-source-input">
                <label
                    htmlFor="filesUp"
                    className="data-source-set"
                >
                    <div>
                        <img
                            src={PDFSvg}
                            alt="image will be here"
                        />
                        {/* <p>Upload a CSV</p> */}
                        {file ? <p>{file.name}</p> : <p>Upload a PDF</p>}
                    </div>
                    <img
                        src={RIGHTArrow}
                        alt={'RIght arrow'}
                    />
                </label>
                <input
                    id="filesUp"
                    type="file"
                    accept={pdfAccept}
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileUpload(e)}
                />
            </div>
            {/* <InputBar data={{ type: "number", label: "Enter Column Row", placeholder: "eg: 1", setTableName: setHeaderRow }} /> */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <select
                    value={processingType}
                    onChange={handleChange}
                >
                    <option value="">Select Processing Type...</option>
                    <option value="gpt">AWS Bedrock (Claude Sonnet 3.5) - Recommended</option>
                    <option value="aws">AWS Textract - Fast OCR</option>
                    <option value="custom">Custom RAG - Advanced Analysis</option>
                </select>
                
                {processingType && (
                    <div style={{ 
                        fontSize: '0.8rem', 
                        color: 'var(--font-color)', 
                        opacity: '0.7',
                        padding: '0.5rem',
                        backgroundColor: 'var(--input-bar-color)',
                        borderRadius: '0.25rem'
                    }}>
                        {processingType === 'gpt' && '🤖 AI-powered analysis with Claude Sonnet 3.5. Best for comprehensive understanding and summaries.'}
                        {processingType === 'aws' && '⚡ Fast OCR text extraction using AWS Textract. Good for simple text extraction.'}
                        {processingType === 'custom' && '🔬 Advanced RAG processing with semantic chunking. Best for detailed analysis and Q&A.'}
                    </div>
                )}
            </div>
            <div className="buttons">
                <button
                    id="cancel"
                    onClick={(e) => pushNode(DataSourceSelect)}
                >
                    Back
                </button>
                {/* <button id="add" onClick={(e) => addDataSource(e)}>Add</button> */}

                {file && processingType ? (
                    <button
                        id="add"
                        style={{ opacity: '100%' }}
                        onClick={(e) => addDataSource(e)}
                    >
                        Add
                    </button>
                ) : (
                    <button
                        id="add"
                        style={{ opacity: '40%' }}
                        disabled
                    >
                        Add
                    </button>
                )}
            </div>
        </div>
    );
};

export default PDFModal;
