# PDF Processing Guide

## Processing Types

### 🤖 AWS Bedrock (Claude Sonnet 3.5) - Recommended
- **Best for**: Comprehensive document analysis and intelligent summaries
- **Processing time**: 30 seconds - 3 minutes
- **File size limit**: Up to 50MB
- **Features**: AI-powered understanding, context-aware summaries, intelligent extraction

### ⚡ AWS Textract - Fast OCR
- **Best for**: Quick text extraction from scanned documents
- **Processing time**: 10-60 seconds
- **File size limit**: Up to 100MB
- **Features**: OCR, table extraction, form recognition

### 🔬 Custom RAG - Advanced Analysis
- **Best for**: Detailed analysis, Q&A preparation, semantic search
- **Processing time**: 1-5 minutes
- **File size limit**: Up to 25MB
- **Features**: Semantic chunking, vector embeddings, advanced search capabilities

## Troubleshooting

### Processing Takes Too Long
- **Cause**: Large or complex PDF files
- **Solution**: 
  - Try a smaller file first
  - Use "AWS Textract" for faster processing
  - Ensure stable internet connection
  - Wait patiently - complex documents can take 3-5 minutes

### Processing Fails
- **Common causes**:
  - File too large (>50MB)
  - Corrupted PDF file
  - Network timeout
  - Server overload

- **Solutions**:
  1. **Reduce file size**: Split large PDFs or compress them
  2. **Check file integrity**: Ensure PDF opens correctly in other applications
  3. **Try different processing type**: Switch from Claude to Textract for faster processing
  4. **Retry**: Sometimes temporary server issues resolve quickly

### Upload Stuck at 0%
- **Cause**: Network or server connection issues
- **Solution**: 
  - Check internet connection
  - Refresh the page and try again
  - Try a smaller file first

### "Server Error" Messages
- **Cause**: Backend processing issues
- **Solution**:
  - Wait a few minutes and retry
  - Try a different processing type
  - Contact support if issue persists

## Best Practices

### File Preparation
- **Optimal size**: 1-10MB for best performance
- **Format**: Native PDF (not scanned) works best with Claude
- **Content**: Text-based PDFs process faster than image-heavy documents

### Processing Type Selection
- **For reports/articles**: Use Claude Sonnet 3.5
- **For scanned documents**: Use AWS Textract
- **For research papers**: Use Custom RAG for better Q&A capabilities

### Performance Tips
- **Start small**: Test with a small PDF first
- **Be patient**: Complex analysis takes time
- **Monitor progress**: Watch the progress indicator and status messages
- **Cancel if needed**: Use cancel button if processing takes too long

## Expected Processing Times

| File Size | Claude Sonnet | AWS Textract | Custom RAG |
|-----------|---------------|--------------|------------|
| < 1MB     | 15-30 sec     | 5-15 sec     | 30-60 sec  |
| 1-5MB     | 30-90 sec     | 15-30 sec    | 1-2 min    |
| 5-15MB    | 1-3 min       | 30-60 sec    | 2-4 min    |
| 15-50MB   | 2-5 min       | 1-2 min      | 3-6 min    |

## Error Codes

- **400**: Invalid file or parameters
- **408**: Request timeout (processing took too long)
- **413**: File too large
- **500**: Server processing error
- **503**: Service temporarily unavailable

## Support

If you continue to experience issues:
1. Check the browser console for detailed error messages
2. Try with a different, smaller PDF file
3. Verify your internet connection is stable
4. Contact technical support with the error details