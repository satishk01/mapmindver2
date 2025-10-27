# AWS Bedrock Migration Summary

## Overview

Your GenAI Mind Map Flow Builder application has been successfully updated to support AWS Bedrock models as an alternative to OpenAI and Google Gemini models. This migration provides enhanced privacy, enterprise-grade security, and seamless AWS integration.

## Changes Made

### 1. Backend Code Updates (`backend/app.py`)

#### New Environment Variables
- `USE_BEDROCK_ONLY`: Toggle between model sets (true/false)
- `AWS_REGION`: AWS region for Bedrock services (default: us-east-1)

#### New Functions Added
- `get_aws_account_id()`: Retrieves AWS account ID for Pegasus
- `analyze_content_with_pegasus()`: Video/audio analysis using Pegasus
- `generate_text_with_claude()`: Text generation using Claude Sonnet 3.5
- `analyze_image_with_claude()`: Image analysis using Claude Sonnet 3.5

#### Updated Functions
- **Image Processing**: Now supports Claude Sonnet 3.5 for image analysis
- **Audio Processing**: Now supports Pegasus for audio analysis
- **Video Processing**: Now supports Pegasus for video analysis
- **YouTube Processing**: Now supports Pegasus for YouTube analysis
- **QA Functions**: Updated IMG_QA, AUDIO_QA, VIDEO_QA, YOUTUBE_QA to use Bedrock models

#### Model Initialization
- Conditional initialization of Google models based on `USE_BEDROCK_ONLY` flag
- Custom LLM wrapper for Claude to maintain compatibility with existing code
- Bedrock runtime client initialization

### 2. Configuration Files

#### New Files Created
- `backend/.env.example`: Template for environment variables
- `backend/BEDROCK_MIGRATION.md`: Detailed migration guide
- `backend/test_bedrock.py`: Configuration testing script
- `backend/switch_models.py`: Model switching utility
- `AWS_EC2_DEPLOYMENT.md`: Complete EC2 deployment guide

#### Updated Files
- `README.md`: Added Bedrock information and setup instructions
- `backend/requirements.txt`: Ensured AWS SDK compatibility

### 3. Model Mapping

| Function | Original Model | Bedrock Alternative |
|----------|----------------|-------------------|
| Text Processing | OpenAI GPT-4o | Claude Sonnet 3.5 |
| Image Analysis | Google Gemini 2.0 Flash | Claude Sonnet 3.5 |
| Video Analysis | Google Gemini 2.0 Flash | Pegasus |
| Audio Analysis | Google Gemini 2.0 Flash | Pegasus |
| YouTube Analysis | Google Vertex AI Gemini | Pegasus |

## How to Use

### Option 1: Keep Current Models (Default)
```bash
# In your .env file
USE_BEDROCK_ONLY=false
```
Application continues to use OpenAI + Google Gemini models.

### Option 2: Switch to AWS Bedrock Models
```bash
# In your .env file
USE_BEDROCK_ONLY=true
AWS_REGION=us-east-1
```

### Quick Setup Commands

```bash
# Switch to Bedrock models
cd backend
python switch_models.py bedrock

# Test Bedrock configuration
python test_bedrock.py

# Switch back to OpenAI/Gemini
python switch_models.py openai
```

## AWS Requirements

### 1. IAM Permissions
Your AWS role/user needs:
- `bedrock:InvokeModel` for Claude and Pegasus
- `s3:GetObject`, `s3:PutObject` for media files
- `sts:GetCallerIdentity` for account ID retrieval

### 2. Model Access
Request access in AWS Bedrock console:
- **Claude Sonnet 3.5**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Pegasus**: `us.twelvelabs.pegasus-1-2-v1:0`

### 3. S3 Bucket
- Existing S3 bucket for file storage
- Proper permissions for Bedrock to access media files

## Deployment Options

### Local Development
1. Set environment variables in `.env`
2. Configure AWS credentials (AWS CLI or environment variables)
3. Test with `python test_bedrock.py`

### AWS EC2 Deployment (Recommended)
1. Create IAM role with Bedrock permissions
2. Launch EC2 instance with the role attached
3. Follow the complete deployment guide in `AWS_EC2_DEPLOYMENT.md`

## Benefits of AWS Bedrock

### Privacy & Security
- Data stays within AWS infrastructure
- No third-party API calls for AI processing
- Enterprise-grade security and compliance

### Cost Management
- Pay-per-use pricing
- Integrated with AWS billing
- No separate API subscriptions needed

### Performance
- Reduced latency with regional deployment
- Optimized for AWS infrastructure
- Better integration with other AWS services

### Enterprise Features
- IAM role-based access control
- CloudTrail logging for audit trails
- VPC deployment options
- Compliance certifications (SOC, HIPAA, etc.)

## Testing Your Setup

### 1. Configuration Test
```bash
cd backend
python test_bedrock.py
```

### 2. Application Test
1. Start the application
2. Create a new flow
3. Upload different file types (image, video, audio)
4. Verify processing works with Bedrock models
5. Check logs for any errors

### 3. Performance Comparison
- Compare response times between model sets
- Monitor token usage and costs
- Test with different file sizes and types

## Troubleshooting

### Common Issues

1. **Model Access Denied**
   - Solution: Request model access in Bedrock console
   - Check IAM permissions

2. **Region Errors**
   - Solution: Verify models are available in your region
   - Update AWS_REGION environment variable

3. **S3 Access Issues**
   - Solution: Check bucket permissions
   - Verify bucket name in configuration

4. **Token Limits**
   - Solution: Claude has different limits than GPT-4o
   - Adjust content chunking if needed

### Getting Help

1. Check the detailed guides:
   - `backend/BEDROCK_MIGRATION.md`
   - `AWS_EC2_DEPLOYMENT.md`

2. Run diagnostic tools:
   - `python test_bedrock.py`
   - `python switch_models.py`

3. Check AWS documentation:
   - [AWS Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
   - [Claude Model Documentation](https://docs.anthropic.com/claude/docs)

## Cost Estimation

### Claude Sonnet 3.5 (approximate)
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens

### Pegasus (approximate)
- Video: $0.10-0.50 per minute
- Audio: $0.05-0.25 per minute

### Monthly Estimate (example usage)
- 1000 text queries: ~$50-100
- 100 image analyses: ~$20-40
- 50 video analyses (5 min avg): ~$25-125
- **Total**: ~$95-265/month

Compare this with your current OpenAI/Gemini costs to make an informed decision.

## Next Steps

1. **Test the Migration**:
   - Set `USE_BEDROCK_ONLY=false` initially
   - Verify existing functionality works
   - Switch to `USE_BEDROCK_ONLY=true` and test Bedrock integration

2. **Plan Deployment**:
   - Choose deployment method (local vs EC2)
   - Set up AWS infrastructure if needed
   - Configure monitoring and logging

3. **Monitor Performance**:
   - Compare response times and accuracy
   - Monitor costs and usage
   - Gather user feedback

4. **Optimize**:
   - Fine-tune prompts for Claude if needed
   - Adjust file processing workflows
   - Implement caching strategies

## Support

For issues specific to this migration:
1. Check the troubleshooting sections in the guides
2. Run the diagnostic scripts
3. Review AWS CloudTrail logs for API calls
4. Contact AWS support for Bedrock-specific issues

The application now provides you with the flexibility to choose between different AI model providers based on your specific needs for privacy, cost, performance, and compliance requirements.