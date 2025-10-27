import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError

# Page configuration
st.set_page_config(
    page_title="S3 Video Analyzer",
    page_icon="??",
    layout="wide"
)

# Initialize session state
if 'videos' not in st.session_state:
    st.session_state.videos = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# AWS Configuration
S3_BUCKET_NAME = "sks-videoai"
S3_VIDEOS_PATH = "videos"
AWS_REGION = "us-east-1"  # Region where Pegasus is available

def initialize_aws_clients():
    """Initialize AWS S3 and Bedrock clients"""
    try:
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        bedrock_runtime_client = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        return s3_client, bedrock_runtime_client
    except Exception as e:
        st.error(f"Error initializing AWS clients: {str(e)}")
        return None, None

def list_s3_videos(s3_client):
    """List all videos in the S3 bucket"""
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=f"{S3_VIDEOS_PATH}/"
        )
        
        if 'Contents' in response:
            # Filter out the folder object and get only video files
            videos = [
                obj['Key'] for obj in response['Contents']
                if not obj['Key'].endswith('/')
            ]
            return videos
        else:
            return []
    except ClientError as e:
        st.error(f"Error listing S3 objects: {str(e)}")
        return []

def get_aws_account_id():
    """Get AWS account ID"""
    try:
        sts_client = boto3.client('sts')
        return sts_client.get_caller_identity()['Account']
    except Exception:
        return None

def analyze_video(bedrock_runtime_client, video_s3_uri, prompt, temperature=0):
    """Analyze video using AWS Bedrock Pegasus model"""
    try:
        # Get AWS account ID for bucketOwner
        account_id = get_aws_account_id()
        
        if not account_id:
            return "Error: Unable to retrieve AWS account ID"
        
        request_body = {
            "inputPrompt": prompt,
            "mediaSource": {
                "s3Location": {
                    "uri": video_s3_uri,
                    "bucketOwner": account_id
                }
            },
            "temperature": temperature
        }
        
        response = bedrock_runtime_client.invoke_model(
            modelId="us.twelvelabs.pegasus-1-2-v1:0",
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response["body"].read())
        return response_body.get("message", "No response received")
    except ClientError as e:
        return f"Error analyzing video: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Main UI
st.title("?? S3 Video Analyzer with AWS Bedrock")
st.markdown("Analyze videos stored in S3 using the Pegasus model")

# Sidebar for configuration
with st.sidebar:
    st.header("?? Configuration")
    st.info(f"**Bucket:** {S3_BUCKET_NAME}\n**Path:** {S3_VIDEOS_PATH}/\n**Region:** {AWS_REGION}")
    
    if st.button("?? Refresh Video List", use_container_width=True):
        st.session_state.videos = []
        st.session_state.analysis_result = None
        st.rerun()
    
    st.divider()
    st.markdown("### About")
    st.markdown("This app analyzes videos from S3 using AWS Bedrock's Pegasus model.")

# Initialize AWS clients
s3_client, bedrock_runtime_client = initialize_aws_clients()

if s3_client and bedrock_runtime_client:
    # Load videos if not already loaded
    if not st.session_state.videos:
        with st.spinner("Loading videos from S3..."):
            st.session_state.videos = list_s3_videos(s3_client)
    
    if st.session_state.videos:
        st.success(f"? Found {len(st.session_state.videos)} video(s) in S3")
        
        # Video selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_video = st.selectbox(
                "Select a video to analyze:",
                st.session_state.videos,
                format_func=lambda x: x.split('/')[-1]  # Show only filename
            )
        
        with col2:
            st.metric("Video Path", selected_video.split('/')[-1])
        
        # Display S3 URI
        video_s3_uri = f"s3://{S3_BUCKET_NAME}/{selected_video}"
        st.code(video_s3_uri, language=None)
        
        st.divider()
        
        # Analysis section
        st.subheader("?? Video Analysis")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            prompt = st.text_area(
                "Enter your prompt:",
                value="What is the video about?",
                height=100,
                help="Ask any question about the video content"
            )
        
        with col2:
            temperature = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                help="Controls randomness in the response"
            )
        
        # Example prompts
        with st.expander("?? Example Prompts"):
            st.markdown("""
            - What is the video about?
            - Summarize the key points in this video
            - Describe the main activities shown in the video
            - What objects or people appear in this video?
            - Provide a detailed analysis of the video content
            - What is the mood or tone of this video?
            """)
        
        # Analyze button
        if st.button("?? Analyze Video", type="primary", use_container_width=True):
            if prompt.strip():
                with st.spinner("Analyzing video... This may take a moment."):
                    result = analyze_video(
                        bedrock_runtime_client,
                        video_s3_uri,
                        prompt,
                        temperature
                    )
                    st.session_state.analysis_result = result
            else:
                st.warning("Please enter a prompt before analyzing.")
        
        # Display results
        if st.session_state.analysis_result:
            st.divider()
            st.subheader("?? Analysis Result")
            st.markdown(st.session_state.analysis_result)
            
            # Download result
            st.download_button(
                label="?? Download Result",
                data=st.session_state.analysis_result,
                file_name=f"analysis_{selected_video.split('/')[-1]}.txt",
                mime="text/plain"
            )
    else:
        st.warning("?? No videos found in the specified S3 path.")
        st.info("Please ensure videos are uploaded to the correct S3 bucket and path.")
else:
    st.error("? Failed to initialize AWS clients. Please check your AWS credentials and configuration.")
    st.info("""
    **Troubleshooting:**
    - Ensure AWS credentials are configured (via `~/.aws/credentials` or environment variables)
    - Verify you have permissions to access S3 and Bedrock services
    - Confirm the region supports the Pegasus model
    """)