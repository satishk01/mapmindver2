# Frontend Bedrock Integration Update

This document describes the changes made to integrate AWS Bedrock (Claude Sonnet 3.5) into the frontend interface.

## Changes Made

### PDF Upload Modal (`frontend/src/modals/PDFModal.jsx`)

**Updated Processing Options:**
- Changed "OpenAI" option to "AWS Bedrock (Claude Sonnet 3.5)"
- Kept the processing_type value as "gpt" (backend routes this to Claude when USE_BEDROCK_ONLY=true)
- Default selection is now "gpt" (AWS Bedrock)

**Current Options:**
1. **AWS Bedrock (Claude Sonnet 3.5)** - `processing_type: "gpt"`
2. **AWS Textract** - `processing_type: "aws"`  
3. **Custom RAG** - `processing_type: "custom"`

## How It Works

### Backend Integration
The backend automatically uses the appropriate model based on the `USE_BEDROCK_ONLY` environment variable:

- When `USE_BEDROCK_ONLY=true`: "gpt" processing_type → Claude Sonnet 3.5
- When `USE_BEDROCK_ONLY=false`: "gpt" processing_type → OpenAI GPT

### Processing Type Mapping

| Frontend Display | processing_type | Bedrock Mode | OpenAI Mode |
|------------------|----------------|--------------|-------------|
| AWS Bedrock (Claude Sonnet 3.5) | "gpt" | Claude Sonnet 3.5 | OpenAI GPT-4 |
| AWS Textract | "aws" | AWS Textract | AWS Textract |
| Custom RAG | "custom" | Custom Processing | Custom Processing |

## Other Document Types

Other document upload modals (DOCX, PPTX, MD, etc.) don't have processing type selection because:

1. They have simpler processing workflows
2. The backend automatically uses the appropriate model based on `USE_BEDROCK_ONLY` setting
3. No alternative processing methods are available for these file types

## User Experience

When users upload a PDF:

1. **Default Selection**: "AWS Bedrock (Claude Sonnet 3.5)" is pre-selected
2. **Clear Labeling**: Users can see they're using Claude Sonnet 3.5 via Bedrock
3. **Alternative Options**: AWS Textract and Custom RAG remain available

## Backend Requirements

For this frontend update to work properly, ensure:

1. `USE_BEDROCK_ONLY=true` in your backend `.env` file
2. AWS Bedrock is properly configured with Claude Sonnet 3.5 access
3. AWS credentials are configured for Bedrock access

## Verification

To verify the integration is working:

1. Upload a PDF file
2. Select "AWS Bedrock (Claude Sonnet 3.5)"
3. Check the backend logs for Claude/Bedrock API calls
4. Verify the processing results use Claude's analysis

## Future Enhancements

Potential future improvements:

1. **Model Selection**: Allow users to choose specific Claude models (Haiku, Sonnet, Opus)
2. **Processing Indicators**: Show which model is actually being used based on backend configuration
3. **Performance Metrics**: Display processing time and token usage for different models
4. **Batch Processing**: Support for multiple file uploads with Bedrock processing

## Technical Notes

- The processing_type value remains "gpt" for backward compatibility
- Backend routing handles the actual model selection based on environment configuration
- No changes needed to other document upload modals
- API endpoints remain unchanged