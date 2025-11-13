from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict


class MessageRole(str, Enum):
    """Role of a message in a conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class DocumentStatus(str, Enum):
    """Status of a document in the dataset."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class WorkflowExecutionStatus(str, Enum):
    """Status of a workflow execution."""
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    STOPPED = "stopped"

class ChatMessage(BaseModel):
    """A single message in a conversation."""

    model_config = ConfigDict(use_enum_values=True)

    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")


class CreateChatMessageRequest(BaseModel):
    """Request model for creating a chat message."""

    model: str = Field(..., description="The model to use for the chat")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")
    conversation_id: Optional[str] = Field(None, description="ID of the conversation")
    user: Optional[str] = Field(None, description="User identifier")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")
    inputs: Optional[Dict[str, Any]] = Field(None, description="Additional input variables")
    query: Optional[str] = Field(None, description="User query for retrieval")
    files: Optional[List[str]] = Field(None, description="List of file IDs")


class CreateDatasetRequest(BaseModel):
    """Request model for creating a dataset."""

    name: str = Field(..., description="Name of the dataset")
    description: Optional[str] = Field(None, description="Description of the dataset")
    permission: Optional[str] = Field("only_me", description="Dataset permission level")
    indexing_technique: Optional[str] = Field("high_quality", description="Indexing technique to use")


class UploadFileResponse(BaseModel):
    """Response model for file upload."""

    id: str = Field(..., description="File ID")
    name: str = Field(..., description="File name")
    size: int = Field(..., description="File size in bytes")
    type: str = Field(..., description="File type")
    created_at: int = Field(..., description="Creation timestamp")
    extension: Optional[str] = Field(None, description="File extension")
    mime_type: Optional[str] = Field(None, description="MIME type")


class DatasetResponse(BaseModel):
    """Response model for dataset operations."""

    id: str = Field(..., description="Dataset ID")
    name: str = Field(..., description="Dataset name")
    description: Optional[str] = Field(None, description="Dataset description")
    provider: str = Field(..., description="Data provider")
    permission: str = Field(..., description="Permission level")
    data_source_type: str = Field(..., description="Data source type")
    indexing_technique: str = Field(..., description="Indexing technique")
    app_count: int = Field(..., description="Number of apps using this dataset")
    document_count: int = Field(..., description="Number of documents in the dataset")
    word_count: int = Field(..., description="Total word count")
    created_by: str = Field(..., description="Creator ID")
    created_at: int = Field(..., description="Creation timestamp")
    updated_at: int = Field(..., description="Last update timestamp")


class DocumentResponse(BaseModel):
    """Response model for document operations."""

    id: str = Field(..., description="Document ID")
    dataset_id: str = Field(..., description="Dataset ID")
    position: int = Field(..., description="Document position")
    data_source_type: str = Field(..., description="Data source type")
    data_source_info: Optional[Dict[str, Any]] = Field(None, description="Data source information")
    dataset_process_rule_id: Optional[str] = Field(None, description="Process rule ID")
    name: str = Field(..., description="Document name")
    created_from: str = Field(..., description="Creation source")
    created_by: str = Field(..., description="Creator ID")
    created_at: int = Field(..., description="Creation timestamp")
    tokens: int = Field(..., description="Token count")
    indexing_status: str = Field(..., description="Indexing status")
    enabled: bool = Field(..., description="Whether the document is enabled")
    disabled_at: Optional[int] = Field(None, description="Disable timestamp")
    disabled_by: Optional[str] = Field(None, description="User who disabled the document")
    archived: bool = Field(..., description="Whether the document is archived")
    display_status: str = Field(..., description="Display status")
    word_count: Optional[int] = Field(None, description="Word count")
    hit_count: Optional[int] = Field(None, description="Hit count")
    segment_count: Optional[int] = Field(None, description="Segment count")


class WorkflowExecutionResponse(BaseModel):
    """Response model for workflow execution."""

    execution_id: str = Field(..., description="Execution ID")
    total_tokens: Optional[int] = Field(None, description="Total tokens used")
    status: WorkflowExecutionStatus = Field(..., description="Execution status")
    outputs: Optional[Dict[str, Any]] = Field(None, description="Execution outputs")
    error: Optional[str] = Field(None, description="Error message if failed")
    elapsed_time: Optional[float] = Field(None, description="Elapsed time in seconds")
    total_steps: Optional[int] = Field(None, description="Total steps")
    finished_steps: Optional[int] = Field(None, description="Finished steps")
    created_at: int = Field(..., description="Creation timestamp")
    finished_at: Optional[int] = Field(None, description="Finish timestamp")


class ChatMessageResponse(BaseModel):
    """Response model for chat message creation."""

    id: str = Field(..., description="Message ID")
    conversation_id: str = Field(..., description="Conversation ID")
    query: str = Field(..., description="User query")
    answer: str = Field(..., description="Assistant answer")
    message_files: List[str] = Field(default_factory=list, description="Message files")
    created_at: int = Field(..., description="Creation timestamp")


class StreamingChatDelta(BaseModel):
    """Delta update for streaming chat responses."""

    event: str = Field(..., description="Event type")
    data: Union[str, Dict[str, Any]] = Field(..., description="Event data")
    id: Optional[str] = Field(None, description="Event ID")
    retry: Optional[int] = Field(None, description="Retry interval")


class AppConfigResponse(BaseModel):
    """Response model for app configuration."""

    app_id: str = Field(..., description="App ID")
    name: str = Field(..., description="App name")
    description: Optional[str] = Field(None, description="App description")
    mode: str = Field(..., description="App mode (chat/completion/workflow)")
    icon: Optional[str] = Field(None, description="App icon")
    icon_background: Optional[str] = Field(None, description="Icon background color")
    show_workflow_steps: bool = Field(False, description="Whether to show workflow steps")
    enable_speech: bool = Field(False, description="Whether speech is enabled")
    enable_video: bool = Field(False, description="Whether video is enabled")
    enable_upload: bool = Field(False, description="Whether file upload is enabled")
    copyright: Optional[str] = Field(None, description="Copyright information")
    privacy_policy: Optional[str] = Field(None, description="Privacy policy")
    custom_disclaimer: Optional[str] = Field(None, description="Custom disclaimer")
    sensitive_word_avoidance_enabled: bool = Field(False, description="Sensitive word avoidance")
    created_at: int = Field(..., description="Creation timestamp")
    updated_at: int = Field(..., description="Last update timestamp")
