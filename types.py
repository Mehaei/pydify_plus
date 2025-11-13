"""Type definitions for Dify Client."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypedDict, Union

if TYPE_CHECKING:
    from .models import (
        ChatMessageResponse,
        DatasetResponse,
        DocumentResponse,
        WorkflowExecutionResponse,
        AppConfigResponse,
        UploadFileResponse,
    )


# Generic response types
class APIResponse(TypedDict, total=False):
    """Generic API response type."""

    id: str
    created_at: int
    updated_at: int


# Chat types
class ChatMessageDict(TypedDict):
    """Type for chat message dictionary."""

    role: str
    content: str


class CreateChatMessageParams(TypedDict, total=False):
    """Parameters for creating a chat message."""

    model: str
    messages: List[ChatMessageDict]
    conversation_id: Optional[str]
    user: Optional[str]
    stream: bool
    inputs: Optional[Dict[str, Any]]
    query: Optional[str]
    files: Optional[List[str]]


# Dataset types
class CreateDatasetParams(TypedDict, total=False):
    """Parameters for creating a dataset."""

    name: str
    description: Optional[str]
    permission: Optional[str]
    indexing_technique: Optional[str]


class SearchDatasetParams(TypedDict, total=False):
    """Parameters for searching a dataset."""

    query: str
    top_k: Optional[int]
    score_threshold: Optional[float]
    reranking_model: Optional[str]


# File types
class UploadFileParams(TypedDict, total=False):
    """Parameters for uploading a file."""

    file: Any  # File-like object
    filename: Optional[str]
    user: Optional[str]


# Workflow types
class ExecuteWorkflowParams(TypedDict, total=False):
    """Parameters for executing a workflow."""

    inputs: Dict[str, Any]
    user: Optional[str]
    response_mode: Optional[str]
    files: Optional[List[str]]


# Document types
class CreateDocumentParams(TypedDict, total=False):
    """Parameters for creating a document."""

    name: str
    text: Optional[str]
    file_id: Optional[str]
    indexing_technique: Optional[str]
    process_rule: Optional[Dict[str, Any]]
    doc_form: Optional[str]
    doc_language: Optional[str]


# Session types
class ConversationHistoryParams(TypedDict, total=False):
    """Parameters for getting conversation history."""

    limit: Optional[int]
    last_id: Optional[str]
    pinned: Optional[bool]


# Response type aliases for better IDE support
ChatMessageResponseType = Union[Dict[str, Any], "ChatMessageResponse"]
DatasetResponseType = Union[Dict[str, Any], "DatasetResponse"]
DocumentResponseType = Union[Dict[str, Any], "DocumentResponse"]
WorkflowExecutionResponseType = Union[Dict[str, Any], "WorkflowExecutionResponse"]
AppConfigResponseType = Union[Dict[str, Any], "AppConfigResponse"]
UploadFileResponseType = Union[Dict[str, Any], "UploadFileResponse"]


# Streaming types
class StreamEvent(TypedDict, total=False):
    """Type for streaming events."""

    event: str
    data: Union[str, Dict[str, Any]]
    id: Optional[str]
    retry: Optional[int]


# Pagination types
class PaginatedResponse(TypedDict, total=False):
    """Type for paginated responses."""

    data: List[Dict[str, Any]]
    has_more: bool
    limit: int
    total: Optional[int]
    page: Optional[int]


# Error response types
class ErrorResponse(TypedDict):
    """Type for error responses."""

    code: str
    message: str
    status: int
    details: Optional[Dict[str, Any]]
