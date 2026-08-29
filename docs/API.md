# API Architecture & Endpoint Standards

## 1. Global Standard Response Format
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "timestamp": "2026-08-29T23:55:00Z",
  "requestId": "9c8b76e1-5e22-4e07-a3a2-094ec2352cb2"
}
```

## 2. Standard Error Response Format
```json
{
  "timestamp": "2026-08-29T23:55:00Z",
  "requestId": "9c8b76e1-5e22-4e07-a3a2-094ec2352cb2",
  "status": 400,
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "fieldErrors": [
    {
      "field": "title",
      "message": "Title is required",
      "rejectedValue": ""
    }
  ]
}
```
