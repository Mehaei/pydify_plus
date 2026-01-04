# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:44:56
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-26 10:31:53

# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:44:56
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11 16:01:21

"""Configuration module for Dify API endpoints.

This module defines all the API endpoint paths used by the Dify client.
These endpoints are organized by functionality and are used internally
by the API modules to construct requests.
"""

API_ENDPOINTS = {
    "CHAT_MESSAGES_CREATE": "/v1/chat-messages",
    "CHAT_MESSAGES_GET": "/v1/chat-messages/{conversation_id}",
    "CHAT_MESSAGES_STREAM": "/v1/chat-messages", # ✅
    "CHAT_MESSAGES_STOP": "/v1/chat-messages/{task_id}/stop", # ✅
    "CHAT_SUGGESTED_QUESTIONS": "/v1/chat-messages/{message_id}/suggested-questions",

    # Text generation
    "COMPLETION_MESSAGES_CREATE": "/v1/completion-messages",
    "COMPLETION_MESSAGES_STREAM": "/v1/completion-messages/stream",
    "COMPLETION_MESSAGES_STOP": "/v1/completion-messages/{message_id}/stop",

    # ✅
    "DATASETS_CREATE": "/v1/datasets",
    "DATASETS_LIST": "/v1/datasets",
    "DATASET_DETAIL": "/v1/datasets/{dataset_id}",
    "DATASET_UPDATE": "/v1/datasets/{dataset_id}",
    "DATASET_DELETE": "/v1/datasets/{dataset_id}",
    "FILE_UPLOAD": "/v1/files/upload",
    "DATASETS_SEARCH": "/v1/datasets/{dataset_id}/search",

    # Documents
    "DOCUMENTS_CREATE_TEXT": "/v1/datasets/{dataset_id}/document/create-by-text",
    # ✅
    "DOCUMENTS_CREATE_FILE": "/v1/datasets/{dataset_id}/document/create-by-file",
    "DOCUMENTS_UPDATE_TEXT": "/v1/datasets/{dataset_id}/documents/{document_id}/update-by-text",
    # ✅
    "DOCUMENTS_UPDATE_FILE": "/v1/datasets/{dataset_id}/documents/{document_id}/update-by-file",
    # ✅
    "DOCUMENTS_EMBED_STATUS": "/v1/datasets/{dataset_id}/documents/{batch_id}/indexing-status",
    "DOCUMENTS_DETAIL": "/v1/datasets/{dataset_id}/documents/{document_id}",
    "DOCUMENTS_DELETE": "/v1/datasets/{dataset_id}/documents/{document_id}",
    "DOCUMENTS_LIST": "/v1/datasets/{dataset_id}/documents",
    "DOCUMENTS_UPDATE_STATUS": "/v1/datasets/{dataset_id}/documents/{document_id}/status",

    # Document segments (blocks)
    "SEGMENTS_LIST": "/v1/datasets/{dataset_id}/documents/{document_id}/segments",
    "SEGMENTS_ADD": "/v1/datasets/{dataset_id}/documents/{document_id}/segments",
    "SEGMENT_DETAIL": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}",
    "SEGMENT_UPDATE": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}",
    "SEGMENT_DELETE": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}",
    "SEGMENT_CHILDREN_LIST": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/children",
    "SEGMENT_CHILD_CREATE": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/children",
    "SEGMENT_CHILD_DELETE": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/children/{child_id}",
    "SEGMENT_CHILD_UPDATE": "/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/children/{child_id}",

    # ✅
    # Files
    "FILES_UPLOAD": "/v1/files/upload",
    "FILES_PREVIEW": "/v1/files/{file_id}/preview",

    # Sessions / Conversations
    "CONVERSATIONS_LIST": "/v1/conversations",
    "CONVERSATION_DELETE": "/v1/conversations/{conversation_id}",
    "CONVERSATION_RENAME": "/v1/conversations/{conversation_id}/name",
    "CONVERSATION_HISTORY": "/v1/conversations/{conversation_id}/messages",
    "CONVERSATION_VARIABLES": "/v1/conversations/{conversation_id}/variables",

    # Feedback
    "FEEDBACK_LIKE": "/v1/feedbacks/{message_id}/like",
    "FEEDBACK_LIST": "/v1/feedbacks",

    # Workflows
    "WORKFLOW_EXECUTE": "/v1/workflows/{workflow_id}/execute",
    "WORKFLOW_EXECUTION_STATUS": "/v1/workflows/{workflow_id}/executions/{execution_id}",
    "WORKFLOW_STOP_TASK": "/v1/workflows/{workflow_id}/executions/{execution_id}/stop",
    "WORKFLOW_LOGS": "/v1/workflows/{workflow_id}/executions/{execution_id}/logs",
    "WORKFLOW_FILES_UPLOAD": "/v1/workflows/{workflow_id}/files/upload",

    # App settings / config
    "APP_BASIC_INFO": "/v1/app/basic-info",
    "APP_PARAMETERS": "/v1/app/parameters",
    "APP_META": "/v1/app/meta",
    "APP_WEBAPP_SETTINGS": "/v1/app/webapp-settings",
    "WORKFLOW_APP_BASIC_INFO": "/v1/workflow/app/basic-info",
    "WORKFLOW_APP_PARAMETERS": "/v1/workflow/app/parameters",
    "WORKFLOW_APP_WEBAPP_SETTINGS": "/v1/workflow/app/webapp-settings",

    # Models
    "EMBEDDING_MODELS_LIST": "/v1/models/embeddings",

    # Metadata & tags
    "KB_TYPE_TAGS_LIST": "/v1/metadata/kb-type-tags",
    "KB_TYPE_TAGS_CREATE": "/v1/metadata/kb-type-tags",
    "KB_TYPE_TAGS_DELETE": "/v1/metadata/kb-type-tags/{tag_id}",
    "KB_TYPE_TAGS_RENAME": "/v1/metadata/kb-type-tags/{tag_id}/name",
    "KB_TYPE_TAGS_BIND_DATASET": "/v1/metadata/kb-type-tags/{tag_id}/datasets/{dataset_id}",
    "KB_TYPE_TAGS_UNBIND_DATASET": "/v1/metadata/kb-type-tags/{tag_id}/datasets/{dataset_id}",
    "DATASET_BOUND_TAGS": "/v1/datasets/{dataset_id}/tags",
}