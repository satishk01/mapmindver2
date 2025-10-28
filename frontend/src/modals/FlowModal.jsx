import CROSSSvg from '../assets/cross.svg';
import useStore from '../stores/store';
import { useShallow } from 'zustand/shallow';
import modalStore from '../stores/modalStore';
import axios from 'axios';
import { createApiUrl } from '../config/api.js';
import flowStore from '../stores/flowStore';
import ErrorModal from './ErrorModal';
import errorStore from '../stores/errorStore';

const FlowModal = ({isDrawer, setIsDrawer, isViewModal, setIsViewFlowModal}) => {
    console.log('🎯 FlowModal rendered');
    console.log('   isDrawer:', isDrawer);
    console.log('   isViewModal:', isViewModal);
   const selector = (state) => ({
        trigger: state.trigger,
        setTrigger: state.setTrigger,
        nodes: state.nodes,
        setNodes: state.setNodes,
        edges: state.edges,
        setEdges: state.setEdges,
        viewport: state.viewport,
        setViewPort: state.setViewPort
    });

    const {
        trigger,
        setTrigger,
        setNodes,
        setEdges,
        setViewPort
    } = useStore(useShallow(selector));
    const setFlow = flowStore((s) => s.setFlow);
    const setFlowName = flowStore((s) => s.setFlowName);
    const setFlowType = flowStore((s) => s.setFlowType)
    const popNode = modalStore((s) => s.popNode);
    const pushNode = modalStore((s) => s.pushNode);

    const createNewFlow = () => {
        console.log('📝 Creating Manual Flow');
        setIsDrawer(false)
        setIsViewFlowModal(false)
        const data = {
            flow_name: 'New Flow',
            summary: 'Flow is empty',
            flow_json: '',
            flow_type: 'manual'
        };
        
        console.log('📡 Sending flow creation request:', data);
        axios
            .post(createApiUrl("create-flow"), data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((res) => {
                console.log('✅ Flow creation success:', res.data);
                setupNewFlow(res);
            })
            .catch((err) => {
                console.error('❌ Flow creation error:', err);
                manageErrors(err);
            });
    };

    const createAutomaticFlow = () => {
        console.log('🤖 Creating Automatic Flow');
        setIsDrawer(false)
        setIsViewFlowModal(false)
        const data = {
            flow_name: 'New Flow',
            summary: 'Flow is empty',
            flow_json: '',
            flow_type: 'automatic'
        };
        
        console.log('📡 Sending automatic flow creation request:', data);
        axios
            .post(createApiUrl("create-flow"), data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((res) => {
                console.log('✅ Automatic flow creation success:', res.data);
                setupNewFlow(res);
            })
            .catch((err) => {
                console.error('❌ Automatic flow creation error:', err);
                manageErrors(err);
            });
    };


    const setupNewFlow = (res) => {
        console.log("SERVER RESPONSE", res.data)
        setFlow(res.data.flow_id);
        setFlowType(res.data.flow_type)
        setIsDrawer(!isDrawer);
        setNodes([]);
        setEdges([]);
        setViewPort({});
        setFlowName('New Flow');
        setTrigger(!trigger);
    };

    const selector2 = (state) => ({
        status: state.status,
        message: state.message,
        setStatus: state.setStatus,
        setMsg: state.setMsg
    });
    const { setStatus, setMsg } = errorStore(
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
    return (
        <div className='container'>
            <div className="modal-container">
                <div className="title">
                    <div>
                        <p>Select Flow Type</p>
                    </div>
                    <img
                        src={CROSSSvg}
                        alt="Cross Svg"
                        onClick={() => setIsViewFlowModal(false)}
                    />
                </div>
                <div className="buttons">
                    <button
                        id="cancel"
                        onClick={() => createAutomaticFlow()}
                    >
                        Automatic
                    </button>

                    <button
                        id="add"
                        style={{ opacity: '100%' }}
                        onClick={() => createNewFlow()}
                    >
                        Manual
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FlowModal;