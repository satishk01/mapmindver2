# AWS Bedrock Migration Guide

This application has been updated to support AWS Bedrock models as an alternative to OpenAI and Google Gemini models.

## Model Mapping

### Text Processing
- **Before**: OpenAI GPT-4o
- **After**: AWS Bedrock Claude Sonnet 3.5 (`anthropic.claude-3-5-sonnet-20241022-v2:0`)

### Image Analysis
- **Before**: Google Gemini 2.0 Flash
- **After**: AWS Bedrock Claude Sonnet 3.5 (with vision capabilities)

### Video/Audio Analysis
- **Before**: Google Gemini 2.0 Flash
- **After**: AWS Bedrock Pegasus (`us.twelvelabs.pegasus-1-2-v1:0`)

### YouTube Analysis
- **Before**: Google Vertex AI Gemini 2.0 Flash
- **After**: AWS Bedrock Pegasus

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# AWS Region where Bedrock models are available
AWS_REGION=us-east-1

# Set to 'true' to use only AWS Bedrock models
# Set to 'false' to use OpenAI + Google Gemini models
USE_BEDROCK_ONLY=false
```

### AWS IAM Permissions

Your AWS role/user needs the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:*::foundation-model/us.twelvelabs.pegasus-1-2-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## Model Availability

### Claude Sonnet 3.5
Available in these regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)

### Pegasus
Available in these regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)

## Migration Steps

1. **Update Environment Variables**:
   ```bash
   AWS_REGION=us-east-1
   USE_BEDROCK_ONLY=true
   ```

2. **Configure AWS Credentials**:
   - Use IAM roles (recommended for EC2)
   - Or set AWS credentials in environment variables

3. **Enable Bedrock Models**:
   - Go to AWS Bedrock console
   - Request access to Claude Sonnet 3.5 and Pegasus models
   - Wait for approval (usually instant for Claude, may take time for Pegasus)

4. **Test the Configuration**:
   - Start with `USE_BEDROCK_ONLY=false` to ensure existing functionality works
   - Switch to `USE_BEDROCK_ONLY=true` to test Bedrock integration

## Cost Considerations

### Claude Sonnet 3.5 Pricing (approximate)
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens

### Pegasus Pricing
- Video analysis: ~$0.10-0.50 per minute of video
- Audio analysis: ~$0.05-0.25 per minute of audio

### Comparison with Previous Models
- Generally more expensive than OpenAI GPT-4o
- Potentially more cost-effective than Google Gemini for large volumes
- Consider usage patterns when choosing models

## Troubleshooting

### Common Issues

1. **Model Access Denied**:
   - Ensure you've requested access to models in Bedrock console
   - Check IAM permissions

2. **Region Errors**:
   - Verify models are available in your selected region
   - Update AWS_REGION environment variable

3. **S3 Access Issues**:
   - Ensure bucket exists and is accessible
   - Check S3 permissions for Pegasus model

4. **Token Limits**:
   - Claude has different token limits than GPT-4o
   - Adjust content chunking if needed

## Performance Notes

- **Claude Sonnet 3.5**: Generally faster response times than GPT-4o
- **Pegasus**: Specialized for video/audio, may be slower but more accurate for multimedia content
- **Network Latency**: Choose AWS region closest to your deployment for best performance